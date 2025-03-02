'''
Author: Bryan x23399937@student.ncirl.ie
Date: 2025-03-01 12:34:59
LastEditors: Bryan x23399937@student.ncirl.ie
LastEditTime: 2025-03-01 14:24:34
FilePath: /cpp-project-library/setup.py
Description: 
setup python file
Copyright (c) 2025 by Bryan Jiang, All Rights Reserved. 
'''
import setuptools

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setuptools.setup(
    name="django_base64_bytesio",
    # Replace with your own username above
    version="0.0.4",
    author="Bryan Jiang",
    author_email="x23399937@student.ncirl.ie",
    description="Input a base64 string and return BytesIO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/BryanJiang-NCI/django-base64-bytesio",
    packages=setuptools.find_packages(),
    # if you have libraries that your module/package/library
    #you would include them in the install_requires argument
    install_requires=[''],
    classifiers=[
    "Programming Language :: Python :: 3",
    "License :: OSI Approved :: MIT License",
    "Operating System :: OS Independent",
    ],
    python_requires='>=3.6',
)