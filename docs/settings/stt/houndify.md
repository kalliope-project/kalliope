This STT is based on the [Houndify](https://www.houndify.com/) engine.

This STT supports english only.

## Input parameters

| parameter | required | default | choices | comment   |
| :-------: | -------- | ------- | ------- | --------- |
|    key    | Yes      | None    |         | User info |
| client_id | Yes      | None    |         | User info |

## Settings example

```yaml
default_speech_to_text: "houndify"

speech_to_text:
  - houndify:
      key: "my_user_key"
      client_id: "my_user_client_id"
```
