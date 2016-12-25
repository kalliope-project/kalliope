# Contributing: Create a STT

[STT](../stt.md) are independent projects so they can be developed under a github project. 
Anyone can clone them and place them under the STT repository and reuse them or directly [install](../stt.md) them

Creating a new STT must follow some rules:

## Repository Structure
1. The STT repository name is in __lowercase__.
1. Under the STT repository, the STT has a __README.md file__ describing the STT following this structure. You can get a [template here](stt_template.md):
    - STT name:
    - Installation:     The CLI command used to install the STT
    - Synopsis:         Description of the STT
    - Options:          A table of the incoming parameters managed by the STT.
    - Notes:            Something which needs to be add.
    - Licence:          The licence you want to use
1. Under the STT repository, a [dna.yml file](dna.md) must be added that contains information about the STT. type = "stt"
1. Under the STT repository, a [install.yml file](installation_file.md) must be added that contains the installation process.


## Code
1. Under the STT repository, the STT file name .py is also in __lowercase__.
1. The STT must be coded in __Python 2.7__.
1. Under the STT repository, include the __init__.py file which contains: *from stt import STT* (/!\ respect the Case)
1. Inside the STT file, the STT Class name is in __uppercase__.
1. The STT __inherits from the OrderListener__ coming from the Core.

    ```
    from kalliope.core.OrderListener import OrderListener
    class Google(OrderListener):
    ```

1. The STT has a constructor __init__ which is the entry point.
The constructor has an incoming callback to call once we get the text.
The constructor has a __**kwargs argument__ which is corresponding to the Dict of incoming variables:values defined either in the settings file.
1. The STT must init itself first.
1. Attach the incoming callback to the self.attribute.
1. Obtain audio from the microphone in the constructor. (Note : we mostly use the [speech_recognition library](https://pypi.python.org/pypi/SpeechRecognition/))
1. Once you get the text back, let give it to the callback

    ```
    def __init__(self, callback=None, **kwargs):
        OrderListener.__init__(self)
        self.callback = callback
        # -------------------
        # do amazing code
        # -------------------
        self.callback(audio_to_text)
    ```



## Code example

Example of STT structure
```
mystt/
├── __init__.py
├── mystt.py
├── dna.yml
├── install.yml
└── README.md
```

Example of STT code
```
class Mystt(OrderListener):
def __init__(self, callback=None, **kwargs):
        OrderListener.__init__(self)
        self.callback = callback
        # -------------------
        # - get the microphone audio 
        # - do amazing code to retrieve the text
        # - call the callback giving it the result text -> self.callback(audio_to_text)
        # -------------------
        
```
