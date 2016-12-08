# Kalliope requirements for Debian Jessie

## Debian packages requirements

Edit `/etc/apt/sources.list` and check that you have `contrib` and `non-free` and backports archives enabled:
```
deb http://httpredir.debian.org/debian jessie main contrib non-free
deb-src http://httpredir.debian.org/debian jessie main contrib non-free
deb http://httpredir.debian.org/debian jessie-backports main contrib non-free
deb-src http://httpredir.debian.org/debian jessie-backports main contrib non-free
```

Install some required system libraries and softwares:

```
sudo apt-get update
sudo apt-get install git python-pip python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer
```

You also need some packages from the backports:

```
sudo apt-get install -t jessie-backports python-setuptools
sudo apt-get install -t jessie-backports python-pyasn1
```
