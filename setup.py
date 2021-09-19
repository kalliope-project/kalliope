#! /usr/bin/env python
# -*- coding: utf-8 -*-
import os
import re

import pip
from setuptools import setup, find_packages
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()


# locate our version number
def read_version_py(file_name):
    try:
        version_string_line = open(file_name, "rt").read()
    except EnvironmentError:
        return None
    else:
        version_regex = r"^version_str = ['\"]([^'\"]*)['\"]"
        mo = re.search(version_regex, version_string_line, re.M)
        if mo:
            return mo.group(1)


def package_files(directory):
    paths = []
    for (path, directories, filenames) in os.walk(directory):
        for filename in filenames:
            paths.append(os.path.join('..', path, filename))
    return paths


VERSION_PY_FILENAME = 'kalliope/_version.py'
version = read_version_py(VERSION_PY_FILENAME)

extra_files = package_files('kalliope/trigger/snowboy')
extra_files.append('brain.yml')
extra_files.append('settings.yml')


def required():
    with open(os.path.join(basedir, "install/files/python_requirements.txt"), 'r') as f:
        return f.read().splitlines()


# required libs
required_packages = required()
for package in required_packages:
    pip.main(["install", package])

setup(
    name='kalliope',
    version=version,
    description='Kalliope is a modular always-on voice controlled personal assistant designed for home automation.',
    long_description=long_description,
    long_description_content_type='text/markdown',
    url='https://github.com/kalliope-project/kalliope',
    author='The dream team of Kalliope-project',
    author_email='kalliope-project@googlegroups.com',
    license='MIT',
    # See https://pypi.python.org/pypi?%3Aaction=list_classifiers
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: MIT License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    keywords='assistant bot TTS STT jarvis',
    zip_safe=False,
    # included packages
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),
    python_requires=">=3.6",

    # additional files
    package_data={
        'kalliope': extra_files,
    },

    # entry point script
    entry_points={
        'console_scripts': [
            'kalliope=kalliope:main',
        ],
    },
)
