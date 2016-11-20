# Kalliope installation on Raspbian

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

# Raspberry Pi configuration

This documentation deals with the special configuration needed for get kalliope working on a RPi.

## Packages

On a Raspberry Pi, pulseaudio is not installed by default
```
sudo apt-get install pulseaudio pulseaudio-utils
```

Start the pulseaudio server
```
pulseaudio -D
```

## Microphone configuration

Get your output card
```
aplay -l
```

Output example with a USB headset connected
```
**** List of PLAYBACK Hardware Devices ****
card 0: ALSA [bcm2835 ALSA], device 0: bcm2835 ALSA [bcm2835 ALSA]
  Subdevices: 7/8
  Subdevice #0: subdevice #0
  Subdevice #1: subdevice #1
  Subdevice #2: subdevice #2
  Subdevice #3: subdevice #3
  Subdevice #4: subdevice #4
  Subdevice #5: subdevice #5
  Subdevice #6: subdevice #6
  Subdevice #7: subdevice #7
card 0: ALSA [bcm2835 ALSA], device 1: bcm2835 ALSA [bcm2835 IEC958/HDMI]
  Subdevices: 1/1
  Subdevice #0: subdevice #0
card 1: Headset [Logitech USB Headset], device 0: USB Audio [USB Audio]
  Subdevices: 0/1
  Subdevice #0: subdevice #0
```

Here, we can see that we have 
- the analog audio (where the jack is connected) on the card 0 and device 1
- usb audio on card 1 and device 1


Get your input (microphone card)
```
arecord -l
```

Output example with a USB headset connected
```
**** List of CAPTURE Hardware Devices ****
card 1: Headset [Logitech USB Headset], device 0: USB Audio [USB Audio]
  Subdevices: 0/1
  Subdevice #0: subdevice #0
```

Here we can see that we have one peripheral on card 1 and device 0

Now, we create a configuration file that will do apply the following configuration:
- output audio (what Kalliope say) on the analog audio (via speakers connected to the jack)
- input audio (what we say to Kalliope) on the USB microphone

Create a file in `/home/pi/.asoundrc` with the content bellow
```
pcm.!default {
   type asym
   playback.pcm {
     type plug
     slave.pcm "hw:1,0"
   }
   capture.pcm {
     type plug
     slave.pcm "hw:1,0"
   }
}
```

Where `playback.pcm` is the output audio and the `capture.pcm` is the input audio.

Restart alsa to apply changes
```
sudo /etc/init.d/alsa-utils restart
```

You can adjust the microphone sensibility by running alsamixer:
```
alsamixer
```
And then select your microphone device by pressing F6 and finally move up the `mic` sensibility level
![logo](../../images/alsamixer_mic_level.png)

To ensure that you can record your voice, run the following command to capture audio input from your microphone
```
rec test.wav
```

Press CTRL-C after capturing a sample of your voice.

Then play the recorded audio file
```
mplayer test.wav
```


## HDMI / Analog audio

By default the audio stream will get out by HDMI if something is plugged to this port.
Check the [official documentation](https://www.raspberrypi.org/documentation/configuration/audio-config.md) to switch from HDMI to analog.

```
sudo raspi-config
```
