# Kalliope requirements for Ubuntu 14.04

## Debian packages requirements

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

Let's install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

Then, follow the [main installation documentation](../installation.md).
