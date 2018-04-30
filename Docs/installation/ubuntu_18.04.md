# Kalliope requirements for Ubuntu 18.04

## Packages requirements

Install some required system libraries and software:

```bash
sudo apt update
sudo apt install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev sox libatlas3-base mplayer
```

Note, if you are using python 3,
```
sudo apt install python3-dev python3-dialog 
```


Install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

Then, follow the [main installation documentation](../installation.md).
