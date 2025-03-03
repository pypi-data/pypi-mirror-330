from setuptools import setup, find_packages


def read_long_description(file_path):
    """Read the contents of a file and return it."""
    with open(file_path, 'r', encoding='utf-8') as file:
        return file.read()


setup(
    name="basicnumeriq",
    version="0.0.3",
    description="A simple math operations library.",
    long_description=read_long_description("README.md"),
    long_description_content_type="text/markdown",
    author="furkankarakuz",
    url="https://github.com/furkankarakuz/basicnumeriq",
    packages=find_packages(),
    install_requires=[],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: Apache Software License",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.10")
