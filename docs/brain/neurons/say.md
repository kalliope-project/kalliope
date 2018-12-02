This neuron is the mouth of Kalliope and uses the TTS engine defined in your settings to say the given message.

## Input parameters

| parameter | required | default | choices | comment                                                    |
|-----------|----------|---------|---------|------------------------------------------------------------|
| message   | YES      |         |         | A single message or a list of messages Kalliope could say  |
| file_template   | NO      |         |         | Path to a file template to use instead of a message  |
| parameters   | NO      |         |         | A dict of parameters to pass to the file template if used  |

## Returned values

No returned values

## Synapses example

Simple example :

```yaml
- name: "Say-hello"
  signals:
    - order: "hello"
  neurons:
    - say:
        message: "Hello Sir"
```

With a multiple choice list, Kalliope will pick one randomly:

```yaml
- name: "Say-hello"
  signals:
    - order: "hello"
  neurons:
    - say:
        message:
          - "Hello Sir"
          - "Welcome Sir"
          - "Good morning Sir"
```

With an input value
```yaml
- name: "Say-hello-to-friend"
  signals:
    - order: "say hello to {{ friend_name }}"
  neurons:
    - say:
        message: "Hello {{ friend_name }}"
```

With a template
```yaml
- name: "Say-hello-template"
  signals:
    - order: "say hello"
  neurons:
    - say:
        file_template: "say_something.j2" 
        parameters: 
          friend_name: "{{ friend_name }}"
```

Where `say_something.j2` would be
```
Hello sir!
```

With a file template, and passing some variable from the order:
```yaml
- name: "Say-hello-to-friend-template"
  signals:
    - order: "say hello to {{ friend_name }}"
  neurons:
    - say:
        file_template: "my_template.j2" 
        parameters: 
          forwarded_variable_name: "{{ friend_name }}"
```

Where `my_template.j2` would be
```
Hello {{ forwarded_variable_name }}
```

## Notes

> **Note:** The neuron does not return any values.
>
> **Note:** Kalliope randomly takes a message from the list
