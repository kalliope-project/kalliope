This TTS is based on the [VoiceRSS engine](http://www.voicerss.org/). [Official Documentation here](http://www.voicerss.org/api/documentation.aspx)

## Input parameters

| Parameters   | Required | Default              | Choices                                                                           | Comment                                         |
| ------------ | -------- | -------------------- | --------------------------------------------------------------------------------- | ----------------------------------------------- |
| language     | YES      |                      | [26 languages](http://www.voicerss.org/api/documentation.aspx), example : "fr-fr" | Languages are identified by the LCID string     |
| key          | YES      |                      |                                                                                   | register in the official website to get API key |
| rate         | NO       | 0                    | any int                                                                           | Audio Rate                                      |
| codec        | NO       | 'MP3'                | 'MP3', 'WAV', 'AAC', 'OGG', 'CAF'                                                 | Audio Codecs                                    |
| audio_format | NO       | '44khz_16bit_stereo' | [51 choices](http://www.voicerss.org/api/documentation.aspx), '8khz_8bit_mono'    | Audio formats                                   |
| ssml         | NO       | False                | True / False                                                                      | True if you want ssml (only upgraded plans)     |
| base64       | NO       | False                | True / False                                                                      | True if you want base64                         |
| ssl          | NO       | False                | True / False                                                                      | True if you want ssl                            |
| cache        | NO       | True                 | True / False                                                                      | True if you want to use the cache with this TTS |

## Settings example

```yaml
default_text_to_speech: "voicerss"

text_to_speech:
    - voicerss:
        language: "fr-fr"
        key: "API_Key"
```

## Notes

limitations : 100KB per request

The Free edition is limited to 350 daily requests.
Possibility to [upgrade the plan](http://www.voicerss.org/personel/upgrade.aspx).
