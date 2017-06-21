### Pico2wave

This TTS is based on the SVOX picoTTS engine

| Parameters | Required | Default | Choices      | Comment                                         |
|------------|----------|---------|--------------|-------------------------------------------------|
| language   | YES      |         | 6 languages  | List of supported languages in the Note section |
| cache      | No       | TRUE    | True / False | True if you want to use the cache with this TTS |
| change_rate| No|False |True / False| Pico2wave creates 16 khz files but not all USB devices support this. If True this will change the samplerate to 44.1 Khz |


#### Notes :

Supported languages : 

- English en-US
- English en-GB
- French fr-FR
- Spanish es-ES
- German de-DE
- Italian it-IT
