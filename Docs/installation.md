# Kalliope installation

## Prerequisites

Please follow the right link bellow to install requirements depending on your target environment:
- [Raspbian (Raspberry Pi 2 & 3)](installation/raspbian_jessie.md)
- [Ubuntu 14.04](installation/ubuntu_14.04.md)
- [Ubuntu 16.04](installation/ubuntu_16.04.md)
- [Debian Jessie](installation/debian_jessie.md)

## Installation

### Method 1 - User install using the PIP package

You can install kalliope on your system by using Pypi:
```bash
sudo pip install kalliope
```

### Method 2 - Manual setup using sources

Clone the project:
```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the project:
```bash
sudo python setup.py install
```

### Method 3 - Developer install using Virtualenv

Install the `python-virtualenv` package:
```bash
sudo apt-get install python-virtualenv
```

Clone the project:
```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Generate a local python environment:
```bash
virtualenv venv
```

Install the project using the local environment:
```bash
venv/bin/pip install --editable .
```

### Method 4 - Developer, dependencies install only

Clone the project:
```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the python dependencies directly:
```bash
sudo pip install -r install/python_requirements.txt
```

## Test your env

To ensure that you can record your voice, run the following command to capture audio input from your microphone:
```bash
rec test.wav
```

Press CTRL-C after capturing a sample of your voice.

Then play the recorded audio file
```bash
mplayer test.wav
```

You can then test that your Kalliope is working by using the "bonjour" order integrated in the [default brain](../kalliope/brain.yml).
Start kalliope:
```bash
kalliope start
```

> **Note:** Do not start Kalliope as root user or with sudo

Kalliope will load default settings and brain, the output should looks the following
```bash
Starting event manager
Events loaded
Starting Kalliope
Press Ctrl+C for stopping
Starting REST API Listening port: 5000
```

Then speak the hotwork out loud to wake up Kalliope. By default, the hotwork is "Kalliopé" with the french pronunciation.
If the trigger is successfully raised, you'll see "say something" into the console. 
```bash
2016-12-05 20:54:21,950 :: INFO :: Keyword 1 detected at time: 2016-12-05 20:54:21
Say something!
```

Then you can say "bonjour" and listen the Kalliope response.
```bash
Say something!
Google Speech Recognition thinks you said Bonjour
Order matched in the brain. Running synapse "say-hello-fr"
Waiting for trigger detection
```

## Get a starter configuration
We create some starter configuration that only need to be downloaded and then started. 
Those repositories provide you a basic structure to start playing with kalliope. We recommend you to clone one of them and then go to the next section.

- [French starter config](https://github.com/kalliope-project/kalliope_starter_fr)
- [English starter config](https://github.com/kalliope-project/kalliope_starter_en)


## Next: Create you own bot
If everything is ok, you can start playing with Kalliope. First, take a look to the [default settings](settings.md).
