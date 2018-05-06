# Kalliope requirements for Ubuntu 16.04

## Debian packages requirements

Install some required system libraries and softwares:

```bash
sudo apt-get update
sudo apt-get install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer libav-tools
```
Let's install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

Then, follow the [main installation documentation](../installation.md).
