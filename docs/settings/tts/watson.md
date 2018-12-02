This TTS is based on the [IBM Watson engine](https://www.ibm.com/watson/services/text-to-speech/).

## Installation

You need to create an account and then a project to get a location and an apikey.

Once you project created, you should see your credentials like the following
```json
{
  "url": "https://stream.watsonplatform.net/text-to-speech/api",
  "apikey": "myRANDOMAPIKEY"
}
```

## Input parameters

| Parameters | Required | Default | Choices               | Comment                                           |
|------------|----------|---------|-----------------------|---------------------------------------------------|
| apikey     | yes      |         |                       | apikey provided by [IAM](https://console.bluemix.net/docs/services/watson/getting-started-iam.html)                 |
| location   | no       |  LONDON |                       | [endpoint location](https://www.ibm.com/watson/developercloud/text-to-speech/api/v1/curl.html?curl#service-endpoint)                               |
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
      apikey: "MyRANDOMAPIKEY"
      voice: "fr-FR_ReneeVoice"
      location: "https://stream-fra.watsonplatform.net/text-to-speech/api"
```

## Notes

This TTS engine is free for less than 10,000 Characters per Month.
