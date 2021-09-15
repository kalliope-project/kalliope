# Welcome to Kalliope's documentation

Kalliope is a framework that will help you to create your own personal assistant.

The concept is to create the [brain](brain/brain.md) of your assistant by attaching an input **signal** (vocal order, scheduled event, MQTT message, GPIO event, etc..) to one or multiple actions called **neurons**.

You can create your own Kalliope bot, by simply choosing and composing the [existing neurons](https://kalliope-project.github.io/neurons_marketplace.html) without writing any code. But, if you need a particular module, you can write it by yourself, add it to your project and propose it to the community.

Kalliope can run on all Linux Debian based distribution including a Raspberry Pi and it's multi-lang. The only thing you need is a microphone.

Kalliope is easy-peasy to use, see the hello world

```yaml
- name: "Hello-world"
  signals:
    - order: "say hello"
  neurons:
    - say:
        message: "Hello world!"
```

If you want an idea of what you can do with Kalliope, click on the image below

<p align="center">
[![ENGLISH DEMO](https://img.youtube.com/vi/PcLzo4H18S4/0.jpg)](https://www.youtube.com/watch?v=PcLzo4H18S4)
</p>
