# Kalliope requirements for Ubuntu

## Pre requisite

### Ubuntu 14.04

Install some required system libraries and softwares:

```bash
sudo apt-get update
sudo apt-get install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac libffi-dev libffi-dev libssl-dev libjack0 libjack-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer libav-tools
```

Recent version of GCC is needed
```bash
sudo add-apt-repository ppa:ubuntu-toolchain-r/test -y
sudo apt-get update -q
sudo apt-get install gcc-4.9
```

### Ubuntu 16.04

Install some required system libraries and softwares:

```bash
sudo apt-get update
sudo apt-get install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer libav-tools
```

### Ubuntu 18.04

Install some required system libraries and software:

```bash
sudo apt update
sudo apt install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev sox libatlas3-base mplayer
```

Note, if you are using python 3,
```
sudo apt install python3-dev python3-dialog
```

## Install lasted version of the python package manager

Install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

## Kalliope installation

{!installation/manual_installation_common.md!}

{!installation/check_env.md!}
