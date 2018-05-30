Run a shell command on the local system where Kalliope is installed.

## Input parameters

| parameter | required | default | choices  | comment                                                                     |
|-----------|----------|---------|----------|-----------------------------------------------------------------------------|
| cmd       | yes      |         |          | The shell command to run                                                    |
| async     | no       | False   |          | If True, Kalliope will not wait for the end of the execution of the command |
| query     | no       | False   |          | An argument to send the script.                                             |


## Returned values

Values are only returned by the neuron if the async mode is set to `False`.

| Name       | Description                                                                                           | Type   | sample                        |
|------------|-------------------------------------------------------------------------------------------------------|--------|-------------------------------|
| output     | The shell output of the command if any. The command "date" will retun "Sun Oct 16 15:50:45 CEST 2016" | string | Sun Oct 16 15:50:45 CEST 2016 |
| returncode | The returned code of the command. Return 0 if the command was succesfuly exectued, else 1             | int    | 0                             |


## Synapses example

Simple that will create a file locally
```yaml
  - name: "create-a-local-file"
    signals:
      - order: "touch"
    neurons:
      - shell:
          cmd: "touch ~/test.txt"
```

We want to launch our favorite web radio. This command, which it call mplayer, will block the entire Kalliope process if we
wait for the result unless the mplayer process is killed. So we add `async` flag.
```yaml
  - name: "run-web-radio"
    signals:
      - order: "run web radio"
    neurons:
      - shell:
          cmd: "mplayer http://192.99.17.12:6410/"
          async: True
      - say:
          message: "web radio lanched"
```
>**Note:** If the parameter `async` is set to True, the neuron will not return any values.


Then, we can kill the player process with another synapse
```yaml
  - name: "stop-web-radio"
    signals:
      - order: "stop web radio"
    neurons:
      - shell:
          cmd: "pkill mplayer"
      - say:
          message: "web radio stopped"
```

Make Kalliope add two number and speak out loud the result. Here you should hear "4".
```yaml
  - name: "get-the-result-of-the-addition"
    signals:
      - order: "addition"
    neurons:
      - shell:
          cmd: "echo $(expr \"1\" + \"3\")"
          say_template: "{{ output }}"
```

Let's use a file template. We try to remove the file `~/test.txt` and make Kalliope give us the result depending of the
returned error code.
If the file is present on the system, you will hear "The command has succeeded" and so the file has been deleted.
If you run it a second time, the command will fail as the file is not anymore present and so you should hear
"The command has failed". See the template example bellow.
```yaml
  - name: "remove-a-file"
    signals:
      - order: "remove file"
    neurons:
      - shell:
          cmd: "rm ~/test.txt"
          file_template: remove_file.j2
```

If you want to add argument to your shell command, you can use an input value from your order.
```yaml
  - name: "Delete-a-specific-file"
    signals:
      - order: "remove file {{ query }}"
    neurons:
      - shell:
          cmd: "rm {{ query }}"
          file_template: remove_file.j2
```
In the example above, kalliope will remove the file you asked for in the query.
eg: "remove file test", the executed command will be "rm test"

## Templates example

Template `remove_file.j2` used in the remove file example remove_file.j2
```jinja2
{% if returncode == 0 %}
    The command succeeded
{% else %}
    The command failled
{% endif %}
```

## Notes

> **Note:** If the parameter `async` is set to True, the neuron will not return any values.
