# Brain

The brain is where you create your personal assistant, your own configuration.

Brain is composed by synapses, a synapse is the link between input and output actions.

A input action, called a "signal" can be:
- **an order:** Something that has been spoke out loud by the user.
- **an event:** A date or a frequency (E.G: repeat each morning at 8:30)

An output action is
- **a list of neurons:** A module or plugin that will perform some actions like simply talking, run a script, run a command or a complex Ansible playbook.

Brain is expressed in YAML format (see YAML Syntax) and have a minimum of syntax, which intentionally tries to not be a programming language or script, 
but rather a model of a configuration or a process.

Let's look a basic synapse in our brain:

```
---
  - name: "Say hello"
    neurons:      
      - say:
          message: "Hello, sir"
    signals:
      - order: "say hello"
```

Let's break this down in sections so we can understand how the file is built and what each piece means.

The file starts with:
```
---
```
This is a requirement for YAML to interpret the file as a proper document.

Items that begin with a ```-``` are considered list items. Items that have the format of ```key: value``` operate as hashes or dictionaries.

At the top level we have a "name"
```
- name: "Say hello"
```
This is the **unique identifier** of the synapse. It must be unique to each synapse and should not contain any accent.

Then we have the neurons declaration that contain a list (because it starts with a "-") which contains neurons
```
neurons:
    - neuron_name
    - neuron_2
    - another_neuron
```

Neurons are modules that will be executed when the input action is triggered.
Some neurons need parameters that can be passed as argument following the syntax bellow:
```
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```
Not here that parameters are indented with one tabulation bellow the neuron's name.

In this example, the neuron called "say" will make Kalliope speak out loud the sentence in parameter **message**.
See the complete list of [available neurons](neurons.md) here.

The last part, called **signals** is a list of input action. This last works exactly the same way as neurons. You must place here at least one action.
In the following example, we use just one signal, an order. See the complete list of [available signals](signals.md) here.
```
signals:
  - order: "say hello"
```

In this example, the task is launched when the captured order contains "say hello". This means the order would start if you say
- "say hello Kalliope"
- "Kalliope, say hello"
- "I want you to say hello"
- "i say goodbye you say hello"
- "whatever I say as long it contains say hello"

To know if your spoken order will be triggered by Kalliope, we recommend you to [use the GUI](kalliope_cli.md) for testing your STT engine.