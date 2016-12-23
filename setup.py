#! /usr/bin/env python
# -*- coding: utf-8 -*-
import re
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

VERSION_PY_FILENAME = 'kalliope/_version.py'
version = read_version_py(VERSION_PY_FILENAME)

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
        'Topic :: Home Automation',
        'Topic :: Multimedia :: Sound/Audio :: Speech',
        'Topic :: Multimedia :: Sound/Audio :: Sound Synthesis',
        'Topic :: Scientific/Engineering :: Artificial Intelligence'
    ],
    keywords='assistant bot TTS STT',

    # included packages
    packages=find_packages(exclude=['contrib', 'docs', 'tests']),

    # required libs
    install_requires=[
        'six==1.10.0',
        'SpeechRecognition>=3.5.0',
        'markupsafe==0.23',
        'pyaudio==0.2.9',
        'ansible==2.2.0.0',
        'python2-pythondialog==3.4.0',
        'jinja2==2.8',
        'cffi==1.9.1',
        'ipaddress==1.0.17',
        'flask==0.11.1',
        'Flask-Restful==0.3.5',
        'requests==2.12.4',
        'httpretty==0.8.14',
        'mock==2.0.0',
        'Flask-Testing==0.6.1',
        'apscheduler==3.3.0',
        'GitPython==2.1.1',
        'packaging>=16.8'
    ],


    # additional files
    package_data={
        'kalliope': [
            'brain.yml',
            'settings.yml',
            'trigger/snowboy/armv7l/_snowboydetect.so',
            'trigger/snowboy/x86_64/_snowboydetect.so',
            'trigger/snowboy/resources/*',
         ],
    },

    # entry point script
    entry_points={
        'console_scripts': [
            'kalliope=kalliope:main',
        ],
    },
)

