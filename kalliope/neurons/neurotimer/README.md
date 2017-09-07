# Neurotimer

## Synopsis

Run a synapse after a delay.

## Installation

CORE NEURON : No installation needed. 

## Options

| parameter            | required | type   | default | choices   | comment                                                      |
|----------------------|----------|--------|---------|-----------|--------------------------------------------------------------|
| seconds              | NO       | int    |         | value > 0 | Number of second to wait before running the synapse          |
| minutes              | NO       | int    |         | value > 0 | Number of minutes to wait before running the synapse         |
| hours                | NO       | int    |         | value > 0 | Number of hours to wait before running the synapse           |
| synapse              | YES      | string |         |           | Name of the synapse to run after the selected delay          |

## Return Values

None

## Synapses example


**Scenario:** You are used to make a tea and want to know when it's time to remove the bag.
> **You:** remember me to remove the bag of my tea<br>
**Kalliope:** Alright<br>
3 minutes later..<br>
**Kalliope:** your tea is ready

```yml
- name: "tea-bag"
  signals:
    - order: "remember me to remove the bag of my tea"
  neurons:
    - neurotimer:
        minutes: 3
        synapse: "time-over"
    - say:
        message:
          - "Alright"

- name: "time-over"
  signals:
     - order: "no-order-for-this-synapse"
  neurons:
    - say:
        message:
          - "your tea is ready" 
```

If your STT engine return integer when capturing a spoken order, you can set the time on the fly.
**Scenario:** You are starting to cook something
> **You:** notify me in 10 minutes<br>
**Kalliope:** I'll notify you in 10 minutes<br>
10 minutes later..<br>
**Kalliope:** You asked me to notify you

```yml
- name: "timer2"
    signals:
      - order: "notify me in {{ time }} minutes"
    neurons:
      - neurotimer:
          minutes: "{{ time }}"
          synapse: "notify"
      - say:
          message:
            - "I'll notify you in {{ time }} minutes"

- name: "notify"
  signals:
     - order: "no-order-for-this-synapse"
  neurons:
    - say:
        message:
          - "You asked me to notify you" 
```

Passing argument to the called synapse with the `kalliope_memory`.
**Scenario:** You want to remember to do something
> **You:** remind me to call mom in 15 minutes<br>
**Kalliope:** I'll notify you in 15 minutes<br>
15 minutes later..<br>
**Kalliope:** You asked me to remind you to call mom 15 minutes ago
```yml
- name: "remember-synapse"
  signals:
    - order: "remind me to {{ remember }} in {{ time }} minutes"
  neurons:
    - neurotimer:
        seconds: "{{ time }}"
        synapse: "remember-todo"
        kalliope_memory:
          - remember: "{{ remember }}"
          - seconds: "{{ time }}"
    - say:
        message:
          - "I'll remind you in {{ time }} minutes"

- name: "remember-todo"
  signals:
    - order: "no-order-for-this-synapse"
  neurons:
    - say:
        message:
          - "You asked me to remind you to {{ kalliope_memory['remember'] }} {{ kalliope_memory['time'] }} minutes ago"
```


## Notes

> **Note:** When used from the API, returned value from the launched synapse are lost

> **Note:** Not all STT engine return integer.

> **Note:** You must set at least one timer parameter (seconds or minutes or hours). You can also set them all.