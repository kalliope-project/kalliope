This Player is based on the [pyaudio engine](https://people.csail.mit.edu/hubert/pyaudio/)

## Input parameters

| parameter      | required  | default   | choices     | comment                                                         |
|----------------|-----------|-----------|-------------|-----------------------------------------------------------------|
| convert_to_wav | no        | TRUE      | True, False | Convert the generated file from the TTS into wav before reading |


## Settings example

```yaml
default_player: "pyaudioplayer"

players:
  - pyaudioplayer:
     convert_to_wav: True
```


#### Notes

>**Note:** This Player does not handle mp3 format, converting mp3 to wav might be required.
