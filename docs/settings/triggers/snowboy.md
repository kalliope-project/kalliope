# Parameters

You can create your magic word by connecting to [Snowboy](https://snowboy.kitt.ai/) and then download the trained model file.

Once downloaded, place the file in your personal config folder and configure snowboy in your [your settings](../settings.md) following the table bellow

Snowboy config:

| parameter      | required | type   | default | choices    | comment                                                                                        |
| -------------- | -------- | ------ | ------- | ---------- | ---------------------------------------------------------------------------------------------- |
| keywords       | TRUE     | list   |         |            | List of `Keyword` objects                                                           |
| apply_frontend | FALSE    | string | False   | True/False | Some universal models (umdl files) need apply_frontend to work properly. See explanation below |

`Keyword` object:

| parameter   | required | type        | default | choices         | comment                                                                                                                                                         |
| ----------- | -------- | ----------- | ------- | --------------- | --------------------------------------------------------------------------------------------------------------------------------------------------------------- |
| file_path   | TRUE     | string      |         |                 | Path to the snowboy model file. The path can be absolute or relative to the brain file                                                                          |
| sensitivity | FALSE    | string/list | 0.5     | between 0 and 1 | Increasing the sensitivity value lead to better detection rate, but also higher false alarm rate. For some umdl models, it can be a string or a list of strings |

## Notes

### apply_frontend

If `apply_frontend` is true, then apply frontend audio processing;
otherwise turns the audio processing off. Frontend audio processing includes algorithms such as automatic gain control (AGC), noise suppression
(NS) and so on. Generally adding frontend audio processing helps the performance, but if the model is not trained with frontend audio
processing, it may decrease the performance. The general rule of thumb is:

    1. For personal models, set it to false.
    2. For universal models, follow the instruction of each published model

### Universal models

Some universal models contains two keywords, if we want to set a custom sensitivity we need to add two sensitivities for each keyword.  

## Configuration examples

Example settings for single keyword
```yaml
# This is the trigger engine that will catch your magic work to wake up Kalliope.
default_trigger: "snowboy"

# Trigger engine configuration
triggers:
  - snowboy:
      keywords:
        - file_path: "trigger/kalliope-FR.pmdl"
          sensitivity: "0.6"
```


Example settings for multiple keywords, where we set the sensitivity for jarvis.umdl and set apply_frontend to True

```yaml
# This is the trigger that will catch your magic work to wake up Kalliope
default_trigger: "snowboy"
triggers:
  - snowboy:
      apply_frontend: True
      keywords:
        - file_path: "trigger/kalliope-FR.pmdl"
        - file_path: "trigger/jarvis.umdl"
          sensitivity:
            - "0.6"
            - "0.7"  
```
## Available Snowboy models

If you want to keep "Kalliope" as the name of your bot, we recommend you to __enhance the existing Snowboy model for your language__.

We will update the following list with all Kalliope model created by the community. If the model doesn't exist, please create one with the following syntax:
```
kalliope-<language_code>
```

E.g
```
kalliope-FR
kalliope-EN
kalliope-RU
kalliope-DE
kalliope-IT
```
Then, open an issue or create a pull request to add the model to the list bellow.

> **Important note:** Do not enhance a model in the wrong language. Check the pronunciation before recording your voice!

| Name                                                 | language | Pronounced   |
|------------------------------------------------------|----------|--------------|
| [kalliope-FR](https://snowboy.kitt.ai/hotword/1363)  | French   | Ka-lio-pé    |
| [kalliope-EN](https://snowboy.kitt.ai/hotword/2540)  | English  | kə-LIE-ə-pee |
| [kalliope-RU](https://snowboy.kitt.ai/hotword/2964)  | Russian  | каллиопа     |
| [kalliope-DE](https://snowboy.kitt.ai/hotword/4324)  | German   | Ka-lio-pe    |
| [kalliope-IT](https://snowboy.kitt.ai/hotword/10650) | Italian  | Ka-lljo-pe   |



## Pretrained universal models

Snowboy provides pretrained universal models.
Ŷou can either find them [here](https://github.com/Kitt-AI/snowboy/tree/master/resources)

Here is the list of the umdl models, and the parameters that you have to use for them:

* alexa.umdl: Universal model for the hotword "Alexa". Set `apply_frontend` to `True`.
* snowboy.umdl: Universal model for the hotword "Snowboy". Set `apply_frontend` to `False`.
* jarvis.umdl: Universal model for the hotword "Jarvis". It has two different models for the hotword Jarvis, so you have to use two sensitivites. Set `apply_frontend` to `True`.
* smart_mirror.umdl: Universal model for the hotword "Smart Mirror". Set `apply_frontend` to `False`.
* subex.umdl: Universal model for the hotword "Subex". Set apply_frontend to true.
* neoya.umdl: Universal model for the hotword "Neo ya". It has two different models for the hotword "Neo ya", so you have to use two sensitivites. Set `apply_frontend` to `True`.
* hey_extreme.umdl: Universal model for the hotword "Hey Extreme". Set `apply_frontend` to `True`.
* computer.umdl: Universal model for the hotword "Computer". Set `apply_frontend` to `True`.
* view_glass.umdl: Universal model for the hotword "View Glass". Set `apply_frontend` to `True`.


## Note

Snowboy is shutting down by Dec. 31st, 2020. After the shutdown the trigger will still work, but we will be unable to create new keywords. 
