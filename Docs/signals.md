# Signals

A signal is an input event triggered by a synapse. When a signal is caught, Kalliope runs attached neurons of the synapse.

The syntax is the following
```yml
signals:
    - signal_type: parameter
```

Or
```yml
signals:
    - signal_type:
        parameter_key1: parameter_value1
        parameter_key2: parameter_value2
```

## Available signals

Here is a list of core signal that are installed natively with Kalliope

| Name                                                   | Description                                                       |
|--------------------------------------------------------|-------------------------------------------------------------------|
| [event](../kalliope/signals/event)                     | Launch synapses periodically at fixed times, dates, or intervals. |
| [mqtt_subscriber](../kalliope/signals/mqtt_subscriber) | Launch synapse from when receive a message from a MQTT broker     |
| [order](../kalliope/signals/order)                     | Launch synapses from captured vocal order from the microphone     |
| [geolocation](../kalliope/signals/geolocation)         | Define synapses to be triggered by clients handling geolocation   |
