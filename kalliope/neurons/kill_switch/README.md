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
    signals:
      - order: "goodbye"
    neurons:
      - kill_switch    
```


## Notes

