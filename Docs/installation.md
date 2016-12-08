# Kalliope installation

## Prerequisites

Please follow link bellow to install requirements depending on your target environment:
- [Raspbian (Raspberry Pi 2 & 3)](installation/raspbian_jessie.md)
- [Ubuntu 14.04/16.04](installation/ubuntu_16.04.md)
- [Debian Jessie](installation/debian_jessie.md)

## Installation

### Method 1 - User install using the PIP package

You can install kalliope on your system by using Pypi:
```
sudo pip install kalliope
```

### Method 2 - Manual setup using sources

Clone the project:
```
git clone https://github.com/kalliope-project/kalliope.git
```

Install the project:
```
sudo python setup.py install
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

You can then test your Kalliope is working by using the "bonjour" order integrated in the [default brain](../kalliope/brain.yml).
Start kalliope:
```
kalliope start
```

Kalliope will load default settings and brain, the output should looks the following
```
Starting event manager
Events loaded
Starting Kalliope
Press Ctrl+C for stopping
Starting REST API Listening port: 5000
```

Then speak the hotwork out loud to wake up Kalliope. By default, the hotwork is "Kalliopé" with the french pronunciation.
If the trigger is successfully raised, you'll see "say something" into the console. 
```
2016-12-05 20:54:21,950 :: INFO :: Keyword 1 detected at time: 2016-12-05 20:54:21
Say something!
```

Then you can say "bonjour" and listen the Kalliope response.
```
Say something!
Google Speech Recognition thinks you said Bonjour
Order matched in the brain. Running synapse "say-hello-fr"
Waiting for trigger detection
```

## Next: Create you own bot
If everything is ok, you can start playing with Kalliope. First, take a look to the [default settings](settings.md).
