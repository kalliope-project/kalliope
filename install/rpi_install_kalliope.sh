#!/usr/bin/env bash

# This script will install automatically everything needed for Kalliope
# usage: ./rpi_install_kalliope.sh [<branch_name>]
# E.g: ./rpi_install_kalliope.sh dev
# If no branch are set, the master branch will be installed

# name of the branch to install
branch="master"

# get the branch name to install from passed arguments if exist
if [ $# -eq 0 ]
  then
    echo "No arguments supplied. Master branch will be installed"
else
    branch=$1
    echo "Selected branch name to install: ${branch}"
fi

echo "Installing python pip..."
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
echo "Installing python pip... [OK]"

# install packages
echo "Installing system packages..."
sudo apt-get update
sudo apt-get install -y git python-dev libsmpeg0 \
flac libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
libssl-dev libffi-dev sox libatlas3-base mplayer libyaml-dev libpython2.7-dev libjpeg-dev

debian_version=`cat /etc/os-release |grep buster`
retVal=$?
if [ $retVal -ne 0 ]; then
    echo "Debian < 10"
    sudo apt-get install libav-tools libttspico-utils
else
    echo "Debian 10 Buster detected. Installing pico2wave manually"
    sudo apt-get install -y ffmpeg
    wget http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-utils_1.0+git20130326-9_armhf.deb
    wget http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico0_1.0+git20130326-9_armhf.deb
    wget http://ftp.fr.debian.org/debian/pool/non-free/s/svox/libttspico-data_1.0+git20130326-9_all.deb
    sudo dpkg -i libttspico-data_1.0+git20130326-9_all.deb
    sudo dpkg -i libttspico-utils_1.0+git20130326-9_armhf.deb
    sudo dpkg -i libttspico0_1.0+git20130326-9_armhf.deb
fi

# this is used to help the RPI
sudo apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0 python-yaml python-pycparser \
python-paramiko python-markupsafe apt-transport-https
sudo pip install ansible
sudo pip install openpyxl
echo "Installing system packages...[OK]"

echo "Cloning the project"
# clone the project
git clone https://github.com/kalliope-project/kalliope.git
echo "Cloning the project...[OK]"

# Install the project
echo "Installing Kalliope..."
cd kalliope
git checkout ${branch}
sudo python setup.py install

# fix https://github.com/kalliope-project/kalliope/issues/487
sudo chmod -R o+r /usr/local/lib/python2.7/dist-packages/

echo "Installing Kalliope...[OK]"
