# setup.py
from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="txtgenai",
    version="0.1.0",
    author="Sohail Shaikh",
    author_email="sohailshaikharifshaikh07@gmail.com",
    description="A Python package for advanced text generation",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/Sohail-Shaikh-07/txtgenai.git",
    packages=find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    install_requires=[
        "requests>=2.25.1",
    ],
)
