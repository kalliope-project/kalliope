# Kalliope installation on Ubuntu 16.04

## Automated install

Clone the project
```
cd
git clone https://github.com/kalliope-project/kalliope.git
```

Run the install script.
```
./kalliope/install/install_kalliope.sh
```

## Manual install

To make Kalliope work, you will have to install a certain number of libraries:
```
sudo apt-get update
sudo apt-get install git python-pip python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer
```

Clone the project
```
git clone https://github.com/kalliope-project/kalliope.git
```

Install libs
```
sudo pip install -r install/files/python_requirements.txt
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

If everything is ok, you can start playing with Kalliope. First, take a look to the [default settings](../settings.md).
