# neurotransmitter

## Synopsis

Link synapses together. Call a synapse directly or depending on the captured speech from the user.

## Installation

CORE NEURON : No installation needed.  

## Options

| parameter        | required | default | choices | comment                                                                                           |
|------------------|----------|---------|---------|---------------------------------------------------------------------------------------------------|
| from_answer_link | NO       |         |         | Link a synapse depending on the answer of the user. Contain a list of tuple synapse/answer object |
| direct_link      | NO       |         |         | Direct call to a synapse by the name of this one                                                  |
| synapse          | NO       |         |         | Name of the synapse to launch if the captured audio from the STT is present in the answer list    |
| answers          | NO       |         |         | List of sentences that are valid for running the attached synapse                                 |
| default          | NO       |         |         | Name of the synapse to launch if the captured audio doesn't match any answers                     |

## Return Values

None

## Synapses example

We call another synapse directly at the end of the first synapse
```
- name: "direct-link"
    signals:
      - order: "direct link"
    neurons:
      - say:
          message: "I launch directly the synapse number 1"
      - neurotransmitter:
          direct_link: "synapse-1"

  - name: "synapse-1"
    signals:
      - order: "synapse-direct-link-1"
    neurons:
      - say:
          message: "Synapse 1 launched"
```


Here the synapse will ask the user if he likes french fries. If the user answer "yes" or "maybe", he will be redirected to the synapse2 that say something.
If the user answer no, he will be redirected to another synapse that say something else.
If the user say something that is not present in `answers`, he will be redirected to the synapse4.

```
 - name: "synapse1"
    signals:
      - order: "ask me a question"
    neurons:
      - say:
          message: "do you like french fries?"
      - neurotransmitter:
          from_answer_link:
            - synapse: "synapse2"
              answers:
                - "absolutely"
                - "maybe"
            - synapse: "synapse3"
              answers:
                - "no at all"
          default: "synapse4"

  - name: "synapse2"
    signals:
      - order: "synapse2"
    neurons:
      - say:
          message: "You like french fries!! Me too! I suppose..."

  - name: "synapse3"
    signals:
      - order: "synapse3"
    neurons:
      - say:
          message: "You don't like french fries. It's ok."
      
  - name: "synapse4"
    signals:
      - order: "synapse4"
    neurons:
      - say:
          message: "I haven't understood your answer"
```


Neurotransmitter also uses parameters in answers. You can provide parameters to your answers so they can be used by the synapse you are about to launch.
/!\ The params defined in answers must match with the expected "args" params in the target synapse, otherwise an error is raised.

```

  - name: "synapse5"
    signals:
      - order: "give me the weather"
    neurons:
      - say:
          message: "which town ?"
      - neurotransmitter:
          from_answer_link:
            - synapse: "synapse6"
              answers:
                - "the weather in {{ location }}"

  - name: "synapse6"
    signals:
      - order: "What is the weather in {{ location }}"
    neurons:
      - openweathermap:
          api_key: "your-api"
          lang: "fr"
          temp_unit: "celsius"
          country: "FR"
          args:
            - location
          say_template:
          - "Today in {{ location }} the weather is {{ weather_today }} with {{ temp_today_temp }} celsius"
```

## Notes
> When using the neuron neurotransmitter, you must set a `direct_link` or a `from_answer_link`, no both at the same time.

