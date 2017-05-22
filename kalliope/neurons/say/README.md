# say

## Synopsis

This neuron is the mouth of Kalliope and uses the [TTS](../../Docs/tts.md) to say the given message.

## Installation

CORE NEURON : No installation needed.  

## Options

| parameter | required | default | choices | comment                                |
|-----------|----------|---------|---------|----------------------------------------|
| message   | YES      |         |         | A list of messages Kalliope could say  |

## Return Values

No returned values

## Synapses example

Simple example : 

```yml
- name: "Say-hello"
  signals:
    - order: "hello"
  neurons:
    - say:
        message:
          - "Hello Sir"     
```

With a multiple choice list, Kalliope will pick one randomly:

```yml
- name: "Say-hello"
  signals:
    - order: "hello"
  neurons:
    - say:
        message:
          - "Hello Sir"
          - "Welcome Sir"
          - "Good morning Sir"
```

With an input value
```yml
- name: "Say-hello-to-friend"
  signals:
    - order: "say hello to {{ friend_name }}"
  neurons:
    - say:
        message:
          - "Hello {{ friend_name }}"     
```

## Notes

> **Note:** The neuron does not return any values.
> **Note:** Kalliope randomly takes a message from the list 
