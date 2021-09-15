The Bing STT is based on the [Microsoft Bing Voice Recognition API](https://www.microsoft.com/cognitive-services/en-us/speech-api)

## Input parameters

| parameter | required | default | choices                                                               | comment     |
| --------- | -------- | ------- | --------------------------------------------------------------------- | ----------- |
| key       | YES      | None    |                                                                       | User info   |
| language  | No       | en-US   | [lang](https://www.microsoft.com/cognitive-services/en-us/speech-api) | 7 languages |

## Settings example

```yaml
default_speech_to_text: "bing"

speech_to_text:
  - bing:
      key: "9e48ddaf75904838bedc11aea6b36fb0"
      language: "en-US"
```
