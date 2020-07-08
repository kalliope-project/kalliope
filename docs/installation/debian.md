# Kalliope requirements for Debian Jessie/Stretch

## Debian packages requirements

Edit `/etc/apt/sources.list` and check that you have `contrib` and `non-free` are enabled:

On Debian Jessie:
```bash
deb http://httpredir.debian.org/debian jessie main contrib non-free
deb-src http://httpredir.debian.org/debian jessie main contrib non-free
```

On Debian Stretch:
```bash
deb http://httpredir.debian.org/debian stretch main contrib non-free
deb-src http://httpredir.debian.org/debian stretch main contrib non-free
```

Install some required system libraries and softwares:

```bash
sudo apt-get update
sudo apt-get install -y \
    git python3-dev libpython3-dev libsmpeg0 libttspico-utils flac \
    libffi-dev libssl-dev portaudio19-dev build-essential \
    libatlas3-base mplayer wget vim sudo locales \
    pulseaudio-utils libasound2-plugins python3-pyaudio libasound-dev \
    libportaudio2 libportaudiocpp0 ffmpeg
```

Let's install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python3 get-pip.py
```

Then, with pip, the last release of setuptools
```bash
sudo pip3 install -U setuptools
```
## Kalliope installation

{!installation/manual_installation_common.md!}

{!installation/check_env.md!}
