#!/usr/bin/env python
import setuptools

setuptools.setup(
    name="ibhax_pack",
    version="1.0.0",
    author="Albin Anthony",
    description="Simplified auto packaging solution",
    packages=setuptools.find_packages(),
    install_requires=["cookiecutter", "pyyaml", "twine"]
    ,
    entry_points={
        "console_scripts": ["ipack=ibhax_pack.ibhax_pack:main"]
    }
    
)
