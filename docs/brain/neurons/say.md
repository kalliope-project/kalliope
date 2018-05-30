This neuron is the mouth of Kalliope and uses the TTS engine defined in your settings to say the given message.

## Input parameters

| parameter | required | default | choices | comment                                                    |
|-----------|----------|---------|---------|------------------------------------------------------------|
| message   | YES      |         |         | A single message or a list of messages Kalliope could say  |

## Returned values

No returned values

## Synapses example

Simple example :

```yaml
- name: "Say-hello"
  signals:
    - order: "hello"
  neurons:
    - say:
        message: "Hello Sir"
```

With a multiple choice list, Kalliope will pick one randomly:

```yaml
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
```yaml
- name: "Say-hello-to-friend"
  signals:
    - order: "say hello to {{ friend_name }}"
  neurons:
    - say:
        message: "Hello {{ friend_name }}"
```

## Notes

> **Note:** The neuron does not return any values.
>
> **Note:** Kalliope randomly takes a message from the list
