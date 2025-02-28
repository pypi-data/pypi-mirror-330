"""
AWS Abort
A lightweight Python package for handling HTTP error status codes
by raising a custom exception with detailed, human-friendly messages.
---
setup.py is the build script for setuptools.
It tells setuptools about your package (such as the name and version) as well as which code files to include.
"""

import setuptools

with open('README.md', 'r') as readme:
    long_description = readme.read()

setuptools.setup(
    name='aws_abort',
    version="0.0.1",
    author="Joe Tilsed",
    author_email="Joe@Tilsed.com",
    description="A lightweight Python package for handling HTTP error status codes "
                "by raising a custom exception with detailed, human-friendly messages.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://bitbucket.org/joetilsed/abort/src",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent"
    ]
)


# That's all folks...
