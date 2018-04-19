# Kalliope quick start

Kalliope needs two files to works, a `settings.yml` and a `brain.yml`.
As files are written on YAML syntax, we strongly recommend you to use an editor(IDE) like [VS Code](https://code.visualstudio.com/) or [Atom](https://atom.io/).

If you are using kalliope from a Rpi, the idea would be to configure your assistant from your main computer with an IDE and then push your config folder into your Rpi.

We made starter kits that only needs to be cloned, placed into the Rpi and launched. You'll find the whole list of available start kits on the [Kalliope's website](https://kalliope-project.github.io/starter_kit.html).

Those repositories provide you a structure to start playing and learning basics of Kalliope.
Download the starter kit of your choice and open the folder with your IDE.

When you start kalliope using the CLI (`kalliope start`), the program will try to load your `settings.yml` and `brain.yml` in the following order:
- From your current folder, E.g `/home/pi/my_kalliope/settings.yml`
- From `/etc/kalliope/settings.yml`
- From the default `settings.yml`. You can take a look into the default [`settings.yml`](../kalliope/settings.yml) file which is located in the root of the project tree.

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

Let's open the main brain file. You'll see there are some included sub brains file.
```yml
- includes:
    - brains/say.yml
```

If you open the `say.yml` file from the brains folder, you'll see a basic synapse that uses the [neuron](../neurons.md) "[Say](../../kalliope/neurons/say)" and make Kalliope speaks out loud "Hello sir" when you say "hello".
Move into the folder and then start Kalliope:
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

Then speak the hotwork out loud to wake up Kalliope (with the right pronunciation depending on your starter kit. "Kalliopé" in french, "Kalliopee" in English).
If the trigger is successfully raised, you'll see "say something" into the console.
```bash
2016-12-05 20:54:21,950 :: INFO :: Keyword 1 detected at time: 2016-12-05 20:54:21
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

## What next?

- See what you can customize in your [settings](../settings.md) like changing the hotword, the STT or TTS engine.
- Create your [brain](../brain.md)
- See the list of [available neurons](../neuron_list.md)
