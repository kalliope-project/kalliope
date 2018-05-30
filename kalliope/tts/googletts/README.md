### Googletts

This TTS is based on the [Google translate engine](http://translate.google.com/)


| Parameters | Required | Default | Choices                                                                                     | Comment                                                                                                    |
|------------|----------|---------|---------------------------------------------------------------------------------------------|------------------------------------------------------------------------------------------------------------|
| language   | YES      |         | 103 languages (http://translate.google.com/about/intl/en_ALL/languages.html), example: "fr" | Language are identified with their ISO_639-1 codes (https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) |
| cache      | No       | TRUE    | True / False                                                                                | True if you want to use the cache with this TTS                                                            |
| split_sentences      | No       | FALSE    | True / False                                                                                | True if you want to split sentences for larger text to speech requests to Google. (This may cause significant overhead but will allow you to use Googletts for larger chunks of text.)                                                            |
