# Kalliope installation on Ubuntu 16.04

## Requirements

### Debian packages requirements

Install some required system libraries and softwares:

```
sudo apt-get update
sudo apt-get install git python-pip python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer
```

## Installation

### Method 1 - User install using the PIP package

You can install kalliope on your system:
```
sudo pip install kalliope
```

Or just in your user home:
```
pip install --user kalliope
```

Run Kalliope:
```
kalliope start
```

### Method 2 - Manual user install using the git repository

Clone the project:
```
git clone https://github.com/kalliope-project/kalliope.git
```

Install the project:
```
sudo python setup.py install
```

Run Kalliope from a shell:
```
kalliope start
```

### Method 3 - Developer install using Virtualenv

Install the `python-virtualenv` package:
```
sudo apt-get install python-virtualenv
```

Clone the project:
```
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Generate a local python environment:
```
virtualenv venv
```

Install the project using the local environment:
```
venv/bin/pip install --editable .
```

Run Kalliope from a shell:
```
venv/bin/kalliope start
```

### Method 4 - Developer, dependencies install only

Clone the project:
```
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the python dependencies directly:
```
sudo pip install -r install/python_requirements.txt
```

Run Kalliope from a shell directly:
```
python kalliope.py start
```

## Test your env

To ensure that you can record your voice, run the following command to capture audio input from your microphone:
```
rec test.wav
```

Press CTRL-C after capturing a sample of your voice.

Then play the recorded audio file
```
mplayer test.wav
```

If everything is ok, you can start playing with Kalliope. First, take a look to the [default settings](../settings.md).
