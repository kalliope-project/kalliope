# Speech To Text (STT)

This chapter describes how STT are working.
This configuration must apply in the settings.yml.

The syntax used is YAML.

## General defaults

The setting.yml defines the STT you want to use by default
```
default_speech_to_text: "type default STT here"
```

Then, still in the settings.yml file, each STT must set up its configuration following 'speech_to_text' tag :
```
speech_to_text:
   - STT1:
      STT1parameter1: "value option1"
      STT1parameter2: "value option2"
   - STT2:
      STT2parameter1: "value option1"
```

## Current Available STT

### Google

The google STT is based on the [Google Speech Recognition API](https://cloud.google.com/speech/)

| parameter| required | default | choices | comments |
|----------|----------|---------|---------|----------|
| key      | No       | None    |         |          |
| language | No       | en-US   | [lang](https://en.wikipedia.org/wiki/Google_Voice_Search#Supported_languages)   |LCID string|

### Bing

The Bing STT is based on the [Microsoft Bing Voice Recognition API](https://www.microsoft.com/cognitive-services/en-us/speech-api)

| parameter| required | default | choices | comments |
|----------|----------|---------|---------|----------|
| key      | YES      | None    |         |User info |
| language | No       | en-US   | [lang](https://www.microsoft.com/cognitive-services/en-us/speech-api)|7 languages|

### wit.ai

The wit.ai STT is based on the Microsoft [Wit.ai API](https://wit.ai/)

| parameter| required | default | choices | comments |
|----------|----------|---------|---------|----------|
| key      | YES      | None    |         |User info |
| language | No       | en-US   |[lang](https://docs.api.ai/docs/languages)|          |

### api.ai

The api.ai STT is based on the [api.ai API](https://api.ai/)

| parameter| required | default | choices | comments |
|----------|----------|---------|---------|----------|
| key      | YES      | None    |         |User info |
| language | No       | en-US   |[lang](https://docs.api.ai/docs/languages)|          |

### Houndify

Not working yet ... in coming

| parameter| required | default | choices | comments |
|----------|----------|---------|---------|----------|
| key      | YES      | None    |         |User info |
| client_id| YES      | None    |         |User info |
| language | No       | en-US   | en-US   |          |

## Full Example

In the settings.yml file :

```
default_speech_to_text: "google"
speech_to_text:
  - google:
      language: "fr-FR"
  - wit:
      key: "B5JI3YUSLYOYWNIZRNBVM34XUODME2K"
  - bing:
      key: "9e48dert65904838bedc11aea6b36fb0"
  - apiai:
      key: "e0cbff145af44944a6b9f82c0668b527"
      language: "fr"
  - houndify:
      key: "6ej90T7qAV74OYXk4X4vI2Xhk7wPsJu4aEZ0G5Ll-BMmV1JGtFpCxtSH9SmTY4G3bpEJ7a5y_GTQid-CAKI6vw=="
      client_id: "lM2JXeaSticbSo9-llczbA=="

```
