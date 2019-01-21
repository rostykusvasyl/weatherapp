from setuptools import setup, find_namespace_packages

with open("README.txt", "r") as fh:
    long_description = fh.read()

setup(
    name="weatherapp.core",
    version="0.1.0",
    author="Vasyl Rostykus",
    description="A simple cli weather aggregator",
    long_description=long_description,
    packages=find_namespace_packages(),
    entry_points={
        'console_scripts': 'wfapp=weatherapp.core.app:main'
    },
    install_requires=[
        'requests',
        'bs4',
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
