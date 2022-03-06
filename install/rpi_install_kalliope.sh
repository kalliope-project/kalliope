#!/usr/bin/env bash

# This script will install automatically everything needed for Kalliope
# usage: ./rpi_install_kalliope.sh [<branch_name>]
# E.g: ./rpi_install_kalliope.sh dev
# If no branch are set, the master branch will be installed

#------------------------------------------
# Variables
#------------------------------------------
# name of the branch to install
branch="master"
python_version="3.9.9"
pulseaudio_service_path="/etc/systemd/system/pulseaudio.service"
#------------------------------------------
# Functions
#------------------------------------------
echo_green(){
    echo -e "\e[32m$1\033[0m"
}

echo_yellow(){
    echo -e "\e[33m$1\033[0m"
}

install_default_packages(){
    echo_green "Installing system packages..."
    sudo apt-get update
    sudo apt-get install -y git python3-dev libsmpeg0 \
    flac libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential \
    libssl-dev libffi-dev libatlas3-base mplayer libyaml-dev libpython3-dev libjpeg-dev
    sudo apt-get install -y libportaudio0 libportaudio2 libportaudiocpp0  \
    apt-transport-https pulseaudio
    echo_green "Installing system packages...[OK]"

}

install_python3(){
     sudo apt-get install build-essential tk-dev libncurses5-dev libncursesw5-dev libreadline6-dev libdb5.3-dev \
     libgdbm-dev libsqlite3-dev libssl-dev libbz2-dev libexpat1-dev liblzma-dev zlib1g-dev libffi-dev -y

     wget https://www.python.org/ftp/python/${python_version}/Python-${python_version}.tar.xz
     tar xf Python-${python_version}.tar.xz
     cd Python-${python_version}
     ./configure
     make -j 4
     sudo make altinstall
     echo_green "Installing python3... [OK]"
}

install_pip3(){
    echo_green "Installing python pip..."
    sudo apt-get install -y python3-distutils
    wget https://bootstrap.pypa.io/get-pip.py
    sudo python3 get-pip.py
    echo_green "Installing python pip... [OK]"
}

install_pico2wave(){
    debian_version=`cat /etc/os-release |grep buster`
    retVal=$?
    if [[ ${retVal} -ne 0 ]]; then
        echo "Debian < 10"
        sudo apt-get install ffmpeg libttspico-utils
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
}

install_kalliope(){
    if [[ -d "kalliope" ]]; then
        echo_green "Source folder already cloned"
    else
        echo_yellow "Cloning the project"
        # clone the project
        git clone https://github.com/kalliope-project/kalliope.git
        echo_green "Cloning the project...[OK]"
    fi
    # Install the project
    echo_yellow "Installing Kalliope..."
    # fix for last ansible
#    sudo pip3 install "ansible==2.9.5"
    cd kalliope
    git checkout ${branch}
    sudo python3 setup.py install
    cd ..
    echo_green "Installing Kalliope...[OK]"
}

setup_pulseaudio(){
    # Get the current user
    current_user=$(logname)

    # Check if default-server already exists in client.conf
    if grep -Fxq "default-server = /var/run/pulse/native" /etc/pulse/client.conf; then
        echo_yellow '"default-server = /var/run/pulse/native" already in /etc/pulse/client.conf'
    else
        # If not, we add it to /etc/pulse/client.conf
        echo_green "Adding default-server to /etc/pulse/client.conf..[OK]"
        echo "default-server = /var/run/pulse/native" | sudo tee -a /etc/pulse/client.conf >/dev/null
    fi

    # Check if autospawn already exists in client.conf
    if grep -Fxq "autospawn = no" /etc/pulse/client.conf; then
        echo_yellow '"autospawn = no" already in /etc/pulse/client.conf'
    else
        # If not, we add it to /etc/pulse/client.conf
        echo_green "Adding 'autospawn = no' to /etc/pulse/client.conf..[OK]"
        echo 'autospawn = no' | sudo tee -a /etc/pulse/client.conf >/dev/null
    fi

    # The Pi users needs to be in pulse-access group, check if already a member
    if id -nG "$current_user" | grep -qw "pulse-access"; then
        echo_yellow "$current_user is already a member of the group pulse-access"
    else
        # If not, then we add it to pulse-access
        echo_green "Adding user $current_user to group pulse-access"
        sudo usermod -a -G pulse-access $current_user
    fi

    # Check if alsa-sink already exists in system.pa
    if grep -Fxq 'load-module module-alsa-sink device="hw:0,0"' /etc/pulse/system.pa; then
        echo_yellow '"load-module module-alsa-sink" already in /etc/pulse/system.pa'
    else
        # If not, we add it to /etc/pulse/system.pa
        echo_green "Adding 'load-module module-alsa-sink device="hw:0,0"' to /etc/pulse/system.pa..[OK]"
        echo 'load-module module-alsa-sink device="hw:0,0"' | sudo tee -a /etc/pulse/system.pa >/dev/null
    fi

    # Check if alsa_output.hw_0_0 is already set as default in system.pa
    if grep -Fxq 'set-default-sink alsa_output.hw_0_0' /etc/pulse/system.pa; then
        echo_yellow '"set-default-sink alsa_output.hw_0_0" already in /etc/pulse/system.pa'
    else
        # If not, we add it to /etc/pulse/system.pa
        echo_green "Adding 'set-default-sink alsa_output.hw_0_0' to /etc/pulse/system.pa..[OK]"
        echo 'set-default-sink alsa_output.hw_0_0' | sudo tee -a /etc/pulse/system.pa >/dev/null
    fi

    # We comment out load-module module-suspend-on-idle in /etc/pulse/system.pa to avoid a delay if the module is suspend
    sudo sed -e '/load-module module-suspend-on-idle/ s/^#*/#/' -i /etc/pulse/system.pa
    
    if [[ -f "/etc/systemd/system/pulseaudio.service" ]]; then
        # If the service already exists, we can skip this step
        echo_green "Pulseaudio service already existing"
    else
        echo_yellow "Create pulseaudio service"
        # Copy the pulseaudio service to /etc/systemd/system/
        sudo cp $(pwd)/kalliope/install/files/pulseaudio.service /etc/systemd/system/
        echo_green "Creating pulseaudio service..[OK]"
        sudo systemctl daemon-reload
        sudo systemctl start pulseaudio
        sudo systemctl enable pulseaudio
        echo_green "Enable and starting pulseaudio.service..[OK]"
    fi
    echo_green "Installing pulseaudio service..[OK]"
}


#------------------------------------------
# Main
#------------------------------------------
# get the branch name to install from passed arguments if exist
if [[ $# -eq 0 ]]
  then
    echo "No arguments supplied. Master branch will be installed"
else
    branch=$1
    echo "Selected branch name to install: ${branch}"
fi

## install packages
install_default_packages

if command -v python3 &>/dev/null; then
    echo_green "Python 3 is installed"
else
    echo_yellow "Python 3 is not installed"
    install_python3
fi

if command -v pip3 &>/dev/null; then
    echo_green "Pip 3 is installed"
else
    echo_yellow "Pip 3 is not installed"
    install_pip3
fi

if command -v pico2wave &>/dev/null; then
    echo_green "Pico2wave is installed"
else
    echo_yellow "Pico2wave is not installed"
    install_pico2wave
fi

install_kalliope
setup_pulseaudio

# fix https://github.com/kalliope-project/kalliope/issues/487
#sudo chmod -R o+r /usr/local/lib/python3.7/dist-packages/
