# JARVIS Command-line interface

## SYNOPSIS
This is the syntax used to run jarvis from command line
```
cd /path/to/jarvis
python jarvis.py command --option <argument>
```

For example, to start JARVIS we simply use
```
python jarvis.py start
```

## ARGUMENTS

### start
Start jarvis main program

Example usage
```
python jarvis.py start
```

To kill jarvis, you can press "Ctrl-C" on your keyboard.

### gui
Launch the jarvis shell Graphical User Interface. 
The GUI allow you to test your [STT](stt.md) and [TTS](tts.md) that you have configured in [settings.yml](default_settings.md) file of JARVIS.

Example usage
```
python jarvis.py gui
```

### load-events
Load crontab file with synapses from the brain which they have an event attached as inout signal.

Example usage
```
python jarvis.py load-events
```

## OPTIONS

### --run-synapse SYNAPSE_NAME

Run a specific synapse from the brain file.

Example usage
```
python jarvis.py start --run-synapse "say hello"
```

### --brain-file BRAIN_FILE

To use another brain file than the default one from the root of the project folder.
> **Important note:** The path must be absolute. The absolute path contains the root directory and all other subdirectories in which a file or folder is contained. 

Example usage
```
python jarvis.py start --brain-file /home/me/my_other_brain.yml
python jarvis.py start --run-synapse "say hello" --brain-file /home/me/my_other_brain.yml
```

### --debug

Show debug output in the console

Example usage
```
python jarvis.py start --debug
```