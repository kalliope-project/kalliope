This Player is based on the [sounddevice and soundfile engines](https://pypi.python.org/pypi/sounddevice)

## Input parameters

| parameter      | required  | default   | choices     | comment                                                         |
|----------------|-----------|-----------|-------------|-----------------------------------------------------------------|
| convert_to_wav | no        | TRUE      | True, False | Convert the generated file from the TTS into wav before reading |


## Settings example

```yaml
default_player: "sounddeviceplayer"

players:
  - sounddeviceplayer:
     convert_to_wav: True
```

## Notes

>**Note:** This Player does not handle mp3 format, converting mp3 to wav might be required.

