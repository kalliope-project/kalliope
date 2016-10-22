# neurotransmitter

## Synopsis

Link synapses together. Call a synapse from another one depending on the captured speech from the user.

## Options

| parameter | required | default | choices | comment                                                                                        |
|-----------|----------|---------|---------|------------------------------------------------------------------------------------------------|
| links     | yes      |         |         | List of tuple synapse/answer object                                                            |
| synapse   | yes      |         |         | Name of the synapse to launch if the captured audio from the STT is present in the answer list |
| answers   | yes      |         |         | List of sentences that are valid for running the attached synapse                              |
| default   | yes      |         |         | Name of the synapse to launch if the captured audio doesn't match any answers                  |

## Return Values

None

## Synapses example

Here the synapse will ask the user if he likes french fries. If the user answer "yes" or "maybe", he will be redirected to the synapse2 that say something.
If the user answer no, he will be redirected to another synapse that say something else.
If the user say something that is not present in `answers`, he will be redirected to the synapse4.

```
 - name: "synapse1"
    neurons:
      - say:
          message: "do you like french fries?"
      - neurotransmitter:
          links:
            - synapse: "synapse2"
              answers:
                - "absolutely"
                - "maybe"
            - synapse: "synapse3"
              answers:
                - "no at all"
          default: "synapse4"
    signals:
      - order: "ask me a question"

  - name: "synapse2"
    neurons:
      - say:
          message: "You like french fries!! Me too! I suppose..."
    signals:
      - order: "synapse2"

  - name: "synapse3"
    neurons:
      - say:
          message: "You don't like french fries. It's ok."
    signals:
      - order: "synapse3"
      
  - name: "synapse4"
    neurons:
      - say:
          message: "I havn't understood your answer"
    signals:
      - order: "synapse4"
```



