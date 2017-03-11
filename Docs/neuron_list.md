# Neuron installation
A neuron is a module that will perform some actions attached to an order. You can use it in your synapses. See the [complete neuron documentation](neurons.md) for more information.

## Neuron list

Get the full neuron list available on [the project web site](https://kalliope-project.github.io/).

## Installation

Core neurons are already packaged with the installation of kalliope an can be used out of the box. Community neuron need to be installed manually.
>**Note:** To install a neuron, you must declare your `resource_directory` in your [settings](settings.md).

### Via the kalliope's CLI

CLI syntax
```bash
kalliope install --git-url <git_url>
```

E.g:
```bash
kalliope install --git-url https://github.com/kalliope-project/kalliope_neuron_wikipedia.git
```
You may be prompted to type your `sudo` password during the process.

### Manually

You can also install a neuron manually.
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

Full example
```bash
cd /home/me/my_kalliope_config/resources/neurons
git clone https://github.com/kalliope-project/kalliope_neuron_hue.git
cd hue
ansible-playbook install.yml -K
```

## Uninstall a resource
### Via the kalliope's CLI
>**Note:** To uninstall a resource, you must declare the `resource_directory` in your [settings](settings.md).

CLI syntax
```bash
kalliope uninstall --neuron-name <neuron_name>
kalliope uninstall --stt-name <stt_name>
kalliope uninstall --tts-name <tts_name>
kalliope uninstall --trigger-name <trigger_name>
```

E.g:
```bash
kalliope uninstall --neuron-name hue
```

### Manually

To remove a resource, you only need to delete the folder from the corresponding `resource_directory`.
```bash
cd /path/to/resource_folder
rm -rf <resource_name>
```

E.g
```bash
cd /home/me/my_kalliope_config/resources/neurons
rm -rf hue
```

>**Note:** When deleting a resource folder, libraries that have been installed by the resource are not removed from the system. If you want a complete cleanup, you'll have to open the install.yml file of the resource to see what have been installed and rollback manually each task.
For example, when installing the neuron hue, the python lib called phue has been installed. To perform a complete cleanup, you need then to run "sudo pip uninstall phue".


## Update a resource

To update a resource, you can either:
- uninstall the resource and then reinstall it back
- go into the resource directory and run a `git pull`
