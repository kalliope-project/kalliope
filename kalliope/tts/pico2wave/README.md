### Pico2wave

This TTS is based on the SVOX picoTTS engine

| Parameters | Required | Default            | Choices      | Comment                                                                                                                                  |
|------------|----------|--------------------|--------------|------------------------------------------------------------------------------------------------------------------------------------------|
| language   | yes      |                    | 6 languages  | List of supported languages in the Note section                                                                                          |
| cache      | no       | TRUE               | True,  False | True if you want to use the cache with this TTS                                                                                          |
| samplerate | no       |                    | int          | Pico2wave creates 16 khz files but not all USB devices support this. Set a value to convert to a specific samplerate. For Example: 44100 |
| path       | no       | /usr/bin/pico2wave |              | Path to the Pico2wave binary. If not set, Kalliope will try to load it from the environment                                              |                                                     convert to a specific samplerate. For Example: 44100|


#### Notes :

Supported languages : 

- English en-US
- English en-GB
- French fr-FR
- Spanish es-ES
- German de-DE
- Italian it-IT
