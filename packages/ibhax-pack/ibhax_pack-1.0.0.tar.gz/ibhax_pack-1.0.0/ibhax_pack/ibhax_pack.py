#!/usr/bin/env python3
import argparse
import configparser
import fnmatch
import json
import os
import shutil
import subprocess
import sys
import tempfile

try:
    import yaml
except ImportError:
    yaml = None

from cookiecutter.main import cookiecutter

# --- Constants and Defaults ---
DEFAULT_IGNORE = ['.env', '.git', 'venv', '__pycache__']
TOKEN_CONFIG_PATH = os.path.join(os.path.expanduser("~"), ".package_manager_token.ini")
PYPIRC_SECTION = 'pypi'

# --- Configuration Loading Functions ---
def load_config_file(path):
    """Load configuration from a YAML or INI file based on extension."""
    config_data = {}
    ext = os.path.splitext(path)[1].lower()
    if ext in ['.yaml', '.yml']:
        if not yaml:
            print("PyYAML is required for YAML config support. Please install it.")
            sys.exit(1)
        with open(path, 'r') as f:
            config_data = yaml.safe_load(f)
    elif ext == '.ini':
        parser = configparser.ConfigParser()
        parser.read(path)
        if 'package' in parser:
            config_data = dict(parser['package'])
    else:
        print("Unsupported config file format. Use YAML or INI.")
        sys.exit(1)
    # If console_scripts is provided as a string, convert it to a list.
    if "console_scripts" in config_data and isinstance(config_data["console_scripts"], str):
        # Expecting a semicolon-separated list: "cmd1=mod1:func1; cmd2=mod2:func2"
        config_data["console_scripts"] = [s.strip() for s in config_data["console_scripts"].split(';') if s.strip()]
    return config_data

def interactive_prompt():
    """Prompt the user for package details interactively."""
    config = {}
    config['package_name'] = input("Enter the package name: ").strip()
    config['version'] = input("Enter the version [0.1.0]: ").strip() or "0.1.0"
    config['description'] = input("Enter the package description: ").strip()
    config['author'] = input("Enter the author name: ").strip()
    deps = input("Enter dependencies (comma separated, leave empty if none): ").strip()
    config['dependencies'] = [d.strip() for d in deps.split(",") if d.strip()]

    # Prompt for multiple console scripts.
    scripts = []
    add_script = input("Do you want to add a console script? (y/n): ").strip().lower()
    while add_script == 'y':
        script_name = input("Enter the console script command name: ").strip()
        script_callable = input("Enter the callable (module:function): ").strip()
        scripts.append(f"{script_name}={script_callable}")
        add_script = input("Add another console script? (y/n): ").strip().lower()
    config['console_scripts'] = scripts

    publish = input("Do you want to publish the package after building? (y/n): ").strip().lower()
    config['publish'] = (publish == 'y')
    return config

def parse_args():
    parser = argparse.ArgumentParser(
        description="One-stop tool to package a Python project and optionally publish to PyPI"
    )
    parser.add_argument("--config", help="Path to configuration file (YAML or INI)")
    parser.add_argument("--package-dir", help="Directory containing files to package", default=".")
    parser.add_argument("--non-interactive", action="store_true",
                        help="Run without interactive prompts (use config or command-line args)")
    return parser.parse_args()

# --- Token and Publishing Functions ---
def get_token():
    """Check for token in environment or in token config file; otherwise prompt for it."""
    token = os.environ.get("PYPI_TOKEN")
    if token:
        return token
    # Try loading from token config file.
    parser = configparser.ConfigParser()
    if os.path.exists(TOKEN_CONFIG_PATH):
        parser.read(TOKEN_CONFIG_PATH)
        if parser.has_option(PYPIRC_SECTION, 'token'):
            return parser.get(PYPIRC_SECTION, 'token')
    # If not found, prompt the user.
    token = input("Enter your PyPI token: ").strip()
    if not parser.has_section(PYPIRC_SECTION):
        parser.add_section(PYPIRC_SECTION)
    parser.set(PYPIRC_SECTION, 'token', token)
    with open(TOKEN_CONFIG_PATH, 'w') as f:
        parser.write(f)
    return token

# --- Cookiecutter Template Generation ---
def generate_cookiecutter_template(config, template_dir):
    """
    Create a cookiecutter template in the given directory.
    The template structure will be:
    
    template_dir/
        cookiecutter.json
        {{cookiecutter.package_name}}/     # Project root
            setup.py
            README.md
            tests/
                __init__.py
            {{cookiecutter.package_name}}/ # Actual package code
                __init__.py
                main.py
    """
    # Ensure dependencies are represented as a comma-separated string (if any).
    dependencies_str = ""
    if config.get("dependencies"):
        deps = [f'"{dep}"' for dep in config["dependencies"]]
        dependencies_str = ", ".join(deps)
    
    # Process console_scripts: if the callable part doesn't contain a dot, prefix it with the package name.
    new_scripts = []
    for script in config.get("console_scripts", []):
        if "=" in script:
            cmd, callable_str = script.split("=", 1)
            if ":" in callable_str:
                module_part, func_part = callable_str.split(":", 1)
                if "." not in module_part:
                    module_part = f"{config['package_name']}.{module_part}"
                new_scripts.append(f"{cmd}={module_part}:{func_part}")
            else:
                new_scripts.append(script)
        else:
            new_scripts.append(script)
    # Update config with processed console_scripts.
    config["console_scripts"] = new_scripts

    # Build cookiecutter JSON.
    cookiecutter_json = {
        "package_name": config.get("package_name", "mypackage"),
        "version": config.get("version", "0.1.0"),
        "description": config.get("description", "A new Python package"),
        "author": config.get("author", "Author Name"),
        "dependencies": dependencies_str,
    }
    # Only add console_scripts_str if console scripts exist.
    if config.get("console_scripts"):
        cookiecutter_json["console_scripts_str"] = ", ".join([f'"{s}"' for s in config["console_scripts"]])
    else:
        cookiecutter_json["console_scripts_str"] = ""

    with open(os.path.join(template_dir, "cookiecutter.json"), "w") as f:
        json.dump(cookiecutter_json, f, indent=4)

    # Create project root directory using the template variable.
    project_dir = os.path.join(template_dir, "{{cookiecutter.package_name}}")
    os.makedirs(project_dir, exist_ok=True)

    # Create setup.py in the project root.
    setup_py_content = r'''#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="{{ cookiecutter.package_name }}",
    version="{{ cookiecutter.version }}",
    author="{{ cookiecutter.author }}",
    description="{{ cookiecutter.description }}",
    packages=setuptools.find_packages(),
    install_requires=[{{ cookiecutter.dependencies }}]{% if cookiecutter.console_scripts_str|trim %}
    ,
    entry_points={
        "console_scripts": [{{ cookiecutter.console_scripts_str }}]
    }
    {% endif %}
)
'''
    with open(os.path.join(project_dir, "setup.py"), "w") as f:
        f.write(setup_py_content)

    # Create a README file.
    with open(os.path.join(project_dir, "README.md"), "w") as f:
        f.write("# {{ cookiecutter.package_name }}\n\n{{ cookiecutter.description }}\n")

    # Create tests directory.
    tests_dir = os.path.join(project_dir, "tests")
    os.makedirs(tests_dir, exist_ok=True)
    with open(os.path.join(tests_dir, "__init__.py"), "w") as f:
        f.write("# __init__.py for tests\n")

    # Create the actual package code directory inside the project root.
    pkg_code_dir = os.path.join(project_dir, "{{ cookiecutter.package_name }}")
    os.makedirs(pkg_code_dir, exist_ok=True)
    with open(os.path.join(pkg_code_dir, "__init__.py"), "w") as f:
        f.write("# __init__.py for {{ cookiecutter.package_name }} package\n")
    with open(os.path.join(pkg_code_dir, "main.py"), "w") as f:
        f.write("def main():\n    print('Hello from {{ cookiecutter.package_name }}')\n")

# --- File Copying Functions ---
def load_gitignore_patterns(package_dir):
    """If .gitignore exists, load its patterns."""
    gitignore_path = os.path.join(package_dir, ".gitignore")
    patterns = []
    if os.path.exists(gitignore_path):
        with open(gitignore_path, "r") as f:
            for line in f:
                line = line.strip()
                if line and not line.startswith("#"):
                    patterns.append(line)
    return patterns

def should_ignore(name, ignore_patterns):
    """Check if a file or directory name should be ignored based on patterns."""
    for pattern in ignore_patterns:
        if fnmatch.fnmatch(name, pattern):
            return True
    return False

def copy_project_files(src_dir, dest_dir, exclude_paths=None):
    """
    Copy files from src_dir to dest_dir, ignoring default patterns, any patterns from .gitignore,
    and any paths specified in exclude_paths (absolute paths).
    """
    if exclude_paths is None:
        exclude_paths = []
    ignore_patterns = DEFAULT_IGNORE + load_gitignore_patterns(src_dir)
    for root, dirs, files in os.walk(src_dir):
        # Skip directories within excluded paths.
        skip_root = False
        for ex in exclude_paths:
            if os.path.commonpath([os.path.abspath(root), ex]) == ex:
                skip_root = True
                break
        if skip_root:
            continue

        rel_path = os.path.relpath(root, src_dir)
        if rel_path == ".":
            rel_path = ""
        # Filter out directories matching ignore patterns.
        dirs[:] = [d for d in dirs if not should_ignore(d, ignore_patterns)]
        for file in files:
            if should_ignore(file, ignore_patterns):
                continue
            src_file = os.path.join(root, file)
            dest_file_dir = os.path.join(dest_dir, rel_path)
            os.makedirs(dest_file_dir, exist_ok=True)
            shutil.copy2(src_file, os.path.join(dest_file_dir, file))

# --- Package Building and Publishing Functions ---
def build_package(package_path):
    """Build the package using setup.py to create sdist and wheel."""
    current_dir = os.getcwd()
    os.chdir(package_path)
    try:
        print("Building package...")
        subprocess.run([sys.executable, "setup.py", "sdist", "bdist_wheel"], check=True)
    except subprocess.CalledProcessError as e:
        print("Error during build:", e)
        sys.exit(1)
    finally:
        os.chdir(current_dir)

def publish_package(package_path, token):
    """Publish the package using twine."""
    current_dir = os.getcwd()
    os.chdir(package_path)
    try:
        print("Publishing package to PyPI...")
        subprocess.run([
            sys.executable, "-m", "twine", "upload", "dist/*",
            "-u", "__token__", "-p", token
        ], check=True)
    except subprocess.CalledProcessError as e:
        print("Error during publishing:", e)
        sys.exit(1)
    finally:
        os.chdir(current_dir)

# --- Main Execution Flow ---
def main():
    args = parse_args()

    # Determine configuration details.
    if args.config:
        config = load_config_file(args.config)
    elif args.non_interactive:
        print("Non-interactive mode requires a config file or command-line parameters.")
        sys.exit(1)
    else:
        config = interactive_prompt()

    # Ensure console_scripts is a list even if coming from a config file.
    if "console_scripts" in config and isinstance(config["console_scripts"], str):
        config["console_scripts"] = [s.strip() for s in config["console_scripts"].split(';') if s.strip()]

    package_dir = os.path.abspath(args.package_dir)

    # Create a temporary directory for the cookiecutter template.
    with tempfile.TemporaryDirectory() as tmp_template_dir:
        generate_cookiecutter_template(config, tmp_template_dir)
        # Generate the project using cookiecutter (suppress prompts with no_input=True).
        output_dir = os.path.abspath("generated_package")
        cookiecutter(tmp_template_dir, no_input=True, output_dir=output_dir)

    # The generated project is in a subdirectory named after the package.
    gen_project_path = os.path.join(output_dir, config['package_name'])
    print(f"Package generated at: {gen_project_path}")

    # Copy user-specified project files into the actual package code directory.
    # The destination is the inner package folder: <gen_project_path>/<package_name>
    target_dir = os.path.join(gen_project_path, config['package_name'])
    copy_project_files(package_dir, target_dir, exclude_paths=[output_dir])
    print("Project files copied to the package directory.")

    # Build the package.
    build_package(gen_project_path)

    # Optionally publish.
    if config.get("publish", False):
        token = get_token()
        publish_package(gen_project_path, token)
        print("Package published successfully.")
    else:
        print("Package build complete. Not publishing per user choice.")

if __name__ == "__main__":
    main()
