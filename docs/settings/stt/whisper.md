This module is based on the self hosted STT solution [OpenAI Whisper](https://github.com/openai/whisper).

## Installation

Install OpenAI Whisper using their installation guide. For example:
```bash
python3 -m pip install git+https://github.com/openai/whisper.git soundfile
```

## Input parameters

| parameter       | required | type   | default | choices | comment                                                                                                                                                |
| --------------- | -------- | ------ | ------- | ------- | ------------------------------------------------------------------------------------------------------------------------------------------------------ |
| model           | no       | string | tiny |         | One of the valid [SpeechRecognition OpenAI Whisper model values](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#recognizer_instancerecognize_whisperaudio_data-audiodata-model-strbase-show_dict-boolfalse-load_options-dictany-anynone-languageoptionalstrnone-translateboolfalse-transcribe_options) |
| language        | no       | string | None |         | One of the valid [SpeechRecognition OpenAI Whisper language values](https://github.com/Uberi/speech_recognition/blob/master/reference/library-reference.rst#recognizer_instancerecognize_whisperaudio_data-audiodata-model-strbase-show_dict-boolfalse-load_options-dictany-anynone-languageoptionalstrnone-translateboolfalse-transcribe_options). If not set, defaults to auto-translation which requires a full (i.e. non-`en`) model. |
| translate       | no       | bool   | False | True, False | Translate the spoken text into English before returning. Requires a full (i.e. non-`en`) model and `language` not set. |
| unformat        | no       | bool   | True | True, False | Return text as all-lowercase and stripped of the characters in `unformat_characters`; enabled by default but with no characters set. |
| unformat_characters | no | list | (empty) | | A list of characters to remove from the text when using `unformat`. |

## Settings example

```yaml
default_speech_to_text: "whisper"

speech_to_text:
  - whisper:
      model: "tiny"
      language: "english"
      translate: no
      unformat: yes
      unformat_characters:
        - '.'
        - ','
        - '?'
```

## Unformat

OpenAI Whisper by default returns a very well-formatted string, which will capitalize relevant letters (e.g. the first letter, proper names, etc.), add punctuation, render "35 dollars" as "$35", etc. This can have its uses, but for some users a more Google STT-like response, without capitalization or puncuation, might be more preferable.

By specifying the `unformat` option by itself, the string will be converted to all lowercase with Python's `lower()` function, but will be otherwise unchanged.

Further, a list of characters that should be removed can be specified with the `unformat_characters` option. In the example above, all periods, commas, and question marks will be removed from the script.

Together, the above example settings would render "What is the answer?" as "what is the answer" for use by neurons.
