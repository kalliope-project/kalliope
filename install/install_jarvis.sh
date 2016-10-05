#!/usr/bin/env bash

# install packages
apt-get install python-pip

# install ansible
pip install ansible==2.1.1.0

# Install the project
cd jarvis/install
ansible-playbook install/install.yml -K
