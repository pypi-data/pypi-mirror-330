from setuptools import setup, find_packages
import os

def read_requirements():
    req_file = "requirements.txt"
    if os.path.exists(req_file):
        with open(req_file, "r") as f:
            return [line.strip() for line in f if line.strip() and not line.startswith("#")]
    return []  # Return an empty list if file doesn't exist

setup(
    name="VR_Assignment_Rutul",
    version="0.1.4",
    packages=find_packages(),
    install_requires=read_requirements(),
    author="Rutul Patel",
    author_email="githubrp@gmail.com",
    description="Coin Detection and Panorama Stitching",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/RutulPatel007/VR_Assignment_1",
    classifiers=[
        "Programming Language :: Python :: 3",
    ],
    python_requires=">=3.7",
)