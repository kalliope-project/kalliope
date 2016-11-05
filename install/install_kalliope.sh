#!/usr/bin/env bash

# install packages
sudo apt-get install -y python-pip libssl-dev

# install ansible
sudo pip install ansible==2.1.1.0

# Install the project
cd kalliope/install
ansible-playbook install.yml -K
