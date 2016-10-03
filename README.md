# Jarvis

JARVIS is a modular always-on voice controlled personal assistant designed for home automation.

TODO: insert video demo EN
TODO: insert video demo FR

JARVIS can run on a Raspberry Pi and he's multi-lang.

JARVIS is easy-peasy to use, see the hello world
```
  - name: "Hello world"
    neurons:      
      - say:
          message: "Hello world!"
    signals:
      - order: "say hello"
```


## Installation

- [Automated installation](Docs/automated_install.md)
- [Manual installation for developement](Docs/dev_env_install.md)

## Usage

- [Configure default settings](Docs/default_settings.md)
- [Create the brain of your JARVIS](Docs/brain.md)
- [Run JARVIS with CLI](Docs/jarvis_cli.md)

## Neurons

A neuron is a plugin that can be used from your **brain.yml**. 

- See the list of [available neurons](Docs/neurons.md).
- See how to [create your own neuron](Docs/contributing.md).


## Contributing

If you'd like to contribute to JARVIS, please read our [Contributing Guide](Docs/contributing.md), which contains the philosophies to preserve, tests to run, and more. 
Reading through this guide before writing any code is recommended.

- Contribute
- Add [issues and feature requests](../../issues)

## Credits

TODO: Write credits

## License

Copyright (c) 2016. All rights reserved.

JARVIS is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.