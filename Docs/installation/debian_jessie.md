# Kalliope requirements for Debian Jessie

## Debian packages requirements

Edit `/etc/apt/sources.list` and check that you have `contrib` and `non-free` are enabled:
```bash
deb http://httpredir.debian.org/debian jessie main contrib non-free
deb-src http://httpredir.debian.org/debian jessie main contrib non-free
```

Install some required system libraries and softwares:

```bash
sudo apt-get update
sudo apt-get install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer
```

Let's install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

Then, with pip, the last release of setuptools
```bash
sudo pip install -U setuptools
```

Then, follow the [main installation documentation](../installation.md).

