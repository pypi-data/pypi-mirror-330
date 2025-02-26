from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="coolprop-oop",
    version="0.1.0",
    author="Ryan Cox",
    author_email="your.email@example.com",
    description="Object-oriented wrapper for CoolProp thermodynamic properties",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/ryancoxrbc/coolprop_oop",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Scientific/Engineering :: Physics",
        "Topic :: Scientific/Engineering :: Chemistry",
    ],
    python_requires=">=3.8",
    install_requires=[
        "CoolProp>=6.4.1",
    ],
    include_package_data=True,
    package_data={
        "": ["LICENSE", "README.md"],
    },
) 