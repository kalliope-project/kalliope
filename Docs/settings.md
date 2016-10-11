# Kalliope settings

This part of the documentation deals with the main configuration of Kalliope. 
This configuration is a file placed at the root of the project tree and called settings.yml.

The syntax used is YAML.

# General defaults

In the settings.yml, the following settings are tunable:

#### default_trigger

The trigger is the module in charge detecting the hotword that wake up Kalliope.
Common usage of hotword include Alexa on Amazon Echo, OK Google on some Android devices and Hey Siri on iPhones.

Specify the name of the trigger module you want to use.
```
default_trigger: "trigger_name"
```

Available trigger for Kalliope are:
- snowboy

#### default_speech_to_text

A Speech To Text(STT) is an engine used to translate what you say into a text that can be processed by Kalliope core. 
By default, Kalliope use google STT engine.

You must provide an engine name in this variable following the syntax bellow
```
default_speech_to_text: "stt_name"
```

E.g
```
default_speech_to_text: "snowboy"
```

Get the full list of [SST engine here](stt.md).

#### default_text_to_speech
A Text To Speech is an engine used to translate written text into a speech, into an audio stream.
By default, Kalliope use Pico2wave TTS engine.

You must provide a TTS engine name in this variable following the syntax bellow
```
default_text_to_speech: "tts_name"
```

Eg
```
default_text_to_speech: "pico2wave"
```

Get the full list of [TTS engine here](tts.md).

#### random_wake_up_answers
When Kalliope detects your trigger/hotword/magic word, she lets you know that he's operational and now waiting for order by answering randomly 
one of the sentences provided in the variable random_wake_up_answers.

This variable must contain a list of string following the syntax bellow
```
random_wake_up_answers:
  - "You sentence"
  - "Another sentence"
```

E.g
```
random_wake_up_answers:
  - "Yes sir?"
  - "I'm listening"
  - "Sir?"
  - "What can I do for you?"
  - "Listening"
  - "Yes?"
```

#### random_wake_up_sounds
You can play a sound when Kalliope detect the hotword/trigger instead of saying something from
the `random_wake_up_answers`.
Place here a list of full path of the sound file or just the name of the file in `/usr/lib/kalliope/sounds`
The file must be .wav or .mp3 format. By default two file are provided: ding.wav and dong.wav. Of more than on file is present in the list,
Kalliope will select one randomly at each wake up.

```
random_wake_up_sounds:
  - "local_file_in_sounds_folder.wav" 
  - "/my/personal/full/path/my_file.mp3"
```

E.g
```
random_wake_up_sounds:
  - "ding.wav"
  - "dong.wav"
  - "/my/personal/full/path/my_file.mp3"
```

>**Note: ** If you want to use a wake up sound instead of a wake up answer you must comment out the `random_wake_up_answers` section.
E.g: `# random_wake_up_answers:`

#### speech_to_text
Speech to text configuration.
Each STT has it own configuration. This configuration is passed as argument following the syntax bellow
```
speech_to_text:
  - stt_name:
      parameter_name: "value"
```      

E.g:
```
speech_to_text:
  - google:
      language: "fr-FR"
  - bing
```

Some arguments are required, some other optional, please refer to the [STT documentation](stt.md) to know available parameters for each supported STT.


#### text_to_speech
Text to speech configuration
Each TTS has it own configuration. This configuration is passed as argument following the syntax bellow
```
text_to_speech:
  - tts_name:
      parameter_name: "value"
```

E.g
```
text_to_speech:
  - pico2wave:
      language: "fr-FR"
  - voxygen:
      language: "fr"
      voice: "michel"
```

Some arguments are required, some other optional, please refer to the [TTS documentation](tts.md) to know available parameters for each supported TTS.

#### triggers
The default hotword (also called a wake word or trigger word) detector is based on [Snowboy](https://snowboy.kitt.ai/).

Each Trigger has it own configuration. This configuration is passed as argument following the syntax bellow
```
triggers:
  - trigger_name:
      parameter_name: "value"
```

E.g, the default Snowboy trigger configuration is
```
triggers:
  - snowboy:
      pmdl_file: "trigger/snowboy/resources/model.pmdl"
```
