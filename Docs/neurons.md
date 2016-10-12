# Neurons

A neuron is a plugin that you can use in a synapse to perform action. 
Neurons are executed one by one when the input action is triggered.

## Usage
Neurons are declared in the `neurons` section of a synapse in your brain file.
The `neurons` section is a list (because it starts with a "-") which contains neuron module name
```
neurons:
    - neuron_name
    - neuron_2
    - another_neuron
```

Some neurons need parameters that can be passed as argument following the syntax bellow:
```
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```
> **note:** parameters are indented with two spaces bellow the neuron's name following the YAML syntax.

To know which parameter are required, check of documentation of the neuron.
Full list of [available neuron here](neuron_list.md)

## Overridable parameters

For each neuron, you can override some parameters to use a specific configuration of TTS instead of the default one 
set in [settings.yml](settings.yml) file.

### Cache

You can choose to override the default cache configuration. By default Kalliope use a cache to save a generated audio from a TTS engine.
This cache is usefull when you know that the text to speech will not change like in the following example
```
- say:
    message:
      - "Hello, sir"
```

In some case, and more specially when the neuron is based on a template, the generated audio will change at each new call of the neuron and so the usage 
of a cache is not necessary. 
The best example is when you use the `systemdate` neuron. As the time change every minute, the generated audio will change too.
Saving a cache of the generated audio is useless in this case. It where the usage of a cache override become usefull.
```
- systemdate:
    say_template:
      - "It's {{ hours }} hour and {{ minutes }} minute"
    cache: False
```

### tts

You can override the default tts in each neurons. Just add the tts parameter to the neuron like in the example bellow
```
neurons:
  - say:
    message:
      - "Hello, sir"
  - say:
    message:
      - "My name is Kalliope"
    tts: "voxygen"
```

Here, the first neuron will use the default tts as set in the settings.yml file. The second neuron will use the tts "voxygen".

>**Note:** The TTS must has been configured with its required parameters in the settings.yml file. See [TTS documentation](tts.md).

