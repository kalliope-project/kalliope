# Dev environment installation

This documentation aims at explaining the step by step manual deployment of Kalliope.

Tested env
- Ubuntu 16.04



## Prerequisite

### Packages installation
On Ubuntu distribution:
```
sudo apt-get install python-pip python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base
```

### Python lib

Install libs
```
pip install SpeechRecognition
pip install pyaudio
pip install ansible
pip install pygame
pip install python2-pythondialog
pip install jinja
pip install python-crontab
pip install cffi
pip install pygmail
pip install pushetta
pip install wakeonlan
pip install ipaddress
pip install pyowm
pip install flask
```

### Test your env
Run the following command to capture audio from your microphone
```
rec test.wav
```

Then play the recorded audio file
```
play test.wav
```

## Installation

Clone the project
```
git clone https://github.com/kalliope-project/kalliope.git
```

