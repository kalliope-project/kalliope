# Kalliope requirements for Raspbian

## Install the pre-compiled disk image

Download the last image [from the release page](https://github.com/kalliope-project/kalliope/releases) of Kalliope and load it as usual onto an SD card.

**Login:** pi
**Password:** raspberry

Once installed, use the `raspi-config` command to expand the file system and fill the available space on the SD card.
The SSH server is enable by default. Get the IP of your Rpi via the command `ip a` and then connect via your favourite SSH client.
The two starter config files are located in `/home/pi` for [French](https://github.com/kalliope-project/kalliope_starter_fr), [English](https://github.com/kalliope-project/kalliope_starter_en) and [German](https://github.com/kalliope-project/kalliope_starter_de).

## Manual installation

Supported Raspbian images:
[raspbian-2016-09-28](http://downloads.raspberrypi.org/raspbian/images/raspbian-2016-09-28/)
[raspbian-2016-11-29](http://downloads.raspberrypi.org/raspbian/images/raspbian-2016-11-29/)
[raspbian-2017-01-10](http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-01-10/)
[raspbian-2017-04-10](http://downloads.raspberrypi.org/raspbian/images/raspbian-2017-04-10/)

> **Note:** It is recommended to use a **lite** installation of Raspbian without any graphical interface for a better experience. 

> **Note:** The first Raspberry Pi is not officially supported. The installation will works but a single core with only 700Mhz may produce latency.

### Debian packages requirements

Install the required system libraries and software:

```bash
sudo apt-get update
sudo apt-get install git python-dev libsmpeg0 libttspico-utils libsmpeg0 flac dialog libffi-dev libffi-dev libssl-dev portaudio19-dev build-essential libssl-dev libffi-dev sox libatlas3-base mplayer libyaml-dev libpython2.7-dev libav-tools
```

Install the last release of python-pip:
```bash
wget https://bootstrap.pypa.io/get-pip.py
sudo python get-pip.py
```

On a Raspberry Pi, pulseaudio is not installed by default:
```bash
sudo apt-get install pulseaudio pulseaudio-utils
```

Start the pulseaudio server:
```bash
pulseaudio -D
```

## Raspberry Pi configuration

This section deals with the special configuration needed to get kalliope working on a RPi.

### Microphone configuration

Get the output card:
```bash
aplay -l
```

Output example with a USB headset connected:
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

Here one shall see: 
- the analog audio (where the jack is connected) on card 0 and device 1
- usb audio on card 1 and device 1


Get the input (microphone card):
```bash
arecord -l
```

Output example with a USB headset connected:
```bash
**** List of CAPTURE Hardware Devices ****
card 1: Headset [Logitech USB Headset], device 0: USB Audio [USB Audio]
  Subdevices: 0/1
  Subdevice #0: subdevice #0
```

Here one shall see one peripheral on card 1 and device 0

Create a configuration file that applies the following configuration:
- output audio (what Kalliope says) on the analog audio (via speakers connected to the jack)
- input audio (what is said to Kalliope) on the USB microphone

Create a file in `/home/pi/.asoundrc` with the content below
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

Restart alsa to apply changes:
```bash
sudo /etc/init.d/alsa-utils restart
```

Adjust the microphone sensibility by running alsamixer:
```bash
alsamixer
```

Select the microphone device by pressing F6 and move up the `mic` sensibility level:
![logo](../../images/alsamixer_mic_level.png)

To ensure voice recording, run the following command to capture audio input from the microphone:
```bash
rec test.wav
```

Press CTRL-C after capturing a voice sample.

Play the recorded audio file:
```bash
mplayer test.wav
```


### HDMI / Analog audio

By default, the audio stream will use HDMI if something is plugged into this port.
Check the [official documentation](https://www.raspberrypi.org/documentation/configuration/audio-config.md) to switch from HDMI to analog.

```bash
sudo raspi-config
```

Then follow the [main installation documentation](../installation.md).
