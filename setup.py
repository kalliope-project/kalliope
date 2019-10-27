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
    install_requires=[
        'pyyaml>=5.1',
        'six>=1.12.0',
        'SpeechRecognition>=3.8.1',
        'markupsafe>=1.1.1',
        'pyaudio>=0.2.11',
        'pyasn1>=0.4.5',
        'ansible>=2.8.1',
        'jinja2>=2.10.1',
        'cffi>=1.12.3',
        'ipaddress>=1.0.17',
        'flask>=1.0.3',
        'Flask-Restful>=0.3.7',
        'flask_cors>=3.0.8',
        'requests>=2.22.0',
        'httpretty>=0.8.14',
        'mock>=3.0.5',
        'Flask-Testing>=0.7.1',
        'apscheduler>=3.6.0',
        'GitPython>=2.1.11',
        'packaging>=19.0',
        'transitions>=0.6.9',
        'sounddevice>=0.3.13',
        'SoundFile>=0.10.2',
        'pyalsaaudio>=0.8.4',
        'sox>=1.3.7',
        'paho-mqtt>=1.4.0',
        'voicerss_tts>=1.0.6',
        'gTTS>=2.0.3',
        'urllib3>=1.25.3',
        'gevent==1.4.0'
    ],


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
