# Neurons

A neuron is a plugin that you can use in a synapse to perform action. 
Neurons are executed one by one when the input action is triggered.

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
> **note:** parameters are indented with one tabulation bellow the neuron's name.

To know which parameter are required, check of documentation of the neuron.

Full list of [available neuron here](neuron_list.md)

