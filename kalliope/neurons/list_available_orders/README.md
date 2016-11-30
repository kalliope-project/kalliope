# list_available_orders

## Synopsis

Get the list of available orders

## Options

| parameter            | required | default | choices              | comment                                                                                                          |
|----------------------|----------|---------|----------------------|------------------------------------------------------------------------------------------------------------------|
| ignore_machine_name  | no       |         | 1 if you wish to ignore machine name orders | If 1, orders written with "-" instead of space will be ignored: (eg: Default-response)    |
| query_replace_text   | no       |         | A String                                    | The replacement text for the arguments in order (eg: {{ query }} or {{ location }}        |


## Return Values

| Name      | Description                   | Type          | sample                                                              |
|-----------|-------------------------------|---------------|---------------------------------------------------------------------|
| nb_orders | The number of orders matching | string        | 1, 2 , 10, …                                                        |
| orders    | A list of orders              | lift of string| [lance Steam, lance Cody, mais nous de la musique, musique rock]    |



## Synapses example

This synapse will list all orders except the machine named ones and will replace variable arguments (like {{ query }}) by "and the arguments"
```
  - name: "All-orders"
    signals:
      - order: "what can I ask"
    neurons:
      - list_available_orders:
          query_replace_text: "and the argument"
          ignore_machine_name: 1
          file_template: "templates/en_all_available_orders.j2"
```

## Templates example 

This template will simply make Kalliope speak out loud the number of orders and then all of them
If no order are found, a simple "order not found" sentence will be said by Kalliope.

```
{% if nb_orders > 0 %}
    You have {{ nb_orders }} available orders:
    {% for order in orders %}
        {{ order }}
    {% endfor %}
{% else %}
    No order found.
{% endif %}
```
