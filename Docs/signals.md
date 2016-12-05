# Signals

A signal is an input event triggered by a synapse. When a signal is caught, Kalliope runs attached neurons of the synapse. The signal can be of two types: order and event.

The syntax is the following
```
signals:
    - signal_type: parameter
```

## Order

An **order** signal is a word, or a sentence caught by the microphone and processed by the STT engine.

Syntax:
```
signals:
    - order: "<sentence>"
```

Example:
```
signals:
    - order: "please do this action"
```

> **Important note:** SST engines can misunderstand what you say, or translate your sentence into text containing some spelling mistakes.
For example, if you say "Kalliope please do this", the SST engine can return "caliope please do this". So, to be sure that your speaking order will be correctly caught and executed, we recommend you to test your STT engine by using the [Kalliope GUI](kalliope_cli.md) and check the returned text for the given order.

> **Important note:** Kalliope will try to match the order in each synapse of its brain. So, if an order of one synapse is included in another order of another synapse, then both synapses tasks will be started by Kalliope.

> For example, you have "test my umbrella" in a synapse A and "test" in a synapse B. When you'll say "test my umbrella", both synapse A and B
will be started by Kalliope. So keep in mind that the best practice is to use really different sentences with more than one word for your order.

## Event

An event is a way to schedule the launching of a synapse periodically at fixed times, dates, or intervals.

The event system is based on [APScheduler](http://apscheduler.readthedocs.io/en/latest/modules/triggers/cron.html) which it is itself based on [Linux crontab](https://en.wikipedia.org/wiki/Cron). 
When you declare an event in the signal, Kalliope will schedule the launching of the target synapse.

The syntax of an event declaration in a synapse is the following
```
signals:
  - event:
      parameter1: "value1"
      parameter2: "value2"
```

For example, if we want Kalliope to run the synapse every day a 8:30, the event will be declared like this:
```
- event:
    hour: "8"
    minute: "30"
```

### Parameters
Parameters are keyword you can use to build your event

List of available parameter:

| parameter   | required | default | choices                                                         | comment   |
|-------------|----------|---------|-----------------------------------------------------------------|-----------|
| year        | no       | *       | 4 digit                                                         | E.g: 2016 |
| month       | no       | *       | month (1-12)                                                    |           |
| day         | no       | *       | day of the (1-31)                                               |           |
| week        | no       | *       | ISO week (1-53)                                                 |           |
| day_of_week | no       | *       | number or name of weekday  (0-6 or mon,tue,wed,thu,fri,sat,sun) | 6=Sunday  |
| hour        | no       | *       | hour (0-23)                                                     |           |
| minute      | no       | *       | minute (0-59)                                                   |           |
| second      | no       | *       | second (0-59)                                                   |           |

> **Note:** You must set at least one parameter from the list of parameter

### Expression 
Expressions can be used in value of each parameter. Multiple expression can be given in a single field, separated by commas.

| Expression | Field | Description                                                                             |
|------------|-------|-----------------------------------------------------------------------------------------|
| *          | any   | Fire on every value                                                                     |
| */a        | any   | Fire every `a` values, starting from the minimum                                        |
| a-b        | any   | Fire on any value within the `a-b` range (a must be smaller than b)                     |
| a-b/c      | any   | Fire every c values within the `a-b` range                                              |
| xrd y      | day   | Fire on the `x` -rd occurrence of weekday `y` within the month                          |
| last x     | day   | Fire on the last occurrence of weekday `x` within the month                             |
| last x     | day   | Fire on the last day within the month                                                   |
| x,y,z      | day   | Fire on any matching expression; can combine any number of any of the above expressions |


### Examples

#### Web clock radio

Let's make a complete example. We want Kalliope to wake us up each morning of working day (Monday to friday) at 7:30 AM and:
- Wish us good morning
- Give us the time
- Play our favourite web radio

The synapse in the brain would be
```
  - name: "wake-up"
    signals:
      - event:
          hour: "7"
          minute: "30"
          day_of_week: "1,2,3,4,5"
    neurons:
      - say:
          message:
            - "Good morning"
      - systemdate:
          say_template:
            - "It is {{ hours }} hours and {{ minutes }} minutes"
      - shell: 
          cmd: "mplayer http://192.99.17.12:6410/"
          async: True
```

After setting up an event, you must restart Kalliope
```
python kalliope.py start
```

If the syntax is ok, Kalliope will show you each synapse that it has loaded in the crontab
```
Add synapse name "wake-up" to the scheduler: cron[day_of_week='1,2,3,4,5', hour='7', minute='30']
Event loaded
```

That's it, the synapse is now scheduled and will be started automatically.


####  Make Kalliope say something on the third Friday of June, July, August, November and December at 00:00, 01:00, 02:00 and 03:00
```
- name: "wake-up"
  signals:
    - event:
        day: "3rd fri"        
        month: "6-8,11-12"
        hour: "0-3"        
  neurons:
    - say:
        message:
          - "This is a schedulled sentence"
```