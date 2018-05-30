This TTS is based on the [IBM Watson engine](https://www.ibm.com/watson/services/text-to-speech/).

## Installation

You need to create an account and then a project to get a username and password.

Once you project created, you should see your credentials like the following
```json
{
  "url": "https://stream.watsonplatform.net/text-to-speech/api",
  "username": "785dazs-example-98dz-b324-a965478az",
  "password": "generated_password"
}
```

## Input parameters

| Parameters | Required | Default | Choices               | Comment                                           |
|------------|----------|---------|-----------------------|---------------------------------------------------|
| username   | yes      |         |                       | Username of the created service in IBM cloud      |
| password   | yes      |         |                       | Password related to the username                  |
| voice      | yes      |         | See voice table below | Code that define the voice used for the synthesis |

## Voice code

Voice code that can be used in the voice flag of your configuration

| Languages              | Code                             | Gender |
|------------------------|----------------------------------|--------|
| German                 | de-DE_BirgitVoice                | Female |
| German                 | de-DE_DieterVoice                | Male   |
| UK English             | en-GB_KateVoice                  | Female |
| US English             | en-US_AllisonVoice               | Female |
| US English             | en-US_LisaVoice                  | Female |
| US English             | en-US_MichaelVoice (the default) | Male   |
| Castilian Spanish      | es-ES_EnriqueVoice               | Male   |
| Castilian Spanish      | es-ES_LauraVoice                 | Female |
| Latin American Spanish | es-LA_SofiaVoice                 | Female |
| North American Spanish | es-US_SofiaVoice                 | Female |
| French                 | fr-FR_ReneeVoice                 | Female |
| Italian                | it-IT_FrancescaVoice             | Female |
| Japanese               | ja-JP_EmiVoice                   | Female |
| Brazilian Portuguese   | pt-BR_IsabelaVoice               | Female |

## Settings example

```yaml
default_text_to_speech: "watson"

text_to_speech:
  - watson:
      username: "username_code"
      password: "generated_password"
      voice: "fr-FR_ReneeVoice"
```

## Notes

This TTS engine is free for less than 10,000 Characters per Month.
