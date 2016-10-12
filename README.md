# Kalliope

Kalliope is a modular always-on voice controlled personal assistant designed for home automation.

TODO: insert video demo EN
TODO: insert video demo FR

Kalliope can run on a Raspberry Pi and he's multi-lang.

Kalliope is easy-peasy to use, see the hello world
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

- [Configure default settings](Docs/settings.md)
- [Create the brain of your Kalliope](Docs/brain.md)
- [Run Kalliope with CLI](Docs/kalliope_cli.md)

## Neurons

A neuron is a plugin that can be used from your **brain.yml**. 

- See the list of [available neurons](Docs/neuron_list.md).
- See how to [create your own neuron](Docs/contributing.md).


## Contributing

If you'd like to contribute to Kalliope, please read our [Contributing Guide](Docs/contributing.md), which contains the philosophies to preserve, tests to run, and more. 
Reading through this guide before writing any code is recommended.

- Contribute
- Add [issues and feature requests](../../issues)

## Credits

> **Meaning of Kalliope** Kalliope means "beautiful voice" from Greek καλλος (kallos) "beauty" and οψ (ops) "voice". 
In Greek mythology she was a goddess of epic poetry and eloquence, one of the nine Muses.
PRONOUNCED: kə-LIE-ə-pee (English) 
PRONOUNCED: Ka-li-o-pé (French)

## License

Copyright (c) 2016. All rights reserved.

Kalliope is covered by the MIT license, a permissive free software license that lets you do anything you want with the source code, 
as long as you provide back attribution and ["don't hold you liable"](http://choosealicense.com/). For the full license text see the [LICENSE.md](LICENSE.md) file.