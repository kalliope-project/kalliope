# Neurons

A neuron is a plugin that performs an action attached to some action. You can use it in to create a synapse.  
You can add as many neurons as you want to a synapse. The neurons are executed one by one when the input action is triggered.

## Usage
Neurons are declared in the `neurons` section of a synapse in your brain file.
The `neurons` section is a list (because it starts with a "-") which contains neuron modules names
```
neurons:
    - neuron_1_name
    - neuron_2_name
    - another_neuron
```

Some neurons need parameters that can be passed as arguments following the syntax bellow:
```
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```
> **note:** parameters are indented with two spaces bellow the neuron's name following the YAML syntax.

To know the list of required parameters, check of documentation of the neuron.
Full list of [available neuron here](neuron_list.md)

## Overridable parameters

For each neuron, you can override some parameters to use a specific configuration of TTS instead of the default one 
set in [settings.yml](settings.yml) file.

### Cache

You can override the default cache configuration. By default Kalliope uses a cache to save a generated audio from a TTS engine.
This cache is usefull to not to regenerate often used sentences that are not suppose to be changed very often. For exemple, the following sentence will not change in time, so it's more optimized to generate it once and to keep it in cash:
```
- say:
    message:
      - "Hello, sir"
```

In some cases, especially when the neuron is based on a template, the generated audio will change at each new call of the neuron and so the usage 
of a cache is not necessary. The best example of the case like this is the `systemdate` neuron. As the time changes every minute, the generated audio will change too and so, saving the generated audio in the cache is useless. In this case, you can override the cache usage for this neuron:
```
- systemdate:
    say_template:
      - "It's {{ hours }} hour and {{ minutes }} minute"
    cache: False
```

### tts

You can override the default tts for each neurons. Just add the "tts" parameter to the neuron like in the example bellow
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

