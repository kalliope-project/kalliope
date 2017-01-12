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
1. The STT __inherits from the SpeechRecognition__ coming from the Utils file in the STT package.

    ```
    from kalliope.stt.Utils import SpeechRecognition
    class Google(SpeechRecognition):
    ```

1. The STT has a constructor __init__ which is the entry point.
The constructor has an incoming callback to call once we get the text.
The constructor has a __**kwargs argument__ which is corresponding to the Dict of incoming variables:values defined either in the settings file.
1. The STT must init itself first.
1. Attach the incoming callback to the self.attribute.
1. Obtain audio from the microphone in the constructor. (Note : we mostly use the [speech_recognition library](https://pypi.python.org/pypi/SpeechRecognition/))
1. Use self.start_listening(self.my_callback) from the mother class to get an audio and pass it to the callback of your choice.
1. The callback methode must implement two arguments: recognizer and audio. The audio argument contains the stream caught by the microphone
1. Once you get the text back, let give it to the callback method received in the constructor

    ```
    def __init__(self, callback=None, **kwargs):
        OrderListener.__init__(self)
        self.callback = callback
        
        self.argument_from_settings = kwargs.get('argument_from_settings', None)
        
        # start the microphone to capture an audio, give to the function a callback        
        self.stop_listening = self.start_listening(self.my_callback)
        
        def my_callback((self, recognizer, audio):
            # ---------------------------------------------
            # do amazing code
            # 'audio' contain stream caught by the microphone
            # ---------------------------------------------
            
            # at the end of the process, send the text into the received callback method
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
- [Google STT](../../kalliope/stt/google/README.md)
