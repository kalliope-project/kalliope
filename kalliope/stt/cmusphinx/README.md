### CMU Sphinx

This module is based on the self hosted STT solution [CMUSPhinx engine](http://cmusphinx.sourceforge.net/wiki/).
By default, only english language is available. You can download [another language model](https://sourceforge.net/projects/cmusphinx/files/Acoustic%20and%20Language%20Models/) from the main repository and install it following [the official documentation](http://cmusphinx.sourceforge.net/wiki/tutoriallm).

#### Installation

Install packages
```bash
sudo apt-get install swig libpulse-dev
```

Then install the python lib
```bash
sudo pip install pocketsphinx
```

Then, declare it as usual in your settings
```YAML
default_speech_to_text: "cmusphinx"

speech_to_text:  
  - cmusphinx:
      language: "en-US" #  [Installing other languages](https://github.com/Uberi/speech_recognition/blob/master/reference/pocketsphinx.rst#installing-other-languages)
```

#### Using keywords

Sphinx usually operates in 'transcription mode' and will return whatever words it recognizes.
Adding `keyword_entries` to the settings narrows down its search space and is more accurate than just looking for those same keywords in non-keyword-based transcriptions, because Sphinx knows specifically what sounds to look for.
The parameter `keyword_entries` expects a list of tuples consisting of a phrase and a sensitivity level defining how sensitive to this phrase the recognizer should be, on a scale from 0 (very insensitive, more false negatives) to 1 (very sensitive, more false positives).
```YAML
default_speech_to_text: "cmusphinx"

speech_to_text:  
  - cmusphinx:
      language: "en-US"
      keyword_entries:
        - ["hello", 0.8]
        - ["stop the music", 0.6]
```
