# Getting started with Kalliope

Kalliope needs two files to works, a `settings.yml` and a `brain.yml`.
As files are written on YAML syntax, we strongly recommend you to use an editor(IDE) like [VS Code](https://code.visualstudio.com/) or [Atom](https://atom.io/).

If you are using kalliope from a Rpi, the idea would be to configure your assistant from your main computer with an IDE and then push your config folder into your Rpi.

When you start kalliope using the CLI (`kalliope start`), the program will try to load your `settings.yml` and `brain.yml` in the following order:

- From your current folder, E.g `/home/pi/my_kalliope/`
- From `/etc/kalliope/`
- From the default `settings.yml` and `brain.yml` which are located in the root of the Kalliope project tree.

This is a common tree of a Kalliope configuration folder:
```
kalliope_config/
├── brains
│   └── included_brain.yml
├── brain.yml
├── files
│   └── kalliope-EN-13samples.pmdl
└── settings.yml
```

We made starter kits that only needs to be cloned, placed into the Rpi and launched. You'll find the whole list of available start kits on the [Kalliope's website](https://kalliope-project.github.io/starter_kit.html).
Those repositories provide you a structure to start playing and learning basics of Kalliope.
Download the starter kit of your choice and open the folder with your IDE.

All files are expressed in YAML format (see [YAML Syntax](https://learnxinyminutes.com/docs/yaml/)) and has a minimum of syntax, which intentionally tries to not be a programming language or script,
but rather a model of a configuration or a process.

Let's open the main brain file of the English starter kit. You'll see there are some included sub brains file.
```yaml
- includes:
    - brains/say.yml
```

If you open the `say.yml` file from the brains folder, you'll see a basic **synapse** that uses the [neuron](brain/brain.md#neurons) "[Say](brain/neurons/say)" and make Kalliope speaks out loud "Hello sir" when you say "hello".
```yaml
- name: "say-hello-en"
  signals:
    - order: "Hello"
  neurons:
    - say:
        message: "Hello sir"
```

Let's break this down in sections so we can understand how the file is built and what each part means.

Items that begin with a ```-``` are considered as list items. Items have the format of ```key: value``` where value can be a simple string or a sequence of other items.

At the top level we have a "name" tag. This is the **unique identifier** of the synapse. It must be an unique word with the only accepted values : alphanumerics and dash. ([a - zA - Z0 - 9\-])
```yaml
- name: "Say-hello"
```

The first part, called **signals** is a list of input actions.
You can add as many signal as you want in the "signals" section. If one of them is triggered, te neuron list will be executed.
```yaml
signals:
  - order: "say-hello"
```

In the following example, we use just one signal, an "order", but it an can be:

- **an order:** Something that has been spoke out loud by the user.
- **an event:** A date or a frequency (E.G: repeat each morning at 8:30)
- **a mqtt message** A message received on a MQTT topic
- **a geolocation** From the position of your smartphone
- **a community signal** E.g: GPIO signal allow you to trigger actions from a button
- **No signal**. Then the synapse can be only called from another synapse or by the API

Then we have the **neurons** declaration. Neurons are modules that will be executed when the input action(signal) is triggered. You can define as many neurons as you want to the same input action (for example: say something, then do something etc...). This declaration contains a list (because it starts with a "-") of neurons
```yaml
neurons:
  - neuron_1_name
  - neuron_2_name
  - another_neuron
```

The order of execution of neurons is defined by the order in which they are listed in neurons declaration.

Some neurons need parameters that can be passed as arguments following the syntax bellow:
```yaml
neurons:
  - neuron_name:
      parameter1: "value1"
      parameter2: "value2"
```
Note here that parameters are indented with one tabulation bellow the neuron's name (YAML syntax requirement).

In this example, the neuron called "say" will make Kalliope speak out loud the sentence in parameter **message**.

Neurons can be Core (installed by default) or community based (need to be installed).

Time to start Kalliope. Move into the folder and then start Kalliope:
```bash
cd /path/to/the/starter_kit
kalliope start
```
> **Note:** Do not start Kalliope as root user or with sudo

Kalliope will load settings and brain, the output should looks the following
```bash
Starting event manager
Events loaded
Starting Kalliope
Press Ctrl+C for stopping
Starting REST API Listening port: 5000
Waiting for trigger detection
```

Then speak the hotwork out loud to wake up Kalliope (with the right pronunciation depending on your starter kit. "Kalliopé" in french, "Kalliopee" in English, etc..).
If the trigger is successfully raised, you'll see "say something" into the console.
```bash
Say something!
```

Then you can say "hello" and listen the Kalliope response.
```bash
Say something!
Google Speech Recognition thinks you said hello
Order matched in the brain. Running synapse "say-hello"
Waiting for trigger detection
```

That's it! You are ready to customize your assistant!
