This TTS is based on the SVOX picoTTS engine

## Input parameters

| Parameters | Required | Default            | Choices     | Comment                                                                                     |
| ---------- | -------- | ------------------ | ----------- | ------------------------------------------------------------------------------------------- |
| language   | yes      |                    | 6 languages | List of supported languages in the Note section                                             |
| cache      | no       | TRUE               | True, False | True if you want to use the cache with this TTS                                             |
| path       | no       | /usr/bin/pico2wave |             | Path to the Pico2wave binary. If not set, Kalliope will try to load it from the environment |

## Settings example

```yaml
default_text_to_speech: "pico2wave"

text_to_speech:
  - pico2wave:
      language: "fr-FR"
      cache: True
```

## Notes

Supported languages:

- English en-US
- English en-GB
- French fr-FR
- Spanish es-ES
- German de-DE
- Italian it-IT
