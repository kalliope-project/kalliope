# JARVIS settings

This part of the documentation deals with the main configuration of JARVIS. 
This configuration is a file placed at the root of the project tree and called settings.yml.

The syntax used is YAML.

# General defaults

In the settings.yml, the following settings are tunable:

#### trigger

The current hotword(also called a wake word or trigger word) detector is based on [Snowboy](https://snowboy.kitt.ai/).
Common usage of hotword include Alexa on Amazon Echo, OK Google on some Android devices and Hey Siri on iPhones.
With JARVIS project, you can set the Hotword you want. You can create your magic word by connecting to [Snowboy](https://snowboy.kitt.ai/) 
and then download the trained model file.

Once downloaded, place the file in **trigger/snowboy/resources**.

Then, specify the name of the Snowboy model use the following syntax
```
trigger:
  name: "my_model_name.pmdl"
```

#### default_speech_to_text

A Speech To Text(STT) is an engine used to translate what you say into a text that can be processed by JARVIS core. 
By default, JARVIS use google STT engine.

You must provide an engine name in this variable following the syntax bellow
```
default_speech_to_text: "stt_name"
```

Available STT for JARVIS are:
- google
- bing

#### default_text_to_speech
A Text To Speech is an engine used to translate written text into a speech, into an audio stream.
By default, JARVIS use Pico2wave TTS engine.

You must provide a TTS engine name in this variable following the syntax bellow
```
default_text_to_speech: "tts_name"
```

Available TTS for JARVIS are:
- pico2wave
- voxygen

#### random_wake_up_answers
When JARVIS detects your trigger/hotword/magic word, he lets you know that he's operational and now waiting for order by answering randomly 
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

Some arguments are required, some other optional, please refer to the STT documentation to know available parameters for each supported STT.


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

Some arguments are required, some other optional, please refer to the TTS documentation to know available parameters for each supported TTS.
