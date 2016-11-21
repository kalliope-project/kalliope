# Kalliope installation on Debian Jessie

## Install system dependencies

Edit `/etc/apt/sources.list` and check that your mirror accept "non-free" package
```
deb http://ftp.fr.debian.org/debian/ jessie main contrib non-free
deb-src http://ftp.fr.debian.org/debian/ jessie main contrib non-free
```

To make Kalliope work, you will have to install a certain number of libraries:
```
sudo apt-get update
sudo apt-get install git python-pip python-dev python-virtualenv libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer
```

## User install

WIP: The step above will be replace by a simple `pip install kalliope` soon.

Clone the project
```
git clone https://github.com/kalliope-project/kalliope.git
```

Install kalliope
```
sudo python setup.py build
sudo python setup.py install
```

## Developer install

Clone the project
```
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope/
virtualenv venv
venv/bin/pip install --editable .
venv/bin/kalliope start
```

## Test your env

To ensure that you can record your voice, run the following command to capture audio input from your microphone
```
rec test.wav
```

Press CTRL-C after capturing a sample of your voice.

Then play the recorded audio file
```
mplayer test.wav
```

If everything is ok, you can start playing with Kalliope. First, take a look to the [default settings](settings.md).
