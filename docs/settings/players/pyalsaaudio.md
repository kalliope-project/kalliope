This Player is based on the [alsa engine](https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html)

## Input parameters

| parameter      | required | default   | choices     | comment                                                         |
| -------------- | -------- | --------- | ----------- | --------------------------------------------------------------- |
| device         | no       | "default" |             | Select the device to use for alsa                               |
| convert_to_wav | no       | TRUE      | True, False | Convert the generated file from the TTS into wav before reading |

## Settings example

Here is an example of configuration you would use if your TTS was acapela. As this TTS generate an MP3 file, this last need to be converted into wav.

```yaml
default_player: "pyalsaaudio"

players:
  - pyalsaaudio:
      device: "default"
      convert_to_wav: True
```

## Notes

> **Note:** Define the default card to use in the `device` parameter. <br>
> For example, on a Raspberry Pi, the default card can be `sysdefault:CARD=ALSA`

> **Note:** This Player does not handle mp3 format, converting mp3 to wav might be required if the selected TTS engine generate mp3 file.
