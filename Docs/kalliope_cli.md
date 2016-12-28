# Kalliope Command-line interface

## SYNOPSIS
This is the syntax used to run Kalliope from command line
```
kalliope command --option <argument>
```

For example, to start Kalliope we simply use
```
kalliope start
```

## ARGUMENTS

### start
Start Kalliope main program

Example of use
```
kalliope start
```

To kill Kalliope, you can press "Ctrl-C" on your keyboard.

### gui
Launch the Kalliope shell Graphical User Interface. 
The GUI allows you to test your [STT](stt.md) and [TTS](tts.md) that you have configured in [settings.yml](default_settings.md) file of Kalliope.

Example of use
```
kalliope gui
```

### install
Install a community module. You must set an install type option. Currently the only available option is `--git-url`.

Syntax
```
kalliope install --git-url <url>
```

Example of use
```
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_wikipedia.git
```

## OPTIONS

Commands can be completed by the following options:

### --run-synapse SYNAPSE_NAME

Run a specific synapse from the brain file.

Example of use
```
kalliope start --run-synapse "say-hello"
```

### --brain-file BRAIN_FILE

Replace the default brain file from the root of the project folder by a custom one.
> **Important note:** The path must be absolute. The absolute path contains the root directory and all other subdirectories in which a file or folder is contained. 

Example of use
```
kalliope start --brain-file /home/me/my_other_brain.yml
```

You can combine the options together like, for example:
```
kalliope start --run-synapse "say-hello" --brain-file /home/me/my_other_brain.yml
```

### --debug

Show debug output in the console

Example of use
```
kalliope start --debug
```

### --git-url

Used by the `install` argument to specify the URL of a git repository of the module to install.
