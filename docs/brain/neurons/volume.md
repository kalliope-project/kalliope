Update the volume

## Input parameters

| parameter | required | type   | default | choices         | comment                                                                            |
|:----------|:---------|:-------|:--------|:----------------|:-----------------------------------------------------------------------------------|
| level     | yes      | int    | None    |                 | The volume level to set or increase or decrease depending of the selected 'action' |
| action    | no       | string | set     | set,raise,lower | The action to apply to the volume                                                  |

Action type:

- **set:** set the 'level' value as new volume level
- **raise:** increase the current volume level with the value provided in 'level'
- **lower:** decrease the current volume level with the value provided in 'level'

## Returned values

| name          | description                            | type   | sample |
|:--------------|:---------------------------------------|:-------|:-------|
| asked_level   | The level variable sent to the neuron  | int    | 22     |
| asked_action  | The action variable sent to the neuron | string | set    |
| current_level | The current volume level on the system | int    | 50     |


## Synapses example

Set the volume to 50%
```yaml
- name: "set-volume"
  signals:
    - order: "set the volume to 50"
  neurons:
    - volume:
        level: "50"
```

Set the volume dynamically
```yaml
- name: "set-volume-dynamic"
  signals:
    - order: "set the volume to {{ volume }}"
  neurons:
    - volume:
        level: "{{ volume }}"
```
>**Note:** Depending of your STT engine, the caught 'volume' variable can be a string. For example "twenty" instead of "20". 

Raise the volume
```yaml
- name: "raise-volume"
  signals:
    - order: "raise the volume"
  neurons:
    - volume:
        level: "10"
        action: "raise"
```

Reduce the volume
```yaml
- name: "lower-volume"
  signals:
    - order: "reduce the volume"
  neurons:
    - volume:
        level: "10"
        action: "lower"
```
