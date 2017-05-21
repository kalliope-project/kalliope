### Acapela

This TTS is based on the [Acapela engine](http://www.acapela-group.com/)

| Parameters | Required | Default | Choices                                                                   | Comment                                                                     |
|------------|----------|---------|---------------------------------------------------------------------------|-----------------------------------------------------------------------------|
| voice      | YES      |         | 34 languages (https://acapela-box.com/AcaBox/index.php), example: "manon" | Check available voices on the web site                                      |
| spd        | NO       | 180     | Min: 120, Max: 240                                                        | Speech rate                                                                 |
| vct        | NO       | 100     | Min: 85, Max: 115                                                         | Voice shaping                                                               |
| cache      | No       | TRUE    | True / False                                                              | True if you want to use the cache with this TTS                             |

#### Notes

The voice name is attached to a specific language.
To test and get the name of a voice, please refer to [this website(https://acapela-box.com/AcaBox/index.php].

The generated file is mp3. 
