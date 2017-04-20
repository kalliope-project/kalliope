# Neurons

A neuron is a plugin that performs a specific action. You use it to create a synapse.
You can add as many neurons as you want to a synapse. The neurons are executed one by one when the input order is triggered.
If you want to install a community neuron, see the [neuron list documentation](neuron_list.md).

## Usage
Neurons are declared in the `neurons` section of a synapse in your brain file.
The `neurons` section is a list (because it starts with a "-") which contains neuron modules names
```yml
neurons:
    - neuron_1_name
    - neuron_2_name
    - another_neuron
```

Some neurons need parameters that can be passed as arguments following the syntax bellow:
```yml
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```
> **note:** parameters are indented with two spaces bellow the neuron's name following the YAML syntax.

> **note:** Kalliope will try to load the neuron from your resources directory, then from core neuron packages.

To know the list of required parameters, check of documentation of the neuron.
Full list of [available neuron here](neuron_list.md)

## Input values

Neurons require some **parameters** from the synapse declaration to work. Those parameters, also called arguments, can be passed to the neuron in two way:
- from the neuron declaration
- from global variables
- from the captured order

From the neuron declaration:
```yml
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```

From global variables: (cf: [settings.md](settings.md))
```yml
  - name: "run-simple-sleep"
    signals:
      - order: "Wait for me "
    neurons:
      - sleep:
          seconds: {{variable}}
```

From the captured order:
```yml
  - name: "run-neuron-with-parameter-in-order"
    signals:
      - order: "this is an order with the parameter {{ parameter3 }}"
    neurons:
      - neuron_name:
          parameter1: "value1"
          parameter2: "value2"
          args:
          - parameter3
```

Here, the spoken value captured by the TTS engine will be passed as an argument to the neuron in the variable named `parameter3`.

Example, with the synapse declaration above, if you say "this is an order with the parameter Amy Winehouse". The neuron will receive a parameter named `parameter3` with "Amy Winehouse" as a value of this parameter.
We recommend the reading of the [signals documentation](signals.md) for a complete understanding of how arguments in a neuron work.


## Output values

Some neurons will return variables into a dictionary of value. Those values can be used to make your own Kalliope answer through a template.
The objective of using a template is to let the user choosing what he wants to make Kalliope saying in its own language.
A template is a text file that contains **variables**, which get replaced with values when the template is evaluated by 
the [template engine](https://en.wikipedia.org/wiki/Jinja_(template_engine)), and **tags**, which control the logic of the template.

The template engine used in Kalliope is [Jinja2](http://jinja.pocoo.org/docs/dev/).

For example, if we look at the [documentation of the neuron systemedate](../kalliope/neurons/systemdate/README.md), we can see that the neuron will return a dictionary of value like `minute`, `hours` and all other values about the current time on the system where Kalliope is installed.

A simple, that only use **variables**, template would be
```
It is {{ hours }} and {{ minutes }} minutes.
```

Placed in a complete synapse, it looks like the following
```yml
- name: "time"
    signals:
      - order: "what time is it"
    neurons:
      - systemdate:
          say_template:
            - "It is {{ hours }} hours and {{ minutes }} minutes"
```

Here, we use [variables](http://jinja.pocoo.org/docs/dev/templates/#variables) from the neuron into our template file. Both variables will be interpreted by the template engine. 
So, what the user will hear is something like `It is 9 hours and 21 minutes`.

We can add some logic to a template with tags. Here a simple example with [a test tag](http://jinja.pocoo.org/docs/dev/templates/#if), that will make Kalliope change the pronounced sentence depending on the current time.
```
{% if hours > 8 %}
    It is late, isn't it?
{% else %}
    We still have time
{% endif %}
```

As this is multi-lines, we can put the content in a file and use a `file_template` instead of a `say_template` for more clarity.
```yml
- name: "time"
    signals:
      - order: "what time is it"
    neurons:
      - systemdate:
          file_template: /path/to/file/template.j2
```


## Overridable parameters

For each neuron, you can override some parameters to use a specific configuration of TTS instead of the default one 
set in [settings.yml](settings.md) file.

### Cache

You can override the default cache configuration. By default Kalliope uses a cache to save a generated audio from a TTS engine.
This cache is useful to manage sentences that are not suppose to be changed very often. For example, the following sentence will not change in time, so it's more optimized to generate it once and to keep it in cash:
```yml
- say:
    message:
      - "Hello, sir"
```

In some cases, especially when the neuron is based on a template, the generated audio will change on each new call of the neuron and so the usage of a cache is not necessary. The best example of the case like this is the `systemdate` neuron. As the time changes every minute, the generated audio will change too and so, saving the generated audio in the cache is useless. In this case, you can override the cache usage for this neuron:
```yml
- systemdate:
    say_template:
      - "It's {{ hours }} hour and {{ minutes }} minute"
    cache: False
```

### tts

You can override the default tts for each neurons. Just add the "tts" parameter to the neuron like in the example bellow
```yml
neurons:
  - say:
    message:
      - "Hello, sir"
  - say:
    message:
      - "My name is Kalliope"
    tts: "acapela"
```

Here, the first neuron will use the default tts as set in the settings.yml file. The second neuron will use the tts "acapela".

or with new parameters:
```yml
neurons:
  - say:
      message:
        - "Me llamo kalliope"
      tts:
        pico2wave:
          language: "es-ES"
```

Here,  neuron will use the tts "pico2wave" with "es-ES" language.



>**Note:** The TTS must has been configured with its required parameters in the settings.yml file. See [TTS documentation](tts.md).

