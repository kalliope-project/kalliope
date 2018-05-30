Core neurons and signals are already packaged with the installation of kalliope an can be used out of the box. Community modules need to be installed manually.

>**Note:** To install a community module, you must declare your `resource_directory` in your [settings](../settings/settings.md).

>**Note:** After installing a community module, you need tu update your brain to use it

## Install a community module

Install via Kalliope CLI
```bash
kalliope install --git-url <git_url>
```

E.g:
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_wikipedia.git
```
You may be prompted to type your `sudo` password during the process.

You can also install a module manually.
Fist, clone the repo in the right resource folder.
```bash
cd /path/to/resource_folder
git clone <plugin_url>
```

Then install it manually via Ansible (Ansible has been installed with kalliope)
```bash
cd <cloned_repo>
ansible-playbook install.yml -K
```

Example
```bash
cd /home/me/my_kalliope_config/resources/neurons
git clone https://github.com/kalliope-project/kalliope_neuron_hue.git
cd hue
ansible-playbook install.yml -K
```

## Uninstall a community module

CLI syntax
```bash
kalliope uninstall --neuron-name <neuron_name>
kalliope uninstall --tts-name <tts_name>
kalliope uninstall --trigger-name <trigger_name>
kalliope uninstall --ignal-name <signal_name>
```

E.g:
```bash
kalliope uninstall --neuron-name hue
```

## List of community modules

- [Community neurons](https://kalliope-project.github.io/neurons_marketplace.html)
- [Community signals](https://kalliope-project.github.io/signals_marketplace.html)