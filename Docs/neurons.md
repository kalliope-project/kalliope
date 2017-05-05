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
  - name: "say-hello"
    signals:
      - order: "say hello to {{ name }}"
    neurons:
      - say:
          message:
            - "Hello {{ name }}"
```

Here, the spoken value captured by the TTS engine will be passed as an argument to the neuron in every parameters that want use it.

Example, with the synapse declaration above, if you say "say hello to Bob". The parameter parameter message is instantiated and all `{{ name }}` are replaced by "bob".
We recommend the reading of the [signals documentation](signals.md) for a complete understanding of how arguments in a neuron work.
> **Note:** If a parameter of a neuron is waiting for a variable from the order and this variable haven't been found in the spoken order, then the neuron is not launched.

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

For each neuron, you can override some parameters to use a specific configuration instead of the default one set in [settings.yml](settings.md) file.

### TTS

You can override the default tts configuration like the TTS engine to use and its parameters like the language, api key or the cache.
By default Kalliope uses a cache to save a generated audio from a TTS engine.
This cache is useful to manage sentences that are not suppose to be changed very often. For example, the following sentence will not change in time, so it's more optimized to generate it once and to keep it in cash:
```yml
- say:
    message:
      - "Hello, sir"
```

In some cases, especially when the neuron is based on a template, the generated audio will change on each new call of the neuron and so the usage of a cache is not necessary. The best example of the case like this is the `systemdate` neuron. As the time changes every minute, the generated audio will change too and so, saving the generated audio in the cache is useless. In this case, you can override the cache usage for this neuron:
Here are my default TTS settings in my `settings.yml` file
```yml
default_text_to_speech: "pico2wave"

text_to_speech:
  - pico2wave:
      language: "fr-FR"
      cache: True
```

And this is how I override only the cache parameter. 
```yml
- systemdate:
    say_template:
      - "It's {{ hours }} hour and {{ minutes }} minute"
    tts:
      pico2wave:
        cache: False
```

You can override all parameter for each neurons like in the example bellow
```yml
- name: "say-something-in-spanish"
    signals:
      - order: "Say hello in spanish"
    neurons:
      - say:
          message:
            - "Buenos dias"
          tts:             
            pico2wave:
              language: "es-ES"
              cache: False
```

>**Note:** The TTS must has been configured with its required parameters in the settings.yml file to be overridden. See [TTS documentation](tts.md).

