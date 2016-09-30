# Signals

A signal is an input event triggered by a synapse. When a signal is caught, Jarvis run attached neurons of the synapse.

The syntax is the following
```
signals:
    - signal_name: parameter
    - signal_name:
        parameter_1: value
        parameter_2: value
```

## Order

An **order** signal is a word, or a sentence caught by the microphone and processed by the STT engine.

Syntax:
```
signals:
    - order: "sentence"
```

Example:
```
signals:
    - order: "Jarvis please do this"
```

> **Important note:** SST engines can misunderstand what you say, or return a text from the speech you said with some spelling mistake.
For example, if you say "Jarvis please do this", the SST engine can return "JARVICE please do this". The recommended way is to test your STT engine by using the 
[JARVIS GUI](jarvis_cli.md) and see what is the returned text for the given order.

> **Important note:** Jarvis will try to match the order in each declared synapse, if a sentence's order of one synapse is included in another sentence's order of another synapse, then
both synapse task will be started by JARVIS. For example, if you have "test my umbrella" in a synapse A and "test" in a synapse B. When you'll say "test my umbrella", both synapse A and B 
will be started by JARVIS. So keep in mind that is a best practice to use different sentences with more than one word.

## Event

