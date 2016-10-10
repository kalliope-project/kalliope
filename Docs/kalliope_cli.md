# Kalliope Command-line interface

## SYNOPSIS
This is the syntax used to run Kalliope from command line
```
cd /path/to/kalliope
python kalliope.py command --option <argument>
```

For example, to start Kalliope we simply use
```
python kalliope.py start
```

## ARGUMENTS

### start
Start Kalliope main program

Example usage
```
python kalliope.py start
```

To kill Kalliope, you can press "Ctrl-C" on your keyboard.

### gui
Launch the Kalliope shell Graphical User Interface. 
The GUI allow you to test your [STT](stt.md) and [TTS](tts.md) that you have configured in [settings.yml](default_settings.md) file of Kalliope.

Example usage
```
python kalliope.py gui
```

## OPTIONS

### --run-synapse SYNAPSE_NAME

Run a specific synapse from the brain file.

Example usage
```
python kalliope.py start --run-synapse "say hello"
```

### --brain-file BRAIN_FILE

To use another brain file than the default one from the root of the project folder.
> **Important note:** The path must be absolute. The absolute path contains the root directory and all other subdirectories in which a file or folder is contained. 

Example usage
```
python kalliope.py start --brain-file /home/me/my_other_brain.yml
python kalliope.py start --run-synapse "say hello" --brain-file /home/me/my_other_brain.yml
```

### --debug

Show debug output in the console

Example usage
```
python kalliope.py start --debug
```