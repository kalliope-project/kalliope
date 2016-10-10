# Signals

A signal is an input event triggered by a synapse. When a signal is caught, Kalliope run attached neurons of the synapse.

The syntax is the following
```
signals:
    - signal_name: parameter
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

> **Important note:** SST engines can misunderstand what you say, or return a text from the speech you said with some spelling mistake.
For example, if you say "Kalliope please do this", the SST engine can return "caliope please do this". The recommended way is to test your STT engine by using the
[Kalliope GUI](kalliope_cli.md) and see what is the returned text for the given order.

> **Important note:** Kalliope will try to match the order in each synapse of his brain, if an order of one synapse is included in another order of another synapse, then both synapse task will 
be started by Kalliope.

> For example, if you have "test my umbrella" in a synapse A and "test" in a synapse B. When you'll say "test my umbrella", both synapse A and B
will be started by Kalliope. So keep in mind that is a best practice to use different sentences with more than one word.

## Event

An event is a way to schedule the launching of a synapse periodically at fixed times, dates, or intervals.

The event system is based on [Linux crontab](https://en.wikipedia.org/wiki/Cron). A crontab is file that specifies shell commands to run periodically
 on a given schedule.
When you declare an event in the brain, Kalliope will load the crontab file for you for scheduling the launching 
of the  target synapse.

The syntax of an event declaration in a synapse is the following
```
signals:
      - event: "<contab period>"
```

Where a crontab period use the syntax bellow
```
 ┌───────────── min (0 - 59)
 │ ┌────────────── hour (0 - 23)
 │ │ ┌─────────────── day of month (1 - 31)
 │ │ │ ┌──────────────── month (1 - 12)
 │ │ │ │ ┌───────────────── day of week (0 - 6) (0 to 6 are Sunday to
 │ │ │ │ │                  Saturday, or use names; 7 is also Sunday)
 │ │ │ │ │
 │ │ │ │ │
 * * * * *  
```

For example, if we want Kalliope to run the synapse every day a 8 PM. The event would be
```
- event: "0 20 * * *"
```

Let make a complete example. We want Kalliope to wake us up each morning of working day (Monday to friday) at 7 AM and:
- Wish us good morning
- Give us the our
- Play our favourite web radio

The synapse in the brain would be
```
  - name: "wake up"
    neurons:
      - say:
          message:
            - "Good morning"
      - systemdate:
          say_template:
            - "It is {{ hours }} hours and {{ minutes }} minutes"
      - command: "mplayer http://192.99.17.12:6410/"
    signals:
      - event: "0 7 * * 1,2,3,4,5"
```

After setting up an event, you must restart Kalliope
```
python kalliope.py start
```

If the syntax is ok, Kalliope will show you each synapse that he has loaded in the crontab
```
Synapse "wake up" added to the crontab
Event loaded in crontab
```

That's it, the synapse is now scheduled and will be started automatically.