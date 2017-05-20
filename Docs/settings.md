# Kalliope settings

This part of the documentation explains the main configuration of Kalliope placed in the `settings.md` file.

## Triggers configuration

#### default_trigger

The trigger is the module detecting the hotword that will wake up Kalliope.
Common usage of hotword include Alexa on Amazon Echo, OK Google on some Android devices and Hey Siri on iPhones.

Specify the name of the trigger module you want to use.
```yml
default_trigger: "trigger_name"
```

Available triggers for Kalliope are:
- snowboy

#### triggers
The hotword (also called a wake word or trigger word) detector is the engine in charge of waking up Kalliope.

Each Trigger has it own configuration. This configuration is passed as argument following the syntax bellow
```yml
triggers:
  - trigger_name:
      parameter_name: "value"
```

E.g, the default Snowboy trigger configuration is
```yml
triggers:
  - snowboy:
      pmdl_file: "trigger/snowboy/resources/model.pmdl"
```

See the complete list of [available triggers here](trigger.md).

## Players configuration

#### default_player

The player is the module managing the sound in Kalliope.

Specify the name of the player module you want to use.
```yml
default_player: "player_name"
```

#### players
The player is the engine in charge of running sounds in Kalliope.

Each Players has it own configuration. 
This configuration is passed as argument following the syntax bellow
```yml
players:
  - player_name:
      parameter_name: "value"
```

See the complete list of [available players here](player.md).

when no parameters are required set an empty object:
```yml
players:
  - mplayer: {}

## Speech to text configuration

#### default_speech_to_text

A Speech To Text(STT) is an engine used to translate what you say into a text that can be processed by Kalliope core.
By default, Kalliope uses google STT engine.

The following syntax is used to provide the engine name:
```yml
default_speech_to_text: "stt_name"
```

E.g
```yml
default_speech_to_text: "google"
```

Get the full list of [SST engine here](stt.md).

#### speech_to_text
Each STT has it own configuration. This configuration is passed as argument as shown bellow
```yml
speech_to_text:
  - stt_name:
      parameter_name: "value"
```

E.g:
```yml
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
```yml
default_text_to_speech: "tts_name"
```

Eg
```yml
default_text_to_speech: "pico2wave"
```

Get the full list of [TTS engine here](tts.md).

#### text_to_speech
Each TTS has it own configuration. This configuration is passed as argument following the syntax bellow
```yml
text_to_speech:
  - tts_name:
      parameter_name: "value"
```

E.g
```yml
text_to_speech:
  - pico2wave:
      language: "fr-FR"
  - googletts:
      language: "fr"
```

Some arguments are required, some other optional, please refer to the [TTS documentation](tts.md) to know available parameters for each supported TTS.

## Wake up answers configuration

#### random_wake_up_answers
When Kalliope detects your trigger/hotword/magic word, it lets you know that it's operational and now waiting for order. It's done by answering randomly
one of the sentences provided in the variable random_wake_up_answers.

This variable must contain a list of strings as shown bellow
```yml
random_wake_up_answers:
  - "You sentence"
  - "Another sentence"
```

E.g
```yml
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

```yml
random_wake_up_sounds:
  - "local_file_in_sounds_folder.wav"
  - "/my/personal/full/path/my_file.mp3"
```

E.g
```yml
random_wake_up_sounds:
  - "ding.wav"
  - "dong.wav"
  - "/my/personal/full/path/my_file.mp3"
```

>**Note: ** If you want to use a wake up sound instead of a wake up answer you must comment out the `random_wake_up_answers` section.
E.g: `# random_wake_up_answers:`


## On ready notification
This section is used to notify the user when Kalliope is waiting for a trigger detection by playing a sound or speak a sentence out loud

#### play_on_ready_notification
This parameter define if you play the on ready notification:
 - `always`: every time Kalliope is ready to be awaken
 - `never`: never play a sound or sentences when kalliope is ready
 - `once`: at the first start of Kalliope

E.g:
```yml
play_on_ready_notification: always
```
#### on_ready_answers
The on ready notification can be a sentence. Place here a sentence or a list of sentence. If you set a list, one sentence will be picked up randomly

E.g:
```yml
on_ready_answers:
  - "I'm ready"
  - "Waiting for order"
```

#### on_ready_sounds
You can play a sound instead of a sentence.
Remove the `on_ready_answers` parameters by commenting it out and use this one instead.
Place here the path of the sound file. Files must be .wav or .mp3 format.

E.g:
```yml
on_ready_sounds:
  - "ding.wav"
  - "dong.wav"
  - "/my/personal/full/path/my_file.mp3"
```

>**Note: ** If you want to use a on ready sound instead of a on ready you must comment out the `random_on_ready_answers` section.
E.g: `# random_on_ready_answers:`


## Rest API

A Rest API can be activated in order to:
- List synapses
- Get synapse's detail
- Run a synapse

For the complete API ref see the [REST API documentation](rest_api.md)

Settings examples:
```yml
rest_api:
  active: True
  port: 5000
  password_protected: True
  login: admin
  password: secret
  allowed_cors_origin: "*"
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

#### Cors request
If you want to allow request from external application, you'll need to enable the CORS requests settings by defining authorized origins.
To do so, just indicated the origins that are allowed to leverage the API. The authorize values are:

False to forbid CORS request.
```yml
allowed_cors_origin: False
```

or either a string or a list:
```yml
allowed_cors_origin: "*"
```
(in case of "*", all origins are accepted).
or
```yml
allowed_cors_origin:
  - 'http://mydomain.com/*'
  - 'http://localhost:4200/*'
```

Remember that an origin is composed of the scheme (http(s)), the port (eg: 80, 4200,…) and the domain (mydomain.com, localhost).

## Default synapse

Run a default [synapse](brain.md) when Kalliope can't find the order in any synapse or if the SST engine haven't understood the order.

```yml
default_synapse: "synapse-name"
```

E.g
```yml
default_synapse: "Default-response"
```

## Resources directory

The resources directory is the path where Kalliope will try to load community modules like Neurons, STTs or TTSs.
Set a valid path is required if you want to install community neuron. The path can be relative or absolute.

```yml
resource_directory:
  resource_name: "path"
```

E.g
```yml
resource_directory:
  neuron: "resources/neurons"
  stt: "resources/stt"
  tts: "resources/tts"
  trigger: "/full/path/to/trigger"
```


## Global Variables

The Global Variables paths list where to load the global variables.
Those variables can be reused in neuron parameters within double brackets.

E.g 
```yml
var_files:
  - variables.yml
  - variables2.yml
```
/!\ If a variable is defined in different files, the last file defines the value.

In the files the variables are defined by key/value:
```yml
variable: 60
baseURL: "http://blabla.com/"
password: "secret"
```

And use variables in your neurons:
/!\ Because YAML format does no allow double braces not surrounded by quotes: you must use the variable between double quotes. 
```yml
  - name: "run-simple-sleep"
    signals:
      - order: "Wait for me "
    neurons:
      - uri:
          url: "{{baseURL}}get/1"        
          user: "admin"
          password: "{{password}}"
```

## Raspberry LED and mute button
LEDs connected to GPIO port of your Raspberry can be used to know current status of Kalliope.
A button can also be added in order to pause the trigger process. Kalliope does not listen for the hotword anymore when pressed.

A Dictionary called `rpi` can be declared which contains pin number to use following the mapping bellow

| Value name        | Description                                                                                                |
|-------------------|------------------------------------------------------------------------------------------------------------|
| pin_mute_button   | Pin connected to a mute button. When pressed the trigger process of kalliope is paused                     |
| pin_led_started   | Pin switched to "on" when Kalliope is running                                                              |
| pin_led_muted     | Pin switched to "on" when the mute button is pressed                                                       |
| pin_led_talking   | Pin switched to "on" when Kalliope is talking                                                              |
| pin_led_listening | Pin switched to "on" when Kalliope is readu to listen an order after a trigger detection ("Say something") |

**Example config**
```yml
rpi:
  pin_mute_button: 6
  pin_led_started: 5
  pin_led_muted: 17
  pin_led_talking: 27
  pin_led_listening: 22
```

You can also define a couple led instead of all if you don't use them
```yml
rpi:
  pin_mute_button: 6
  pin_led_started: 5
#  pin_led_muted: 17
#  pin_led_talking: 27
#  pin_led_listening: 22
```

**Example circuit**

You will be using one of the ‘ground’ (GND) pins to act like the ‘negative’ or 0 volt ends of a battery. 
The ‘positive’ end of the battery will be provided by a GPIO pin.

<p align="center">
    <img style="width: 200px;" src="../images/led_kalliope_circuit.png">
</p>


>**Note:** You must ALWAYS use resistors to connect LEDs up to the GPIO pins of the Raspberry Pi. 
The Raspberry Pi can only supply a small current (about 60mA). T
he LEDs will want to draw more, and if allowed to they will burn out the Raspberry Pi. 
Therefore putting the resistors in the circuit will ensure that only this small current will flow and the Pi will not be damaged.


## Next: configure the brain of Kalliope
Now your settings are ok, you can start creating the [brain](brain.md) of your assistant.
