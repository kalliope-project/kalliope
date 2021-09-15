Update your brain from a neuron

Current actions available:

- enable / disable a synapse from the brain

## Input parameters

| parameter    | required | type    | default | choices     | comment                            |
| ------------ | -------- | ------- | ------- | ----------- | ---------------------------------- |
| synapse_name | YES      | string  |         |             | The name of the synapse to update. |
| enabled      | YES      | boolean |         | True, False | if True, the synapse is enabled.   |

## Returned values

| Name         | Description               | Type    | sample                     |
| ------------ | ------------------------- | ------- | -------------------------- |
| synapse_name | The updated synapse name  | string  | to-deactivate              |
| status       | New status of the synapse | boolean | enabled, disabled, unknown |

## Synapses example

```yaml
- name: "to-deactivate"
  signals:
    - order: "who are you"
  neurons:
    - say:
        message: "I'm Kalliope"

- name: "deactivate"
  signals:
    - order: "deactivate a synapse"
  neurons:
    - brain:
        synapse_name: "to-deactivate"
        enabled: False

- name: "activate"
  signals:
    - order: "active back the synapse"
  neurons:
    - brain:
        synapse_name: "to-deactivate"
        enabled: True
```

## Notes

> **Note:** Changes made to the brain from this neuron are not persistent. The brain will be loaded again following the yaml file at the next start of Kalliope.
