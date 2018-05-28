Send a message to all signals launched in Kalliope to update their behavior.
The message will be interpreted by all signals that support notification.
All supported notification type are documented in each Signals.

A basic example of usage is to [disable the trigger from the Order signal](../signals/order#control-from-the-signal-neuron) to create an interactive mode where you can chain orders without having to wake up Kalliope with the hotword.

## Input parameters

| parameter    | required | type   | default | choices | comment                                                                                                  |
| ------------ | -------- | ------ | ------- | ------- | -------------------------------------------------------------------------------------------------------- |
| notification | YES      | string |         |         | The notification string identifier that will be recognized by launched signals                           |
| payload      | NO       | dict   |         |         | Dict of parameters to send with the notification. The payload must match the target Signal documentation |


## Synapse examples

Syntax:
```yaml
- name: "my-synapse"
  signals: {}
  neurons:
    - signals:
        notification: "notification_name"
        payload:
          key1: "value1"
          key2: "value2"
```

E.g:
```yaml
- name: "start-skip-trigger"
  signals: {}
  neurons:
    - signals:
        notification: "skip_trigger"
        payload:
          status: "True"
```

## Concrete example

See a complete example from the [order signal documentation](../signals/order#control-from-the-signal-neuron).

## How to implement notifications in my community signals

You Signal will implement 2 classes, SignalModule and Thread.

- SignalModule is used to implement methods like notification
- Thread is used to keep the signal awaken during the Kalliope process execution.

Here is a basic implementation of a signal.
```python
class Mysignal(SignalModule, Thread):
    def __init__(self):
        super(Mysignal, self).__init__()
        Thread.__init__(self, name=Mysignal)

    def run:
        # do my signal job
```

Now, to implement notification, add the `on_notification_received`

```python
class Mysignal(SignalModule, Thread):
    def __init__(self):
        super(Mysignal, self).__init__()
        Thread.__init__(self, name=Mysignal)

    def run:
        # do my signal job

    def on_notification_received(self, notification=None, payload=None):
        logger.debug("[My_signal] received notification, notification: %s, payload: %s" % (notification, payload))
        if notification == "notification_that_I_care":
            # do stuff with payload
```
