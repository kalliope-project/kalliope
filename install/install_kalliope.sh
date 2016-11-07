#!/usr/bin/env bash

# install packages
sudo apt-get install -y python-pip libssl-dev

# this is used to help the RPI
sudo apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 portaudio19-dev
sudo apt-get install -y libffi-dev python-yaml python-pycparser python-paramiko python-markupsafe apt-transport-https

# install ansible
sudo pip install ansible==2.1.1.0

# Install the project
cd kalliope/install
ansible-playbook install.yml -K
