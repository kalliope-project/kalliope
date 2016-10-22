# Speech To Text (STT)

This chapter describes how STT engine works.

The STT is a programs or API that converts the speech into text.
Each STT has a specific configuration and supports multiple voices and/or languages.

The configuration of each STT you use must appear in the [settings.yml](settings.md) file.

The syntax used is YAML.

## General defaults

The setting.yml defines the STT you want to use by default
```
default_speech_to_text: "type default STT here"
```

Then, still in the settings.yml file, each STT must set up its configuration following the 'speech_to_text' tag :
```
speech_to_text:
   - STT1:
      STT1parameter1: "value option1"
      STT1parameter2: "value option2"
   - STT2:
      STT2parameter1: "value option1"
```

## Current Available STT

- [apiai](../stt/apiai/README.md)
- [bing](../stt/bing/README.md)
- [google](../stt/google/README.md)
- [houndify](../stt/houndify/README.md)
- [witai](../stt/wit/README.md)

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
