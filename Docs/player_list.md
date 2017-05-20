# List of available Player

A player is a module that Kalliope will use when playing a sound generated from a TTS engine.
You can define them in your [settings.yml file](settings.md). 

## Core Players
Core Players are already packaged with the installation of Kalliope an can be used out of the box.

|        Name       | Description                                                                    | Note                |
|-------------------|--------------------------------------------------------------------------------|---------------------|
| mplayer           | [mplayer](http://www.mplayerhq.hu/design7/news.html)                           |                     |
| AlsaAudioPlayer   | [AlsaAudioPlayer](https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html) | Does not handle mp3 |
| PyAudioPlayer     | [PyAudioPlayer](https://people.csail.mit.edu/hubert/pyaudio/)                  | Does not handle mp3 |
| SoundDevicePlayer | [SoundDevicePlayer](https://pypi.python.org/pypi/sounddevice)                  | Does not handle mp3 |

## Community Players
Community Players need to be installed manually.

Wanna add your Player in the list? Open [an issue](../../issues) and send a pull request to update the list directly.

