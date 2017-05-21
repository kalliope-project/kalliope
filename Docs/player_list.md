# List of available Player

A player is a module that Kalliope will use when playing a sound generated from a TTS engine.
You can define them in your [settings.yml file](settings.md). 

## Core Players
Core Players are already packaged with the installation of Kalliope an can be used out of the box.

| Name              | Description                                                          | Note                                                                                    |
|-------------------|----------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| mplayer           | [mplayer](../kalliope/players/mplayer/README.md)                     | Based on [mplayer software](http://www.mplayerhq.hu/design7/news.html)                  |
| pyalsaaudio       | [AlsaAudioPlayer](../kalliope/players/pyalsaaudio/README.md)         | Based on [pyalsaaudio](https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html) lib |
| pyaudioplayer     | [PyAudioPlayer](../kalliope/players/pyaudioplayer/README.md)         | Based on [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/docs/) lib               |
| sounddeviceplayer | [SoundDevicePlayer](../kalliope/players/sounddeviceplayer/README.md) | Based on [sounddevice](https://pypi.python.org/pypi/sounddevice) lib                    |

## Community Players
Community Players need to be installed manually.

Wanna add your Player in the list? Open [an issue](../../issues) and send a pull request to update the list directly.

