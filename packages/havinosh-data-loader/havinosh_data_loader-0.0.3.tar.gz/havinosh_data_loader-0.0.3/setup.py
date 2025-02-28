from setuptools import setup, find_packages
from typing import List

HYPEN_E_DOT = "-e ."

def get_requirements(file_path: str) -> List[str]:
    """
    This function returns the list of package dependencies from the requirements file.
    """
    with open(file_path, "r", encoding="utf-8") as file_obj:
        requirements = [req.strip() for req in file_obj.readlines() if req.strip()]
    
    if HYPEN_E_DOT in requirements:
        requirements.remove(HYPEN_E_DOT)

    return requirements

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="havinosh_data_loader",
    version="0.0.3",  # Incremented version
    author="Vishal Singh Sangral",
    author_email="support@havinosh.com",
    description="A Python package to dynamically load CSV files into PostgreSQL tables.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/IAMDSVSSANGRAL/havinosh_data_loader",  # Update to actual repo
    packages=find_packages(include=["havinosh_data_loader", "havinosh_data_loader.*"]),
    install_requires=get_requirements("requirements.txt"),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.7",
    entry_points={
        "console_scripts": [
            "data-loader=havinosh_data_loader.scripts.ingest:main",  # Corrected CLI entry
        ]
    },
    include_package_data=True,
)
