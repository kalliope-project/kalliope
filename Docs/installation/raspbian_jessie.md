# Kalliope requirements for Raspbian

## Install the pre-compiled disk image

Download the last image [from the release page](https://github.com/kalliope-project/kalliope/releases) of Kalliope and load it as usual into your SD card.

**Login:** pi
**Password:** raspberry

Once installed, use the `raspi-config` command to expend the file system and fill the whole available space on your SD card.
The SSH server is already active. You only need to get the ip of your Rpi via the command `ip a` and then connect via your favourite SSH client.
We placed in `/home/pi` the two starter config we made for [French](https://github.com/kalliope-project/kalliope_starter_fr) and [English](https://github.com/kalliope-project/kalliope_starter_en). 

## Manual installation

Supported Raspbian images:
[raspbian-2016-09-28](http://downloads.raspberrypi.org/raspbian/images/raspbian-2016-09-28/)
[raspbian-2016-11-29](http://downloads.raspberrypi.org/raspbian/images/raspbian-2016-11-29/)
[raspbian-2017-01-10](http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-01-10/)

> **Note:** We recommend to use a **lite** installation of Raspbian without any graphical interface for a better experience. 

> **Note:** The first Raspberry Pi is not officially supported. The installation will works but a single core with only 700Mhz may produce a some latencies.

### Debian packages requirements

Install some required system libraries and software:

```bash
sudo apt-get update
sudo apt-get install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer libyaml-dev libpython2.7-dev libav-tools
```

Let's install the last release of python-pip
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

On a Raspberry Pi, pulseaudio is not installed by default
```bash
sudo apt-get install pulseaudio pulseaudio-utils
```

Start the pulseaudio server
```bash
pulseaudio -D
```

## Raspberry Pi configuration

This part deals with the special configuration needed to get kalliope working on a RPi.

### Microphone configuration

Get your output card
```bash
aplay -l
```

Output example with a USB headset connected
```bash
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
```bash
arecord -l
```

Output example with a USB headset connected
```bash
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
```bash
sudo /etc/init.d/alsa-utils restart
```

You can adjust the microphone sensibility by running alsamixer:
```bash
alsamixer
```
And then select your microphone device by pressing F6 and finally move up the `mic` sensibility level
![logo](../../images/alsamixer_mic_level.png)

To ensure that you can record your voice, run the following command to capture audio input from your microphone
```bash
rec test.wav
```

Press CTRL-C after capturing a sample of your voice.

Then play the recorded audio file
```bash
mplayer test.wav
```


### HDMI / Analog audio

By default the audio stream will get out by HDMI if something is plugged to this port.
Check the [official documentation](https://www.raspberrypi.org/documentation/configuration/audio-config.md) to switch from HDMI to analog.

```bash
sudo raspi-config
```

Then, follow the [main installation documentation](../installation.md).
