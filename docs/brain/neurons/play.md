This neuron plays a given sound file.

## Input parameters

| parameter     | required | default | choices | comment                                                                                                             |
|:--------------|:---------|:--------|:--------|:--------------------------------------------------------------------------------------------------------------------|
| filename      | YES      |         |         | A single filename or a list of filenames for sound files that Kalliope should play (randomly picking one if a list) |

## Returned values

No returned values

## Synapses example

Simple example :

```yaml
- name: "Play-jingle"
  signals:
    - order: "play jingle"
  neurons:
    - play:
        filename: "resources/files/jingle.wav"
```

With a multiple choice list, Kalliope will pick one randomly:

```yaml
- name: "Play-random-jingle"
  signals:
    - order: "play random jingle"
  neurons:
    - play:
        filename:
          - "resources/files/jingle1.wav"
          - "resources/files/jingle2.wav"
          - "resources/files/jingle3.wav"
```

Play a sound instead of saying somthing after being triggered (the signal has to be configured accordingly in settings.yml):


```yaml
  - name: "on-triggered-synapse"
    signals: []
    neurons:
      - play:
          file: "resources/files/dong.wav"

```


## Notes

> **Note:** The neuron does not return any values.
>
> **Note:** Kalliope randomly takes a filename from the list
