This neuron runs a script located on the Kalliope system.

## Input parameters

| parameter | required | default | choices | comment                                                                    |
| --------- | -------- | ------- | ------- | -------------------------------------------------------------------------- |
| path      | YES      |         |         | The path of the script to execute                                          |
| async     | NO       | FALSE   |         | If True, Kalliope will not wait for the end of the execution of the script |

## Returned values

Values are only returned by the neuron if the async mode is set to `False`.

| Name       | Description                                                                                            | Type   | sample                        |
| ---------- | ------------------------------------------------------------------------------------------------------ | ------ | ----------------------------- |
| output     | The shell output of the command if any. The command "date" will return "Sun Oct 16 15:50:45 CEST 2016" | string | Sun Oct 16 15:50:45 CEST 2016 |
| returncode | The returned code of the command. Return 0 if the command was succesfuly exectued, else 1              | int    | 0                             |

## Synapses example

Simple example:

```yaml
- name: "run-simple-script"
  signals:
    - order: "Run the script"
  neurons:
    - script:
        path: "/path/to/script.sh"
```

If the script can take a long time and you don't want to block the Kalliope process, you can run it in asynchronous mode.
Keep in mind that you cannot get any returned value with this mode.

```yaml
- name: "run-simple-script"
  signals:
    - order: "Run the script"
  neurons:
    - script:
        path: "/path/to/script.sh"
        async: True
```

Make Kalliope speak out loud the result of the script.

```yaml
- name: "run-script-an-give-output"
  signals:
    - order: "run the script"
  neurons:
    - script:
        path: "/path/to/script.sh"
        say_template: "{{ output }}"
```

Path an argument to the script from your order

```yaml
- name: "run-simple-script-with-input-value"
  signals:
    - order: "Run the script with {{ my_var }}"
  neurons:
    - script:
        path: "/path/to/script.sh {{ my_var }}"
        async: True
```

## Notes

> **Note:** Kalliope must have the rights to run the script.

> **Note:** Kalliope can be used to grant access to an user with lower rights ... !

> **Note:** When 'async' flag is used, returned values are lost
