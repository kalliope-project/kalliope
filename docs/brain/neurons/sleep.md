
This neuron sleeps the system for a given time in seconds.

## Input parameters

| parameter | required | default | choices | comment                         |
|-----------|----------|---------|---------|---------------------------------|
| seconds   | YES      |         |         | The number of seconds to sleep. |

## Returned values

No returned values

## Synapses example

Simple example :

```yaml
  - name: "run-simple-sleep"
    signals:
      - order: "Wait for me "
    neurons:
      - sleep:
          seconds: 60
```
