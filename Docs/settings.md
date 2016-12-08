# Kalliope settings

This part of the documentation explains the main configuration of Kalliope.

Kalliope need two file to works, a `settings.yml` and a `brain.yml`. Files are written on YAML syntax.

When you start kalliope using the CLI, the program will try to load your settings.yml and brain.yml in the following order:
- From you current folder, E.g `/home/pi/my_kalliope/settings.yml`
- From `/etc/kalliope/settings.yml`
- From the default `settings.yml`. You can take a look into the default [`settings.yml`](../kalliope/settings.yml) file which is located in the root of the project tree.

This a common tree of a Kalliope configuration folder:
```
kalliope_config/
├── brains
│   └── included_brain.yml
├── brain.yml
├── files
│   └── kalliope-FR-13samples.pmdl
└── settings.yml
```

## Triggers configuration

#### default_trigger

The trigger is the module detecting the hotword that will wake up Kalliope.
Common usage of hotword include Alexa on Amazon Echo, OK Google on some Android devices and Hey Siri on iPhones.

Specify the name of the trigger module you want to use.
```
default_trigger: "trigger_name"
```

Available triggers for Kalliope are:
- snowboy

#### triggers
The hotword (also called a wake word or trigger word) detector is the engine in charge of waking up Kalliope.

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

See the complete list of [available triggers here](trigger.md).

## Speech to text configuration

#### default_speech_to_text

A Speech To Text(STT) is an engine used to translate what you say into a text that can be processed by Kalliope core.
By default, Kalliope uses google STT engine.

The following syntax is used to provide the engine name:
```
default_speech_to_text: "stt_name"
```

E.g
```
default_speech_to_text: "google"
```

Get the full list of [SST engine here](stt.md).

#### speech_to_text
Each STT has it own configuration. This configuration is passed as argument as shown bellow
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

Some arguments are required, some others are optional, please refer to the [STT documentation](stt.md) to know available parameters for each supported STT.

## Text to speech configuration

#### default_text_to_speech
A Text To Speech is an engine used to translate written text into a speech, into an audio stream.
By default, Kalliope use Pico2wave TTS engine.

The following syntax is used to provide the TTS engine name
```
default_text_to_speech: "tts_name"
```

Eg
```
default_text_to_speech: "pico2wave"
```

Get the full list of [TTS engine here](tts.md).

#### text_to_speech
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
      voice: "michel"
```

Some arguments are required, some other optional, please refer to the [TTS documentation](tts.md) to know available parameters for each supported TTS.

## Wake up answers configuration

#### random_wake_up_answers
When Kalliope detects your trigger/hotword/magic word, it lets you know that it's operational and now waiting for order. It's done by answering randomly
one of the sentences provided in the variable random_wake_up_answers.

This variable must contain a list of strings as shownbellow
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
You can play a sound when Kalliope detects the hotword/trigger instead of saying something from
the `random_wake_up_answers`.
Place here a list of full paths of the sound files you want to use. Otherwise, you can use some default sounds provided by Kalliope which you can find in `/usr/lib/kalliope/sounds`.
By default two file are provided: ding.wav and dong.wav. In all cases, the file must be in `.wav` or `.mp3` format. If more than on file is present in the list,
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


## Rest API

A Rest API can be activated in order to:
- List synapses
- Get synapse's detail
- Run a synapse

For the complete API ref see the [REST API documentation](rest_api.md)

Settings examples:
```
rest_api:
  active: True
  port: 5000
  password_protected: True
  login: admin
  password: secret
```

#### active
To enable the rest api server.

#### port
The listening port of the web server. Must be an integer in range 1024-65535.

#### password_protected
If `True`, the whole api will be password protected.

#### Login
Login used by the basic HTTP authentication. Must be provided if `password_protected` is `True`

#### Password
Password used by the basic HTTP authentication. Must be provided if `password_protected` is `True`


## Default synapse

Run a default [synapse](brain.md) when Kalliope can't find the order in any synapse. 

```
default_synapse: "synapse-name"
```

E.g
```
default_synapse: "Default-response"
```

## Next: configure the brain of Kalliope
Now your settings are ok, you can start creating the [brain](brain.md) of your assistant.