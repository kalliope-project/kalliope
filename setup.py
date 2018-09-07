#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
import sys
from setuptools import setup, find_packages
from codecs import open
from os import path

basedir = path.abspath(path.dirname(__file__))

# Get the long description from the README file
with open(path.join(basedir, 'README.md'), encoding='utf-8') as f:
    long_description = f.read()

# get requirements
with open('install/files/python_requirements.txt') as f:
    requirements = f.read().splitlines()


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

VERSION_PY_FILENAME = 'kalliope/_version.py'
version = read_version_py(VERSION_PY_FILENAME)

py2_prefix = ''
if sys.version_info[0] < 3:
    py2_prefix = 'python2-'

setup(
    name='kalliope',
    version=version,
    description='Kalliope is a modular always-on voice controlled personal assistant designed for home automation.',
    long_description=long_description,
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
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    keywords='assistant bot TTS STT jarvis',

    # included packages
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # required libs
    install_requires=requirements,

    # additional files
    package_data={
        'kalliope': [
            'brain.yml',
            'settings.yml',
            'trigger/snowboy/armv7l/python27/_snowboydetect.so',
            'trigger/snowboy/x86_64/python27/_snowboydetect.so',
            'trigger/snowboy/x86_64/python34/_snowboydetect.so',
            'trigger/snowboy/x86_64/python35/_snowboydetect.so',
            'trigger/snowboy/x86_64/python36/_snowboydetect.so',
            'trigger/snowboy/resources/*',
            'sounds/*'
         ],
    },

    # entry point script
    entry_points={
        'console_scripts': [
            'kalliope=kalliope:main',
        ],
    },
)
