# neuron_name

## Synopsis

Little description of what the neuron does.

## Installation
```
kalliope install --git-url "https://github.com/my_user/my_neuron.git"
```

## Options

(usage of a [table generator](http://www.tablesgenerator.com/markdown_tables) is recommended)

| parameter        | required | default                       | choices                           | comments                     |
|------------------|----------|-------------------------------|-----------------------------------|------------------------------|
| parameter_name_1 | yes      |                               |                                   | description of the parameter |
| parameter_name_2 | no       |                               | possible_value_1,possible_value_2 | description of the parameter |
| parameter_name_3 | yes      | default_value_if_not_provided |                                   | description of the parameter |


## Return Values

Only necessary when the neuron use a template to say something

| name      | description                        | type       | sample                    |
|-----------|------------------------------------|------------|---------------------------|
| value_key | dictionary containing all the data | dictionary | {"name":"me", "email": 2} |
| value_key | list of value                      | list       | ["val1", "val2", "val3"]  |
| value_key | string value                       | string     | "2"                       |


## Synapses example

Description of what the synapse will do
```
 - name: "type here your name"
   signals:
     - order: "this is what I have to say to run this synapse"
   neurons:      
     - neuron_name:
        parameter: "value"
        parameter: "value"
        file_template: template_name.j2
    
```

## Templates example 

Description of the template
```
This is a var {{ var }} 
{% for item in items %}
 This is the  {{ item }}  
{% endfor %}
```

## Notes

> **Note:** This is an important note concerning the neuron
