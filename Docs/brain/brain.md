# Brain

The brain is where you create your personal assistant, your own configuration.

Brain is the link between input and output actions.

An input action can be:
- **an order:** Something that has been spoke out loud by the user.
- **an event:** A date or a frequency (E.G: repeat each morning at 8:30)

An output action is
- a neuron: A module or plugin that will perform some actions like simply talking, run a script, run a command or a complex Ansible playbook.
- a list of neurons

Brain is expressed in YAML format (see YAML Syntax) and have a minimum of syntax, which intentionally tries to not be a programming language or script, 
but rather a model of a configuration or a process.

Let's look a basic brain:

```
---
  - name: "Say hello"
    neurons:      
      - say:
          message: "Hello, sir"
    when:
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
This is the identifier of the task. This one must be unique as it will be used by the event handler based on crontab.

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
Not here that parameters are indented this one tabulation.


In this example, the neuron called "say" will make Jarvis speak out loud the phrase in parameter **message**.

The last part, called **when** is a list of input action. This last works exactly the same way as neurons. You must place here at least one action.
```
when:
  - order: "say hello"
```

In this example, the task is launched when the captured order contains "say hello". This means the order would start if you say
- "say hello jarvis"
- "jarvis, say hello"
- "I want you to say hello"
- "i say goodbye you say hello"
- "whatever I say as long it contains say hello"

