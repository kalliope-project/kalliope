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
# no parameters for this one
speech_to_text:  
  - cmusphinx
```
