# Debug

## Synopsis

Print a message in the console. This neuron can be used to check your [captured variable from an order](../../Docs/neurons.md#input-values) or check the content of variable placed 
in [Kalliope memory](../../Docs/neurons.md#kalliope_memory-store-in-memory-a-variable-from-an-order-or-generated-from-a-neuron).

## Installation

CORE NEURON : No installation needed.  

## Options

| parameter | required | default | choices | comment                                  |
|-----------|----------|---------|---------|------------------------------------------|
| message   | YES      |         |         | Message to print in the console output   |

## Return Values

No returned values

## Synapses example

Simple example : 
```yml
- name: "debug"
  signals:
    - order: "print a debug"
  neurons:
    - debug:
        message: "this is a debug line"     
```

Output example:
```
[Debug neuron, 2017-12-17 17:30:53] this is a debug line
```

Show the content of captured variables from the spoken order
```yml
- name: "debug"
  signals:
    - order: "tell me what I say {{ here }}"
  neurons:
    - debug:
        message: "{{ here }}"     
```

Show the content of a variable placed in Kalliope memory
```yml
- name: "debug"
  signals:
    - order: "what time is it?"
  neurons:
    - systemdate:
        say_template:
          - "It' {{ hours }} hours and {{ minutes }} minutes"
        kalliope_memory:
          hours_when_asked: "{{ hours }}"
          minutes_when_asked: "{{ minutes }}"   
    - debug:
        message: "hours: {{ kalliope_memory['hours_when_asked']}}, minutes: {{ kalliope_memory['minutes_when_asked']}}"
```
