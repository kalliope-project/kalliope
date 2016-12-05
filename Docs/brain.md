# Brain

The brain is a main component of Kalliope. It's a module that gives a configuration of your own personal assistant and, so, determines it's behavior and fonctionnalities.

Brain is composed by synapses: a synapse is the link between input and output actions.

An input action, called a "[signal](signals.md)" can be:
- **an order:** Something that has been spoke out loud by the user.
- **an event:** A date or a frequency (E.G: repeat each morning at 8:30)

An output action is
- **a list of neurons:** A [neuron](neurons.md) is a module or plugin that will perform some actions like simply talking, run a script, run a command or a complex Ansible playbook.

Brain is expressed in YAML format (see YAML Syntax) and has a minimum of syntax, which intentionally tries to not be a programming language or script, 
but rather a model of a configuration or a process.
Kalliope will search her brain in the order bellow:
- From you current folder, E.g `/home/pi/my_kalliope/brain.yml`
- From `/etc/kalliope/brain.yml`
- From the default `brain.yml`. You can take a look into the default [`brain.yml`](../kalliope/brain.yml) file which is located in the root of the project tree.

Let's take a look on a basic synapse in our brain:

```
---
  - name: "Say-hello"
    signals:
      - order: "say hello"
    neurons:      
      - say:
          message: "Hello, sir"    
```

Let's break this down in sections so we can understand how the file is built and what each part means.

The file starts with: `---`. This is a requirement for YAML to interpret the file as a proper document.

Items that begin with a ```-``` are considered as list items. Items have the format of ```key: value``` where value can be a simple string or a sequence of other items.

At the top level we have a "name" tag. This is the **unique identifier** of the synapse. It must be an unique word with the only accepted values : alphanumerics and dash. ([a - zA - Z0 - 9\-])
```
- name: "Say-hello"
```


The first part, called **signals** is a list of input actions. This works exactly the same way as neurons. You must place here at least one action.
In the following example, we use just one signal, an order. See the complete list of [available signals](signals.md) here.
```
signals:
  - order: "say-hello"
```

You can add as many orders as you want for the signals. Even if literally they do not mean the same thing (For example order "say hello" and order "adventure" or whatever) as long they are in the same synaps, they will trigger the same action defined in neurons. 

Note that you are not limited by the exact sentence you put in your order. Kalliope uses the matching, it means that you can pronounce the sentence which contains your order (so, can be much longer) and it will lauch an attached task anyway. In this example, the task attached to order "say hello" will be launched even if you say
- "say hello Kalliope"
- "Kalliope, say hello"
- "I want you to say hello"
- "i say goodbye you say hello"
- "whatever I say as long it contains say hello"

To know if your order will be triggered by Kalliope, we recommend you to [use the GUI](kalliope_cli.md) for testing your STT engine.

>**Note:**
You must pay attention to define the orders as precise as possible. As Kalliope is based on matching, if you define your orders in different synapses too similiary, Kalliope risks to trigger more actions that you were expecting. For exemple, if you define two different synapses as shown below:
```
- name: "Say-hello"
  signals:
    - order: "say hello"
```
and 
```
- name: "Say-something"
  signals:
    - order: "say"
```
When you will pronounce "say hello", it will trigger both synapses. 

Then we have the neurons declaration. Neurons are modules that will be executed when the input action is triggered. You can define as many neurons as you want to the same input action (for example: say somethning, then do something etc...). This declaration contains a list (because it starts with a "-") of neurons
```
neurons:
    - neuron_1_name
    - neuron_2_name
    - another_neuron
```

The order of execution of neurons is defined by the order in which they are listed in neurons declaration.

Some neurons need parameters that can be passed as arguments following the syntax bellow:
```
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```
Note here that parameters are indented with one tabulation bellow the neuron's name (YAML syntax requirement).

In this example, the neuron called "say" will make Kalliope speak out loud the sentence in parameter **message**.
See the complete list of [available neurons](neuron_list.md) here.

## Manage synapses

Kalliope provides also a REST API to manage your synapses (get the list, get one, run one), refer to [rest api documentation](rest_api.md) for more details.


## Split the brain

If you want a better visibly, or simply sort your actions in different files, you can split the main brain file into multiple ones.

To do that, use the import statement in the entry brain.yml file with the following syntax:
```
  - includes:
      - path/to/sub_brain.yml
      - path/to/another_sub_brain.yml
```

E.g:
```
  - includes:
      - brains/rolling_shutter_commands.yml
      - brains/find_my_phone.yml
```

>**Note:** You can only use the `include` statement in the main brain file. 

>**Note:** the includes statement must start with a `-`


## The default Synapse

You can provide a default synapse in case none of them are matching when an order is given.
>**Note:** This default synapse is optional.
>**Note:** You need to define it in the settings.yml cf :[Setting](settings.md).

## Next: Start Kalliope
Now you take a look into the [CLI documentation](kalliope_cli.md) to learn how to start kalliope


