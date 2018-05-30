# brain.yml

The brain is a main component of Kalliope. It's a module that gives a configuration of your own personal assistant and, so, determines it's behavior and fonctionnalities.

Kalliope will look for the brain in the order bellow:

- From you current folder, E.g `/home/pi/my_kalliope/brain.yml`
- From `/etc/kalliope/brain.yml`
- From the default `brain.yml` located in the root of the project tree.

Brain is composed by **synapses**: a synapse is the link between input(**signals**) and output actions(**neurons**).

## Signals

### Syntax

A signal is an input event triggered by a synapse. When a signal from the list is caught, Kalliope runs attached neurons of the synapse.

The syntax is the following
```yaml
signals:
  - signal_name: parameter
```

Or
```yaml
signals:
  - signal_name:
      parameter_key1: parameter_value1
      parameter_key2: parameter_value2
```

Example:
```yaml
signals:
  - order: "hello kalliope"
```

```yaml
signals:
  - event:
      hour: "8"
      minute: "30"
```

You can also set an empty list as signals. This means that the synapse can only be started from the CLI, the API, a hook or from another synapse.
```yaml
signals: []
```

### Output parameters

Some signals will send a list of parameters to all neurons when triggered. Neurons are then free to use them or not.
For example, the signal mqtt_subscriber(signals/mqtt_subscriber.md) send a variable called "mqtt_subscriber_message" when triggered. In the example bellow, the neuron "say" use this variable to make Kalliope speak out loud a status received from the MQTT broker.

E.g
```yaml
- name: "mqtt"
  signals:
    - mqtt_subscriber:   # this signal send a "mqtt_subscriber_message" when triggered
        broker_ip: "127.0.0.1"
        topic: "topic1"
  neurons:
    - say:
        message:
          - "The light is now {{ mqtt_subscriber_message }}"
```

### Available signals

Here is a list of core signal that are installed natively with Kalliope

| Name                                                   | Description                                                       |
|--------------------------------------------------------|-------------------------------------------------------------------|
| [event](signals/event)                     | Launch synapses periodically at fixed times, dates, or intervals. |
| [mqtt_subscriber](signals/mqtt_subscriber) | Launch synapse from when receive a message from a MQTT broker     |
| [order](signals/order)                     | Launch synapses from captured vocal order from the microphone     |
| [geolocation](signals/geolocation)         | Define synapses to be triggered by clients handling geolocation   |

See the full list of core and community signals on the [Kalliope's website](https://kalliope-project.github.io/signals_marketplace.html).

## Neurons

A neuron is a plugin that performs a specific action. You use it to create a synapse.
You can add as many neurons as you want to a synapse. The neurons are executed one by one when one of the input signal is triggered.

### Syntax

Neurons are declared in the `neurons` section of a synapse in your brain file.
The `neurons` section is a list (because it starts with a "-") which contains neuron modules names
```yaml
neurons:
    - neuron_1_name
    - neuron_2_name
    - another_neuron
```

Some neurons need parameters that can be passed as arguments following the syntax bellow:
```yaml
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```

Eg:

> **note:** parameters are indented with two spaces bellow the neuron's name following the YAML syntax.

> **note:** Kalliope will try to load the neuron from your resources directory, then from core neuron packages.

### Input values

Neurons require some **parameters** from the synapse declaration to work. Those parameters, also called arguments, can be passed to the neuron from:

- the neuron declaration
- global variables
- the captured order
- output parameter from a signal
- kalliope memory

From the neuron declaration:
```yaml
neurons:
    - neuron_name:
        parameter1: "value1"
        parameter2: "value2"
```

From global variables: (cf: [settings](../settings/settings.md#global-variables))
```yaml
  - name: "run-simple-sleep"
    signals:
      - order: "Wait for me "
    neurons:
      - sleep:
          seconds: {{variable}}
```

From the captured order:
```yaml
  - name: "say-hello"
    signals:
      - order: "say hello to {{ name }}"
    neurons:
      - say:
          message:
            - "Hello {{ name }}"
```
Here, the spoken value captured by the TTS engine will be passed as an argument to the neuron in every parameters that want use it.

Example, with the synapse declaration above, if you say "say hello to Bob". The parameter message is instantiated and all `{{ name }}` are replaced by "bob".

From parameters sent by a signal(E.g, mqtt subscriber)
```yaml
- name: "mqtt"
  signals:
    - mqtt_subscriber:   # this signal send a "mqtt_subscriber_message" when triggered
        broker_ip: "127.0.0.1"
        topic: "topic1"
  neurons:
    - say:
        message:
          - "The light is now {{ mqtt_subscriber_message }}"
```

> **Note:** If a parameter of a neuron is waiting for a variable from the order and this variable haven't been found in the spoken order, then the neuron is not launched.

### Output values

Some neurons will return variables into a dictionary of value. Those values can be used to make your own Kalliope answer through a template.
The objective of using a template is to let the user choosing what he wants to make Kalliope saying in its own language.
A template is a text file that contains **variables**, which get replaced with values when the template is evaluated by
the [template engine](https://en.wikipedia.org/wiki/Jinja_(template_engine)), and **tags**, which control the logic of the template.

The template engine used in Kalliope is [Jinja2](http://jinja.pocoo.org/docs/dev/).

For example, if we look at the [documentation of the neuron systemedate](neurons/systemdate.md), we can see that the neuron will return a dictionary of value like `minute`, `hours` and all other values about the current time on the system where Kalliope is installed.

A simple, that only use **variables**, template would be
```
It is {{ hours }} and {{ minutes }} minutes.
```

Placed in a complete synapse, it looks like the following
```yaml
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
```jinja2
{% if hours > 8 %}
    It is late, isn't it?
{% else %}
    We still have time
{% endif %}
```

As this is multi-lines, we can put the content in a file and use a `file_template` instead of a `say_template` for more clarity.
```yaml
- name: "time"
    signals:
      - order: "what time is it"
    neurons:
      - systemdate:
          file_template: /path/to/file/template.j2
```

### kalliope_memory

Kalliope can store in a short term memory a variable from an order or generated from a neuron:
- output parameters from a neuron
- variable parameters captured from an order.

Stored parameters can then be used in other synapses during a future call.
Please not that this memory is not preserved after a restart of Kalliope.

#### Store parameters generated by a neuron

Syntax with output parameters from a neuron
```yaml
- name: "synapse-name"
  signals:
    - order: "my order"
  neurons:
    - neuron_name:
        kalliope_memory:
          key_name_in_memory: "{{ output_variable_from_neuron }}"
          other_key_name_in_memory: "{{ other_output_variable_from_neuron }}"
```

Syntax to reuse memorized parameters in another synapse
```yaml
- name: "synapse-name"
  signals:
    - order: "an order"
  neurons:
    - neuron_name:
        parameter1: "{{ kalliope_memory['key_name_in_memory'] }}"
        parameter2: "{{ kalliope_memory['other_key_name_in_memory'] }}"
```

>**Note:** The key name need to be placed into simple quotes


Example with a core neuron like `systemdate`
```yaml
- name: "synapse-name"
  signals:
    - order: "my order"
  neurons:
    - systemdate:
        say_template:
          - "It' {{ hours }} hours and {{ minutes }} minutes"
        kalliope_memory:
          hours_when_asked: "{{ hours }}"
          minutes_when_asked: "{{ minutes }}"
```

Here, the `systemdate` neuron generates variables that haven been passed to the template like described in the previous section and to the memory of Kalliope.

Those parameters can now be used in a next call
```yaml
- name: "synapse-name-2"
  signals:
    - order: "a what time I've asked the time?"
  neurons:
    - say:
        message:
          - "at {{ kalliope_memory['hours_when_asked']}} hours and {{ kalliope_memory['minutes_when_asked']}} minutes"
```

As it's based on a template, the value can be modified by adding a string
```yaml
kalliope_memory:
  my_saved_key: "{{ neuron_parameter_name }} with a word"
```

Multiple parameters can be used and concatenated in the same memorized key
```yaml
kalliope_memory:
  my_saved_key: "{{ neuron_parameter_name1 }} and {{ neuron_parameter_name2 }}"
```

#### Store parameters captured from orders

Syntax
```yaml
- name: "synapse-name"
  signals:
    - order: "my order with {{ variable }}"
  neurons:
    - neuron_name:
        kalliope_memory:
          key_name_in_memory: "{{ variable }}"
```

The syntax to reuse memorized parameters in another synapse is the same as the one used with neuron parameters
```yaml
- name: "synapse-name"
  signals:
    - order: "an order"
  neurons:
    - neuron_name:
        parameter1: {{ kalliope_memory['key_name_in_memory']}}
```

Example
```yaml
- name: "synapse-id"
  signals:
    - order: "say hello to {{ name }}"
  neurons:
    - say:
        message:
          - "Hello {{ name }}"
        kalliope_memory:
          friend: "{{ name }}"
```

Here, the variable "name" has been used directly into the template and also saved in memory behind the key "friend".
The value can now be used in a next call like the following
```yaml
- name: "synapse-id"
  signals:
    - order: "what is the name of my friend?"
  neurons:
    - say:
        message:
          - "It's {{ kalliope_memory['friend'] }}
```

Here is another example brain whit use the `neurotimer` neuron. In this scenario, you want to remember to do something

> **You:** remind me to call mom in 15 minutes<br>
**Kalliope:** I'll notify you in 15 minutes<br>
15 minutes later..<br>
**Kalliope:** You asked me to remind you to call mom 15 minutes ago

```yaml
- name: "remember-synapse"
  signals:
    - order: "remind me to {{ remember }} in {{ time }} minutes"
  neurons:
    - neurotimer:
        seconds: "{{ time }}"
        synapse: "remember-todo"
        kalliope_memory:
          remember: "{{ remember }}"
          seconds: "{{ time }}"
    - say:
        message:
          - "I'll remind you in {{ time }} minutes"

- name: "remember-todo"
  signals: {}
  neurons:
    - say:
        message:
          - "You asked me to remind you to {{ kalliope_memory['remember'] }} {{ kalliope_memory['time'] }} minutes ago"
```

#### Get the last order generated TTS message

Kalliope will save in memory automatically:
- the last generated TTS message .
- the last caught order

To get the last generated message, use the key `{{ kalliope_memory['kalliope_last_tts_message'] }}` in your synapse.
To get the last order, use the key `{{ kalliope_memory['kalliope_last_order'] }}` in your synapse.

Keep in mind that the `kalliope_last_tts_message` variable is overridden every time Kalliope says something.
So you need to catch messages you want to process in the right hook like `on_start_speaking` or `on_stop_speaking`.

An example of usage is to send each message to an API each time Kalliope start speaking.

You need at first to create a hook in your `settings.yaml` like the following
```yaml
hooks:
  on_start_speaking: "mm-say"
```

Then create a synapse in your `brain` that is linked to the hook to send each message.
As a concrete example, here the [magic mirror neuron](https://github.com/kalliope-project/kalliope_neuron_magic_mirror) is used to send each spelt out loud message to the Magic Mirror API in order to show them on the screen.
```yaml
  - name: "mm-say"
    signals: []
    neurons:
      - magic_mirror:
          mm_url: "http://127.0.0.1:8080/kalliope"
          notification: "KALLIOPE"
          payload: "{{ kalliope_memory['kalliope_last_tts_message'] }}"
```

**Note**

`kalliope_last_tts_message` is overridden each time Kalliope says something.
For example, a common practice is to have a synapse placed in the hook `on_triggered` in order to know when the hotword has been triggered.
So, if this synapse is configured like the following
```yaml
- name: "on-triggered-synapse"
  signals: []
  neurons:
    - say:
        message: "what can i do for you?"
```

And you try the get the last generated message with a synapse like the following
```yaml
- name: "last-message"
    signals:
      - order: "what was the last message?"
    neurons:
      - say:
          message: "it was {{ kalliope_memory['kalliope_last_tts_message'] }}"
```

Then the answer will always be "it was what can i do for you?" because the variable `kalliope_last_tts_message` has been overridden during the execution of the `on-triggered-synapse`.

## Split the brain

If you want a better visibly, or simply sort your actions in different files, you can split the main brain file into multiple ones.

To do that, use the import statement in the entry brain.yml file with the following syntax:
```yaml
  - includes:
      - path/to/sub_brain.yml
      - path/to/another_sub_brain.yml
```

E.g:
```yaml
  - includes:
      - brains/rolling_shutter_commands.yml
      - brains/find_my_phone.yml
```

>**Note:** You can only use the `include` statement in the main brain file.

>**Note:** the includes statement must start with a `-`
