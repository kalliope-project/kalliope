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

Activate the local environment:
```bash
source venv/bin/activate
```

### Method 4 - Developer, dependencies install only

Clone the project:
```bash
git clone https://github.com/kalliope-project/kalliope.git
cd kalliope
```

Install the python dependencies directly:
```bash
sudo pip install -r install/files/python_requirements.txt
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

Your installation is now complete, let's take a look now to the [quickstart documentation](installation/quickstart.md) to learn how to use Kalliope.

## Get a starter configuration
We create some starter configuration that only need to be downloaded and then started. 
Those repositories provide you a basic structure to start playing with kalliope. We recommend you to clone one of them and then go to the next section.

- [French starter config](https://github.com/kalliope-project/kalliope_starter_fr)
- [English starter config](https://github.com/kalliope-project/kalliope_starter_en)
- [German starter config](https://github.com/kalliope-project/kalliope_starter_de)


## Start Kalliope automatically after a reboot

If you want to start Kalliope automatically Place the script bellow in `/etc/systemd/system/kalliope.service`.
Update the path to your folder where you've placed your `brain.yml` and `settings.yml`.
```bash
[Unit]
Description=Kalliope

[Service]
WorkingDirectory=/path/to/kalliope_brain_folder

Environment='STDOUT=/var/log/kalliope.log'
Environment='STDERR=/var/log/kalliope.err.log'
ExecStart=/bin/bash -c "/usr/local/bin/kalliope start > ${STDOUT} 2> ${STDERR}"
User=%i

[Install]
WantedBy=multi-user.target
```

Then, reload systemctl, start the service and enable it at startup
```bash
sudo systemctl daemon-reload
sudo systemctl start kalliope
sudo systemctl enable kalliope
```

## Next: 
If everything is ok, you can start playing with Kalliope. First, take a look to the [default settings](settings.md).
