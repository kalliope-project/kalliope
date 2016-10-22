# shell

## Synopsis

This neuron runs a script located on the Kalliope system.

## Options

| parameter | required | default | choices | comment                             |
|-----------|----------|---------|---------|-------------------------------------|
| path      | YES      |         |         | The path of the script to execute.  |

## Return Values

No returned values

## Synapses example

Simple example : 

```
  - name: "run-simple-script"
    neurons:
      - script:
          path: "/path/to/script.sh"
    signals:
      - order: "Run the script"
```


## Notes

> **Note:** Kalliope must have the rights to run the script.
> **Note:** Kalliope can be used to grant access to an user with lower rights ... !
