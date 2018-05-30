# settings.yml

This part of the documentation explains the main configuration of Kalliope placed in the `settings.yml` file.

Kalliope will look for the settings file in the order bellow:

- From you current folder, E.g `/home/pi/my_kalliope/settings.yml`
- From `/etc/kalliope/settings.yml`
- From the default `settings.yml` located in the root of the project tree.

## Triggers configuration

### default_trigger

The trigger is the engine in charge of detecting the hotword that will wake up Kalliope.
Common usage of hotword include "Alexa" on Amazon Echo, "OK Google" on some Android devices and "Hey Siri" on iPhones.

Specify the name of the trigger module you want to use.
```yaml
default_trigger: "trigger_name"
```

E.g
```yaml
default_trigger: "snowboy"
```

### triggers
The hotword (also called a wake word or trigger word) detector is the engine in charge of waking up Kalliope.

Each Trigger has it own configuration. This configuration is passed as argument following the syntax bellow
```yaml
triggers:
  - trigger_name:
      parameter_name: "value"
```

E.g, the default Snowboy trigger configuration is
```yaml
triggers:
  - snowboy:
      pmdl_file: "trigger/snowboy/resources/model.pmdl"
```

### Settings example

```yaml
default_trigger: "snowboy"
triggers:
  - snowboy:
      pmdl_file: "trigger/snowboy/resources/model.pmdl"
```

### Available trigger engine

| Doc                            | Note                                                  |
| ------------------------------ | ----------------------------------------------------- |
| [snowboy](triggers/snowboy.md) | Based on [Snowboy software](https://snowboy.kitt.ai/) |

## Players configuration

The player is the library/software used to make Kalliope talk.
With Kalliope project, you can set whatever sound player you want to use.

### default_player

Specify the name of the player module you want to use.
```yaml
default_player: "player_name"
```
E.g
```yaml
default_player: "mplayer"
```

### players

Each Players has it own configuration.
This configuration is passed as argument following the syntax bellow
```yaml
players:
  - player_name:
      parameter_name: "value"
```

When no parameters are required set an empty object:
```yaml
players:
  - mplayer: {}
```

### Settings example

```yaml
players:
  - mplayer: {}
  - pyalsaaudio:
     device: "default"
     convert_to_wav: True
  - pyaudioplayer:
     convert_to_wav: True
  - sounddeviceplayer:
     convert_to_wav: True
```

>**Note:** Sometime, parameters will be necessary to use an engine.
Click on a Player engine link in the `Current CORE Available Players` section to know which parameter are required.

>**Note:** A player which does not ask for input parameters need to be declared as an empty dict. E.g: ```- player_name: {}```

>**Note:** Core players are already packaged with the installation of Kalliope an can be used out of the box.

>**Note:** Most cloud based TTS generate a file in MP3 format. Some players are not able to read this format and then a conversion to wav is needed.

### Available players

Core Players are already packaged with the installation of Kalliope an can be used out of the box.

| Doc                                               | Note                                                                                    |
| ------------------------------------------------- | --------------------------------------------------------------------------------------- |
| [mplayer](players/mplayer.md)                     | Based on [mplayer software](http://www.mplayerhq.hu/design7/news.html)                  |
| [pyalsaaudio](players/pyalsaaudio.md)             | Based on [pyalsaaudio](https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html) lib |
| [pyaudioplayer](players/pyaudioplayer.md)         | Based on [pyaudio](https://people.csail.mit.edu/hubert/pyaudio/docs/) lib               |
| [sounddeviceplayer](players/sounddeviceplayer.md) | Based on [sounddevice](https://pypi.python.org/pypi/sounddevice) lib                    |


## Speech to text configuration

### default_speech_to_text

A Speech To Text(STT) is an engine used to translate what you say into a text that can be processed by Kalliope core.
By default, Kalliope uses google STT engine.

The following syntax is used to provide the engine name:
```yaml
default_speech_to_text: "stt_name"
```

E.g
```yaml
default_speech_to_text: "google"
```

### speech_to_text
Each STT has it own configuration. This configuration is passed as argument as shown bellow
```yaml
speech_to_text:
  - stt_name:
      parameter_name: "value"
```

E.g:
```yaml
speech_to_text:
  - google:
      language: "fr-FR"
  - bing
```

### Settings example

```yml
default_speech_to_text: "google"
speech_to_text:
  - google:
      language: "fr-FR"
  - wit:
      key: "MYKEYS"
  - bing:
      key: "MYKEYS"
  - apiai:
      key: "MYKEYS"
      language: "fr"
  - houndify:
      key: "MYKEYS"
      client_id: "MYCLIENTID"

```

### Available STT

Core STTs are already packaged with the installation of Kalliope an can be used out of the box.

| Name                          | Type        |
| ----------------------------- | ----------- |
| [apiai](stt/api.ai.md)        | Cloud based |
| [Bing](stt/bing.md)           | Cloud based |
| [CMUSphinx](stt/CMUSphinx.md) | Self hosted |
| [Google](stt/google.md)       | Cloud based |
| [Houndify](stt/houndify.md)   | Cloud based |
| [wit.ai](stt/wit.ai.md)       | Cloud based |

## Text to speech configuration

### default_text_to_speech
A Text To Speech is an engine used to translate written text into a speech, into an audio stream.
By default, Kalliope use Pico2wave TTS engine.

The following syntax is used to provide the TTS engine name
```yaml
default_text_to_speech: "tts_name"
```

Eg
```yml
default_text_to_speech: "pico2wave"
```

### text_to_speech

Each TTS has it own configuration. This configuration is passed as argument following the syntax bellow
```yaml
text_to_speech:
  - tts_name:
      parameter_name: "value"
```

E.g
```yaml
text_to_speech:
  - pico2wave:
      language: "fr-FR"
  - googletts:
      language: "fr"
```

### cache_path

TTS engines work all the same, we give them a text, they give back an audio file and we play the audio file. The generated audio file is placed in cache until it
is played by the audio player. Before generating a new audio file, Kalliope will take a look to the cache to load it directly without having to call the
TSS engine if the file has been generated before.

You must set a path where the cache will be saved in the tag `cache_path`. This one is placed in /tmp by default.
```yml
cache_path: "/tmp/kalliope_tts_cache"
```

>**Note:** The path must be a valid path, and the current user must has enough right to read and write in it.

>**Note:** The consumed disk space can dramatically increase in the cache path folder. It is recommended to set your neuron correctly to clean up automatically
generated audio files that will not be played more than once.

### Settings example

```yaml
default_text_to_speech: "voicerss"

cache_path: "/tmp/kalliope_tts_cache"

text_to_speech:
  - pico2wave:
      language: "fr-FR"
      cache: True
  - acapela:
      language: "sonid15"
      voice: "Manon"
      cache: False
  - googletts:
      language: "fr"
  - voicerss:
      language: "fr-fr"
      cache: True
```

### Available TTS

Core TTSs are already packaged with the installation of Kalliope an can be used out of the box.

| Name                          | Type        |
| ----------------------------- | ----------- |
| [espeak](tts/espeak.md)       | Self hosted |
| [googletts](tts/googletts.md) | Cloud based |
| [pico2wave](tts/pico2wave.md) | Self hosted |
| [voicerss](tts/voicerss.md)   | Cloud based |
| [watson](tts/watson.md)       | Cloud based |


## Hooks

Hooking allow to bind actions to events based on the lifecycle of Kalliope.
For example, it's useful to know when Kalliope has detected the hotword from the trigger engine and make her spell out loud that she's ready to listen your order.

To use a hook, attach the name of the hook to a synapse (or list of synapse) which exists in your brain.

Syntax:
```yaml
hooks:
  hook_name1: synapse_name
  hook_name2:
    - synapse_name_1
    - synapse_name_2
```

E.g.
```yaml
hooks:
  on_start: "on-start-synapse"
```

List of available hook

| Hook name              | Description                                                     |
| ---------------------- | --------------------------------------------------------------- |
| on_start               | When kalliope is started. This hook will only be triggered once |
| on_waiting_for_trigger | When Kalliope waits for the hotword detection                   |
| on_triggered           | When the hotword has been detected                              |
| on_start_listening     | When the Speech to Text engine is listening for an order        |
| on_stop_listening      | When the Speech to Text engine stop listening for an order      |
| on_order_found         | When the pronounced order has been found in the brain           |
| on_order_not_found     | When the pronounced order has not been found in the brain       |
| on_processed_synapses  | When all neurons in synapses have been processed                |
| on_deaf                | When Kalliope switches from non deaf to deaf                    |
| on_undeaf              | When Kalliope switches from deaf to non deaf                    |
| on_mute                | When Kalliope switches from non mute to mute                    |
| on_unmute              | When Kalliope switches from mute to non mute                    |
| on_start_speaking      | When Kalliope starts speaking via the text to speech engine     |
| on_stop_speaking       | When Kalliope stops speaking                                    |
| on_stt_error           | When an error appeared during the STT processing                |

### Settings example

Example: You want to hear a random answer when the hotword has been triggered

**settings.yml**
```yaml
hooks:
  on_triggered: "on-triggered-synapse"
```

**brain.yml**
```yaml
- name: "on-triggered-synapse"
  signals: []
  neurons:
    - say:
        message:
          - "yes sir?"
          - "I'm listening"
          - "I'm listening to you"
          - "sir?"
          - "what can i do for you?"
          - "Speaking"
          - "how can i help you?"
```

Example: You want to know that your order has not been found

**settings.yml**
```yaml
hooks:
  on_order_not_found: "order-not-found-synapse"
```

**brain.yml**
```yaml
- name: "order-not-found-synapse"
    signals: []
    neurons:
      - say:
          message:
            - "I haven't understood"
            - "I don't know this order"
            - "Please renew your order"
            - "Would you please reword your order"
            - "Can ou please reformulate your order"
            - "I don't recognize that order"
```

Example: You are running Kalliope on a Rpi. You've made a script that turn on or off a led.
You can call this script every time kalliope start or stop speaking

**settings.yaml**
```yaml
hooks:
  on_start_speaking: "turn-on-led"
  on_stop_speaking: "turn-off-led"
```

**brain.yml**
```yaml
- name: "turn-on-led"
  signals: []
  neurons:
    - script:
        path: "/path/to/script.sh on"

- name: "turn-off-led"
  signals: []
  neurons:
    - script:
        path: "/path/to/script.sh off"
```

>**Note:** You cannot use a neurotransmitter neuron inside a synapse called from a hook.
You cannot use the "say" neuron inside the "on_start_speaking" or "on_stop_speaking" or it will create an infinite loop

## Rest API

A Rest API can be activated in order to:

- List synapses
- Get synapse's detail
- Run a synapse
- Update settings
- Update the brain

For the complete API ref see the [REST API documentation](../rest_api.md)

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

| parameter           | type    | comment                                                                                            |
| ------------------- | ------- | -------------------------------------------------------------------------------------------------- |
| active              | boolean | To enable the rest api server                                                                      |
| port                | integer | TThe listening port of the web server. Must be an integer in range 1024-65535                      |
| password_protected  | boolean | If `True`, the whole api will be password protected                                                |
| login               | string  | Login used by the basic HTTP authentication. Must be provided if `password_protected` is `True`    |
| password            | string  | Password used by the basic HTTP authentication. Must be provided if `password_protected` is `True` |
| allowed_cors_origin | string  | Allow request from external application. See examples bellow                                       |

**Cors request**

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
> **Note:** If a variable is defined in different files, the last file defines the value.

In the files the variables are defined by key/value:
```yml
variable: 60
baseURL: "http://blabla.com/"
password: "secret"
```

And use variables in your neurons:
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

> **Note:** Because YAML format does no allow double braces not surrounded by quotes: you must use the variable between double quotes.

A global variable can be a dictionary. Example:
```yml
contacts:
  nico: "1234"
  tibo: "5678"
```

And a synapse that use this dict:
```yml
- name: "test-var"
  signals:
    - order: "give me the number of {{ contact_to_search }}"
  neurons:
    - say:
        message:
        - "the number is {{ contacts[contact_to_search] }}"
```

## Options

Options that can be defined for Kalliope.

Example config
```yaml
options:
  mute: True
  deaf: False
```

Available options:

| Option                          | Description                                                                                  |
| ------------------------------- | -------------------------------------------------------------------------------------------- |
| mute                            | When mute, the STT engine will not be used to make Kalliope talking during neurons execution |
| deaf                            | When deaf, the trigger engine is not started. Kalliope will not listen for a wake up word    |
| energy_threshold                | [energy_threshold](#energy_threshold)                                                        |
| adjust_for_ambient_noise_second | [adjust_for_ambient_noise_second](#adjust_for_ambient_noise_second)                          |
| stt_timeout                     | Number of seconds before stop the STT process automatically                                  |


### energy_threshold

Represents the energy level threshold for sounds. By default set to **4000**.
Values below this threshold are considered silence, and values above this threshold are considered speech.
This is adjusted automatically if dynamic thresholds are enabled with `adjust_for_ambient_noise_second` parameter.

This threshold is associated with the perceived loudness of the sound, but it is a nonlinear relationship.
The actual energy threshold you will need depends on your microphone sensitivity or audio data.
Typical values for a silent room are 0 to 100, and typical values for speaking are between 150 and 3500.
Ambient (non-speaking) noise has a significant impact on what values will work best.

If you're having trouble with the recognizer trying to recognize words even when you're not speaking, try tweaking this to a higher value.
If you're having trouble with the recognizer not recognizing your words when you are speaking, try tweaking this to a lower value.
For example, a sensitive microphone or microphones in louder rooms might have a ambient energy level of up to 4000.
```yml
options:
  energy_threshold: 4000
```

>**Note:** The default value is 4000 if not set

### adjust_for_ambient_noise_second

If defined, will adjusts the energy threshold dynamically by capturing the current ambient noise of the room during the number of second set in the parameter.
When set, the `energy_threshold` parameter is overridden by the returned value of the noise calibration.
This value should be at least 0.5 in order to get a representative sample of the ambient noise.

```yml
options:
  adjust_for_ambient_noise_second: 1
```

>**Note:** The number of second here represents the time between kalliope's awakening and the moment when you can give her your order.
