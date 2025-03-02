"""
Setup script for SvaraScala.
"""

from setuptools import setup, find_packages

with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

setup(
    name="svarascala",
    version="0.1.0",
    author="Bruno Lago",
    author_email="teolupus@gmail.com",
    description="A library for calculating musical frequencies across Western and Indian musical systems",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/teolupus/svarascala",
    project_urls={
        "Bug Tracker": "https://github.com/teolupus/svarascala/issues",
    },
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Programming Language :: Python :: 3.11",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Topic :: Multimedia :: Sound/Audio",
        "Topic :: Scientific/Engineering :: Physics",
    ],
    packages=find_packages(),
    python_requires=">=3.8",
    entry_points={
        "console_scripts": [
            "svarascala=svarascala.main:main",
        ],
    },
)