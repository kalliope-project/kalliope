# Mute

## Synopsis

Mute control of kalliope. If set to True the trigger process will be stopped.

Once this neuron is used, and Kalliope muted, the hotword is deactivated. Only ways to unmute are:
- by calling the API (see [mute section](../../../Docs/rest_api.md#switch-mute-status))
- If running on Raspberry, by using the unmute button. (See the section [Raspberry LED and mute button](../../../Docs/settings.md#raspberry-led-and-mute-button))
- by using another signals than a "vocal order" that call back this neuron with a status set to "False"
- Restarting Kalliope

## Options

| parameter | required | type    | default | choices     | comment                                           |
|-----------|----------|---------|---------|-------------|---------------------------------------------------|
| status    | YES      | Boolean |         | True, False | If "True" Kalliope will stop the hotword process  |


## Return Values

Not returned values

## Synapses example

Mute Kalliope from a vocal order
```yml
- name: "mute-synapse"
  signals:
    - order: "stop listening"
  neurons:
    - say:
        message:
          - "I stop hearing you, sir"
    - mute:
        status: True
```

Unmute Kalliope from another signals. In the following example, a MQTT message is received
```yml
- name: "unmute-synapse"
  signals:
    - mqtt_subscriber:
        broker_ip: "127.0.0.1"
        topic: "/my/sensor"
  neurons:
    - mute:
        status: False
    - say:
        message:
          - "Waiting for orders, sir"
```
