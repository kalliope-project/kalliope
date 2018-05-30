The google STT is based on the [Google Speech Recognition API](https://cloud.google.com/speech/).
This STT is free for less than 60 minutes of usage per month. After that you need a subscription.

## Input parameters

| parameter | required | default | choices                                                                       | comment     |
| --------- | -------- | ------- | ----------------------------------------------------------------------------- | ----------- |
| key       | No       | None    |                                                                               |             |
| language  | No       | en-US   | [lang](https://en.wikipedia.org/wiki/Google_Voice_Search#Supported_languages) | LCID string |


## Settings example

Free usage
```yaml
default_speech_to_text: "google"

speech_to_text:
  - google:
      language: "fr-FR"
```

For paying users
```yaml
default_speech_to_text: "google"

speech_to_text:
  - google:
      language: "fr-FR"
      key: "my_google_stt_key"
```
