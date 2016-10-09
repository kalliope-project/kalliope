# Push notification

## Synopsis

Send broadcast communications to groups of subscribers.

Available client are:
- Android phone
- iOS phone/
- Windows Phone
- Chrome Browser

This neuron is based on [Pushetta API](http://www.pushetta.com/). 
You need to [create a free account](http://www.pushetta.com/accounts/signup/) and a chanel before using it.
You need to install a [client App](http://www.pushetta.com/pushetta-downloads/) on the target device.

## Options

| parameter    | requiered | default | choices | comment                                                                                               |
|--------------|-----------|---------|---------|-------------------------------------------------------------------------------------------------------|
| message      | yes       |         |         | Message that will be send to the android phone                                                        |
| api_key      | yes       |         |         | Token API key availlable from [Pushetta dashboard](http://www.pushetta.com/my/dashboard/) |
| channel_name | yes       |         |         | Name of the subscribed [channel](http://www.pushetta.com/pushetta-docs/#create)                       |


## Return Values

No returned value


## Synapses example

The following synapse will send a push message to device that have subscribed to the channel name "my_chanel_name" when you say "push message".
```
 - name: "Send push message"
    neurons:
      - android_pushetta:
           message: "Message to send"
           api_key: "TOEKENEXAMPLE1234"
           channel_name: "my_chanel_name"
    signals:
      - order: "push message"
```

## Notes

> **Note:** You must install a [client App](http://www.pushetta.com/pushetta-downloads/) on the target device.

> **Note:** You must create a channel an get a token key on [Pushetta website](http://www.pushetta.com/) before using the neuron.
