# Triggers

With Kalliope project, you can set whatever Hotword you want to wake it up. 


# Snowboy

You can create your magic word by connecting to [Snowboy](https://snowboy.kitt.ai/) and then download the trained model file.

Once downloaded, place the file in your personal config folder and configure snowboy in your [your settings](settings.md) following the table bellow

| parameter   | required | type   | default | choices         | comment                                                                                          |
|-------------|----------|--------|---------|-----------------|--------------------------------------------------------------------------------------------------|
| pmdl_file   | TRUE     | string |         |                 | Path to the snowboy model file. The path can be absolute or relative to the brain file           |
| sensitivity | FALSE    | string | 0.5     | between 0 and 1 | Increasing the sensitivity value lead to better detection rate, but also higher false alarm rate |


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

## List of available Snowboy Kalliope model

> **Important note:** Do not enhance a model in the wrong language. Check the pronunciation before recording your voice!

| Name                                                 | language | Pronounced   |
|------------------------------------------------------|----------|--------------|
| [kalliope-FR](https://snowboy.kitt.ai/hotword/1363)  | French   | Ka-lio-pé    |
| [kalliope-EN](https://snowboy.kitt.ai/hotword/2540)  | English  | kə-LIE-ə-pee |
| [kalliope-RU](https://snowboy.kitt.ai/hotword/2964)  | Russian  | каллиопа     |
| [kalliope-DE](https://snowboy.kitt.ai/hotword/4324)  | German   | Ka-lio-pe    |
| [kalliope-IT](https://snowboy.kitt.ai/hotword/10650) | Italian  | Ka-lljo-pe   |
