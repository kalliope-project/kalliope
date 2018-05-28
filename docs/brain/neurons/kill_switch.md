This neuron exits the Kalliope process.

## Input parameters

No parameters

## Returned values

No returned values

## Synapses example

Simple example :
```yaml
  - name: "stop-kalliope"
    signals:
      - order: "goodbye"
    neurons:
      - kill_switch
```
