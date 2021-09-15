The api.ai STT is based on the [api.ai API](https://api.ai/)

## Input parameters

| parameter | required | default | choices                                    | comment   |
| --------- | -------- | ------- | ------------------------------------------ | --------- |
| key       | yes      | None    |                                            | User info |
| language  | no       | en-US   | [lang](https://docs.api.ai/docs/languages) |           |

## Settings example

```yaml
default_speech_to_text: "apiai"

speech_to_text:
  - apiai:
      key: "0cbff154af44944a6"
      language: "en"
```
