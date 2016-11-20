# say

## Synopsis

This neuron is the mouth of Kalliope and uses the [TTS](../../Docs/tts.md) to say the given message.

## Options

| parameter | required | default | choices | comment                                |
|-----------|----------|---------|---------|----------------------------------------|
| message   | YES      |         |         | A list of messages Kalliope could say  |

## Return Values

No returned values

## Synapses example

Simple example : 

```
- name: "Say-hello"
  signals:
    - order: "hello"
  neurons:
    - say:
        message:
          - "Hello Sir"     
```

With a multiple choice list, Kalliope will pick one randomly:

```
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


## Notes

> **Note:** The neuron does not return any values.
> **Note:** Kalliope randomly takes a message from the list 
