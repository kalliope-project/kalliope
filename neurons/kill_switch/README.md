# kill_switch

## Synopsis

This neuron exits the Kalliope process.

## Options

No parameters

## Return Values

No returned values

## Synapses example

Simple example : 

```
  - name: "stop-kalliope"
    neurons:
      - kill_switch
    signals:
      - order: "goodbye"
```


## Notes

