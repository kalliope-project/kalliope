# Deaf

## Synopsis

Deaf control of kalliope. If set to True the trigger process will be stopped.

Once this neuron is used, and Kalliope deaf, the hotword is deactivated. Only ways to undeaf are:
- by calling the API (see [deaf section](../../../Docs/rest_api.md#switch-deaf-status))
- If running on Raspberry, by using the undeaf button. (See the section [Raspberry LED and deaf button](../../../Docs/settings.md#raspberry-led-and-deaf-button))
- by using another signals than a "vocal order" that call back this neuron with a status set to "False"
- Restarting Kalliope

## Options

| parameter | required | type    | default | choices     | comment                                           |
|-----------|----------|---------|---------|-------------|---------------------------------------------------|
| status    | YES      | Boolean |         | True, False | If "True" Kalliope will stop the hotword process  |


## Return Values

Not returned values

## Synapses example

Deaf Kalliope from a vocal order
```yml
- name: "deaf-synapse"
  signals:
    - order: "stop listening"
  neurons:
    - say:
        message:
          - "I stop hearing you, sir"
    - deaf:
        status: True
```

Undeaf Kalliope from another signals. In the following example, a MQTT message is received
```yml
- name: "undeaf-synapse"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        topic: "/my/sensor"
  neurons:
    - deaf:
        status: False
    - say:
        message:
          - "Waiting for orders, sir"
```
