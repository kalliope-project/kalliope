### PyAlsaAudio

This Player is based on the [alsa engine](https://larsimmisch.github.io/pyalsaaudio/libalsaaudio.html)

| AlsaAudioPlayer |          |           |             |                                   |
|-----------------|----------|-----------|-------------|-----------------------------------|
| Parameters      | Required | Default   | Choices     | Comment                           |
| device          | No       | "default" |             | Select the device to use for alsa |
| convert_to_wav  | No       | TRUE      | True, False | convert the file into wav         |

#### Notes

Ability to define the device to use.
This Player does not handle mp3 format, converting mp3 to wav might be required.

