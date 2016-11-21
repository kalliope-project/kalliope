# sleep

## Synopsis

This neuron sleeps the system for a given time in seconds.

## Options

| parameter | required | default | choices | comment                         |
|-----------|----------|---------|---------|---------------------------------|
| seconds   | YES      |         |         | The number of seconds to sleep. |

## Return Values

No returned values

## Synapses example

Simple example : 

```
  - name: "run-simple-sleep"
    signals:
      - order: "Wait for me "
    neurons:
      - sleep:
          seconds: 60
```


## Notes

