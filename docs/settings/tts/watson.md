This TTS is based on the [IBM Watson engine](https://www.ibm.com/watson/services/text-to-speech/).

## Installation

You need to create an account and then a project to get a location and an apikey.

Once your project is created, you should see your credentials like the following:

```json
{
  "url": "https://stream.watsonplatform.net/text-to-speech/api",
  "apikey": "myRANDOMAPIKEY"
}
```

## Input parameters

| Parameters | Required | Default | Choices                                                                                                           | Comment                                                                                                              |
| ---------- | -------- | ------- | ----------------------------------------------------------------------------------------------------------------- | -------------------------------------------------------------------------------------------------------------------- |
| apikey     | yes      |         |                                                                                                                   | Apikey provided by [IBM](https://console.bluemix.net/docs/services/watson/getting-started-iam.html)                  |
| location   | no       | LONDON  |                                                                                                                   | [Endpoint location](https://www.ibm.com/watson/developercloud/text-to-speech/api/v1/curl.html?curl#service-endpoint) |
| voice      | yes      |         | See voice table below                                                                                             | Code that defines the voice used for the synthesis                                                                    |
| pitch      | no       | medium  | [See accepted values here](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-elements#prosody-pitch) | Modifies the baseline pitch for the text                                                                             |
| rate       | no       | medium  | [See accepted values here](https://cloud.ibm.com/docs/text-to-speech?topic=text-to-speech-elements#prosody-rate)  | Changes the speaking rate for the text                                                                                |

## Voice code

Voice code that can be used in the voice flag of your configuration

| Languages              | Code                             | Gender |
| ---------------------- | -------------------------------- | ------ |
| German                 | de-DE_BirgitVoice                | Female |
| German                 | de-DE_BirgitV3Voice              | Female |
| German                 | de-DE_DieterVoice                | Male   |
| German                 | de-DE_DieterV3Voice              | Male   |
| German                 | de-DE_ErikaV3Voice               | Female |
| UK English             | en-GB_CharlotteV3Voice           | Female |
| UK English             | en-GB_JamesV3Voice               | Male   |
| UK English             | en-GB_KateVoice                  | Female |
| UK English             | en-GB_KateV3Voice                | Female |
| US English             | en-US_AllisonVoice               | Female |
| US English             | en-US_AllisonV3Voice             | Female |
| US English             | en-US_EmilyV3Voice               | Female |
| US English             | en-US_HenryV3Voice               | Male   |
| US English             | en-US_KevinV3Voice               | Male   |
| US English             | en-US_LisaVoice                  | Female |
| US English             | en-US_LisaV3Voice                | Female |
| US English             | en-US_MichaelVoice (the default) | Male   |
| US English             | en-US_MichaelV3Voice             | Male   |
| US English             | en-US_OliviaV3Voice              | Female |
| Castilian Spanish      | es-ES_EnriqueVoice               | Male   |
| Castilian Spanish      | es-ES_EnriqueV3Voice             | Male   |
| Castilian Spanish      | es-ES_LauraVoice                 | Female |
| Castilian Spanish      | es-ES_LauraV3Voice               | Female |
| Latin American Spanish | es-LA_SofiaVoice                 | Female |
| Latin American Spanish | es-LA_SofiaV3Voice               | Female |
| North American Spanish | es-US_SofiaVoice                 | Female |
| North American Spanish | es-US_SofiaV3Voice               | Female |
| French                 | fr-FR_NicolasV3Voice             | Male   |
| French                 | fr-FR_ReneeVoice                 | Female |
| French                 | fr-FR_ReneeV3Voice               | Female |
| Italian                | it-IT_FrancescaVoice             | Female |
| Italian                | it-IT_FrancescaV3Voice           | Female |
| Japanese               | ja-JP_EmiVoice                   | Female |
| Japanese               | ja-JP_EmiV3Voice                 | Female |
| Brazilian Portuguese   | pt-BR_IsabelaVoice               | Female |
| Brazilian Portuguese   | pt-BR_IsabelaV3Voice             | Female |

## Settings example

```yaml
default_text_to_speech: "watson"

text_to_speech:
  - watson:
      apikey: "MyRANDOMAPIKEY"
      voice: "fr-FR_ReneeVoice"
      location: "https://stream-fra.watsonplatform.net/text-to-speech/api"
      pitch: "+3st"
      rate: "+10%"
```

## Notes

This TTS engine is free for less than 10,000 Characters per Month.
