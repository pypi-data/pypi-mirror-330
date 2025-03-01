#!/usr/bin/env python3.9.1
# authors: BarzoThom, Steinhia

from setuptools import setup

with open("requirements.txt") as req_file:
    requirements = req_file.read().splitlines()

setup(
    name='braidacq_exec',
    version='0.1.0',
    description='Toy version of Braid',
    long_description=open('README.md').read(),
    long_description_content_type="text/markdown",
    author='Alexandra Steinhilber',
    author_email='alexandra.st@free.fr',
    url='https://https://gitlab.com/braid-acq/BRAID-Acq', 
    classifiers=[
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent"
    ],
    python_requires=">=3.8.5",
    requirements=requirements,
    packages=["braidpy"],
    package_dir={'braidpy': 'braidpy'},
    package_data={
        "braidpy": [
            "resources/chardicts/*.csv",
            "resources/confusionMatrix/*.csv",
            "resources/lexicon/*.csv",
        ]},
    entry_points={
        'console_scripts': [
            'braidacq_exec = braidpy.__main__:hook'
        ]
    }
)
