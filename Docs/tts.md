# Text to speech (TTS)

This chapter describes how TTS engine works.

The TTS is a programs or API that converts a text into a speech.
Each TTS has a specific configuration and supports multiple voices and/or languages.

The configuration of each TTS you use must appear in the [settings.yml](settings.md) file.


## Settings

### default_text_to_speech

The `setting.yml` defines the STT you want to use by default
```
default_text_to_speech: "type default TTS engine name here"
```

### text_to_speech

Still in the `settings.yml` file, each TTS must set up its configuration following the 'text_to_speech' tag :
```
text_to_speech:
   - TTS1:
      TTS1parameter1: "value option1"
      TTS1parameter2: "value option2"
   - TTS2:
      TTS2parameter1: "value option1"
```
Click on a TTS engine link in the `Current Available TTS` section to know which parameter are required.


### cache_path

TTS engines work all the same, we give them a text, they give back an audio file and we play the audio file. The generated audio file is placed in cache until it 
is played by the audio player. Before generating a new audio file, Kalliope will take a look to the cache to load it directly without having to call the 
TSS engine if the file has been generated before.

You must set a path where the cache will be saved in the tag `cache_path`. This one is placed in /tmp by default.
```
cache_path: "/tmp/kalliope_tts_cache"
```

>**Note:** The path must be a valid path, and the current user must has enough right to read and write in it.

>**Note:** The cache can be enabled or disabled by a neuron. See the [neuron documentation](neurons.md).

>**Note:** The consumed disk space can dramatically increase in the cache path folder. It is recommended to set your neuron correctly to clean up automatically
generated audio files that will not be played more than once.

## Current Available TTS
Core TTSs are already packaged with the installation of Kalliope an can be used out of the box.

- [acapela](../kalliope/tts/acapela/README.md)
- [googletts](../kalliope/tts/googletts/README.md)
- [pico2wave](../kalliope/tts/pico2wave/README.md)
- [voicerss](../kalliope/tts/voicerss/README.md)
- [voxygen](../kalliope/tts/voxygen/README.md)

## TTS Community Installation

Community TTSs need to be installed manually.

Use the CLI
```
kalliope install --git-url <git_url>
```

You may be prompted to type your `sudo` password during the process. You can see the list of [available TTS here](tts_list.md)

## Full Example

```
default_text_to_speech: "voicerss"

cache_path: "/tmp/kalliope_tts_cache"

text_to_speech:
  - pico2wave:
      language: "fr-FR"
      cache: True
  - voxygen:
      voice: "Agnes"
      cache: True
  - acapela:
      language: "sonid15"
      voice: "Manon"
      cache: True
  - googletts:
      language: "fr"
      cache: True
  - voicerss:
      language: "fr-fr"
      cache: True
```
