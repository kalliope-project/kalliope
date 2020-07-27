# Kalliope requirements for Ubuntu

## Pre requisite

### Ubuntu 18.04

Install some required system libraries and software:

```bash
sudo apt update
sudo apt install -y \
    git python3-dev python3.7-dev libsmpeg0 libttspico-utils flac \
    libffi-dev libssl-dev portaudio19-dev build-essential \
    libatlas3-base mplayer wget vim sudo locales alsa-base alsa-utils \
    pulseaudio-utils libasound2-plugins python3-pyaudio libasound-dev \
    libportaudio2 libportaudiocpp0 ffmpeg 
```

### Ubuntu 20.04

Install some required system libraries and software:

```bash
sudo apt update
sudo apt install -y \
    git python3-dev libsmpeg0 libttspico-utils flac \
    libffi-dev libssl-dev portaudio19-dev build-essential \
    libatlas3-base mplayer wget vim sudo locales alsa-base alsa-utils \
    pulseaudio-utils libasound2-plugins python3-pyaudio libasound-dev \
    libportaudio2 libportaudiocpp0 ffmpeg 
```

## Install lasted version of the python package manager

Install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

## Kalliope installation

{!installation/manual_installation_common.md!}

{!installation/check_env.md!}
