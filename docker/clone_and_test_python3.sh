#!/usr/bin/env bash

# install dev version
git clone https://github.com/kalliope-project/kalliope.git kalliope;
cd kalliope;
git checkout dev;

# install
sudo python3 setup.py install

# tests
export LANG=C.UTF-8
python3 -m unittest discover
