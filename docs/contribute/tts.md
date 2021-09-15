# Contributing: Create a TTS

TTS are independent projects so they can be developed under a github project.
Anyone can clone them and place them under the TTS repository and reuse them or directly install them.

Creating a new TTS must follow some rules:

## Repository Structure

1. The TTS repository name is in **lowercase**.
2. Under the TTS repository, the TTS has a **README.md file** describing the TTS following this structure:
   - TTS name: TTS's name.
   - Installation: The CLI command used to install the TTS.
   - Synopsis: Description of the TTS.
   - Options: A table of the incoming parameters managed by the TTS.
   - Notes: Something which needs to be added.
   - Licence: The licence you want to use.
3. Under the TTS repository, a [dna.yml file](dna.md) must be added that contains information about the TTS. type = "tts"
4. Under the TTS repository, a [install.yml file](installation_file.md) must be added that contains the installation process.

## Code

1. Under the TTS repository, the TTS file name .py is also in **lowercase**.
2. The TTS must be coded in **Python 2.7**.
3. Under the TTS repository, include the **init**.py file which contains: _from tts import TTS_ (/!\ respect the Case)
4. Inside the TTS file, the TTS Class name is in **uppercase**.
5. The TTS **inherits from the TTSModule** coming from the Core.

   ```python
   from kalliope.core.TTS.TTSModule import TTSModule
   class Pico2wave(TTSModule):
   ```

6. The TTS has a constructor **init** which is the entry point.
   The constructor has a **\*\*kwargs argument** which is corresponding to the Dict of incoming variables: values defined either in the settings file.
7. The TTS must refer to its **parent structure** in the init by calling the super of TTSModule.

   ```python
    def __init__(self, **kwargs):
       super(Pico2wave, self).__init__(**kwargs)
   ```

8. The TTS **must** implement a method \_say(self, words) which must call a method coming from the mother Class self.generate_and_play(words, callback).
9. Implement a callback in a separate method to run the audio.
   This callback is in charge to get the sound and save it on the disk. You can use our lib "FileManager.write_in_file(file_path, content)"
10. The module must use `self.file_path` from the mother class to know the full path where to save the generated audio file. The file path is handled by the core in order to allow caching.
11. The generated audio file must be supported by Mplayer. Try to play a generated file with `mplayer /path/to/the/generated_audio_file`

## Code example

Example of TTS structure

```
mytts/
├── __init__.py
├── mytts.py
├── dna.yml
├── install.yml
└── README.md
```

Example of TTS code

```python
class Mytts(TTSModule):
def __init__(self, **kwargs):
    super(Mytts, self).__init__(**kwargs)
    # the args from the tts configuration
    self.arg1 = kwargs.get('arg1', None)
    self.arg2 = kwargs.get('arg2', None)

    def say(self, words):
        """
        :param words: The sentence to say
        """

        self.generate_and_play(words, self._generate_audio_file)

    def _generate_audio_file(self):
    """
    Generic method used as a Callback in TTSModule
        - must provided the audio file and write it on the disk in self.file_path

    .. raises:: FailToLoadSoundFile
    """
    # -------------------
    # - do amazing code to get the sound
    # - save it to the disk using self.file_path
    # - Attach the sound file path to the attribute : self.file_path = audio_file_path !
    # -------------------

```
