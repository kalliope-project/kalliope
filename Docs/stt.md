# Speech To Text (STT)

This chapter describes how STT engine works.

The STT is a programs or API that converts the speech into text.
Each STT has a specific configuration and supports multiple languages.

The configuration of each STT you use must appear in the [settings.yml](settings.md) file.

## Settings

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
Sometime, an API key will be necessary to use an engine. Click on a TTS engine link in the `Current Available STT` section to know which parameter are required.

## Current CORE Available STT
Core STTs are already packaged with the installation of Kalliope an can be used out of the box.

- [apiai](../kalliope/stt/apiai/README.md)
- [bing](../kalliope/stt/bing/README.md)
- [CMUSphinx](../kalliope/stt/cmusphinx/README.md)
- [google](../kalliope/stt/google/README.md)
- [houndify](../kalliope/stt/houndify/README.md)
- [witai](../kalliope/stt/wit/README.md)

## STT Community Installation

Community STTs need to be installed manually.

Use the CLI
```
kalliope install --git-url <git_url>
```

You may be prompted to type your `sudo` password during the process. You can see the list of [available STT here](stt_list.md)

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
