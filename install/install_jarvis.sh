#!/usr/bin/env bash

# install packages
sudo apt-get install python-pip

# install ansible
sudo pip install ansible==2.1.1.0

# Install the project
cd jarvis/install
ansible-playbook install.yml -K
