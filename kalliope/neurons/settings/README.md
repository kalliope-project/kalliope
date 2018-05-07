# SETTINGS

## Synopsis

Manage / Update / Add settings entries of Kalliope []
Currently available:
- default_tts
- default_stt
- default_trigger
- default_player
- text_to_speech
- speech_to_text
- triggers
- players
- hooks
- var_files
- variable
- deaf
- mute
- energy_threshold
- adjust_for_ambient_noise_second

## Installation

CORE NEURON : No installation needed.

## Options

| parameter                       | required | type           | default | choices     | comment                                                         |
|---------------------------------|----------|----------------|---------|-------------|-----------------------------------------------------------------|
| default_tts                     | No       | Str            | None    |             | Pick a tts name from the list of text_to_speech                 |
| default_stt                     | No       | Str            | None    |             | Pick a stt name from the list of speech_to_text                 |
| default_trigger                 | No       | Str            | None    |             | Pick a trigger name from the list of triggers                   |
| default_player                  | No       | Str            | None    |             | Pick a player name from the list of players                     |
| text_to_speech                  | No       | list (of dict) | None    |             | Add or Update a tts to the list                                 |
| speech_to_text                  | No       | list (of dict) | None    |             | Add or Update a stt to the list                                 |
| triggers                        | No       | list (of dict) | None    |             | Add or Update a trigger to the list                             |
| players                         | No       | list (of dict) | None    |             | Add or Update a player to the list                              |
| hooks                           | No       | dict           | None    |             | Update the hooks dict from the settings with the given dict     |
| var_files                       | No       | list           | None    |             | Update variables from the settings with the given files path    |
| variable                        | No       | dict           | None    |             | Update the variable dict from the settings with the given dict  |
| deaf                            | No       | boolean        | None    | True, False |                                                                 |
| mute                            | No       | boolean        | None    | True, False |                                                                 |
| energy_threshold                | No       | int            | None    |             |                                                                 |
| adjust_for_ambient_noise_second | No       | int            | None    |             |                                                                 |

## Return Values

Nope

## Synapses example

#### tts, stt, triggers, players 
```yaml
  - name: "say-hello-en"
    signals:
      - order: "Hello"
    neurons:
      - settings:
          default_tts: "googletts"
      - say:
          message:
            - "Hello sir"
```

To update the list of text_to_speech
```yaml
  - name: "say-hello-en"
    signals:
      - order: "Hello"
    neurons:
      - settings:
          text_to_speech:
            - googletts:
                language: "en"
            - pico2wave:
                language: "fr-FR"
                cache: False
          default_tts: "googletts"
      - say:
          message:
            - "Hello sir"
```

#### Options (deaf, mute, ...)
```yaml
  - name: "say-hello-en"
    signals:
      - order: "Hello"
    neurons:
      - settings:
          mute: True
      - say:
          message:
            - "Hello sir"
```

#### Hooks
```yaml
- name: "say-hello-en"
    signals:
      - order: "Hello"
    neurons:
      - settings:
          hooks:
            on_order_found: "random-on-order-found-synapse"
            on_processed_synapses:
              - "random1-on-processed-synapse"
              - "random2-on-processed-synapse"
      - say:
          message:
            - "Hello sir"
```

#### Variables
```yaml
  - name: "say-hello-en"
    signals:
      - order: "Hello"
    neurons:
      - settings:
          variable:
            nickname: "monf"
      - say:
          message:
            - "Hello {{nickname}}"

```

/!\ the keyword is 'var_files' for files!

The {{nickname}} will be loaded from the variables.yml file.
```yaml
  - name: "say-hello-en"
    signals:
      - order: "Hello"
    neurons:
      - settings:
          var_files:
            - variables.yml
      - say:
          message:
            - "Hello {{nickname}}"
```

## Notes

>**Note:** It is not possible to update the REST API config nor the ressources path nor the cache path for tts.

>**Note:** Changes made to the settings from this neuron are not persistent. Settings will be loaded again following the yaml file at the next start of Kalliope.