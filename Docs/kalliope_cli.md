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

Example of use
```
python kalliope.py start
```

To kill Kalliope, you can press "Ctrl-C" on your keyboard.

### gui
Launch the Kalliope shell Graphical User Interface. 
The GUI allows you to test your [STT](stt.md) and [TTS](tts.md) that you have configured in [settings.yml](default_settings.md) file of Kalliope.

Example of use
```
python kalliope.py gui
```

## OPTIONS

Commands can be completed by the following options:

### --run-synapse SYNAPSE_NAME

Run a specific synapse from the brain file.

Example of use
```
python kalliope.py start --run-synapse "say hello"
```

### --brain-file BRAIN_FILE

Replace the default brain file from the root of the project folder by a custom one.
> **Important note:** The path must be absolute. The absolute path contains the root directory and all other subdirectories in which a file or folder is contained. 

Example of use
```
python kalliope.py start --brain-file /home/me/my_other_brain.yml
```

You can combine the options together like, for example:
```
python kalliope.py start --run-synapse "say hello" --brain-file /home/me/my_other_brain.yml
```

### --debug

Show debug output in the console

Example of use
```
python kalliope.py start --debug
```