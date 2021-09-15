This TTS is based on the [Google translate engine](http://translate.google.com/)

## Input parameters

| Parameters | Required | Default | Choices                                                                       | Comment                                                                                                    |
| ---------- | -------- | ------- | ----------------------------------------------------------------------------- | ---------------------------------------------------------------------------------------------------------- |
| language   | YES      |         | [103 languages](http://translate.google.com/about/intl/en_ALL/languages.html) | Language are identified with their [ISO_639-1 codes](https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes) |
| cache      | No       | TRUE    | True / False                                                                  | True if you want to use the cache with this TTS                                                            |

## Settings example

```yaml
default_text_to_speech: "googletts"

text_to_speech:
  - googletts:
      language: "fr"
```
