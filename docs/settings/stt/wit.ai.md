The wit STT is based on the [Wit.ai API](https://wit.ai/)

## Input parameters

| parameter | required  | default | choices                                    | comment   |
|:---------:|-----------|---------|--------------------------------------------|-----------|
| key       | Yes       | None    |                                            | User info |

## Settings example

```yaml
default_speech_to_text: "wit"

speech_to_text:
  - wit:
      key: "my_user_key"
```
