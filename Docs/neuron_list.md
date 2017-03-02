# List of available neuron

A neuron is a module that will perform some actions attached to an order. You can use it in your synapses. See the [complete neuron documentation](neurons.md) for more information.

## Core neuron

| Name                                                      | Description                                       |
|-----------------------------------------------------------|---------------------------------------------------|
| [ansible_playbook](../kalliope/neurons/ansible_playbook/) | Run an ansible playbook                           |
| [kill_switch](../kalliope/neurons/kill_switch/)           | Stop Kalliope process                             |
| [neurotransmitter](../kalliope/neurons/neurotransmitter/) | Link synapse together                             |
| [say](../kalliope/neurons/say/)                           | Make Kalliope talk by using TTS                   |
| [script](../kalliope/neurons/script/)                     | Run an executable script                          |
| [shell](../kalliope/neurons/shell/)                       | Run a shell command                               |
| [sleep](../kalliope/neurons/sleep/)                       | Make Kalliope sleep for a while before continuing |
| [systemdate](../kalliope/neurons/systemdate/)             | Give the local system date and time               |
| [uri](../kalliope/neurons/uri/)                           | Interacts with HTTP and HTTPS web services.       |

## Community neuron

| Name                                                                                 | Description                                                                             |
|--------------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [facebook](https://github.com/kalliope-project/kalliope_neuron_facebook)             | Post and Read message on Facebook                                                        |
| [gmail_checker](https://github.com/kalliope-project/kalliope_neuron_gmail)           | Get the number of unread email and their subjects from a gmail account             |
| [google agenda](https://github.com/bacardi55/kalliope-google-calendar)               | Get your next meetings on google calendar                                               |
| [google maps](https://github.com/bacardi55/kalliope-gmaps)                           | Get address / distance / time / directions from Google maps |
| [hue](https://github.com/kalliope-project/kalliope_neuron_hue)                       | Control the Philips Hue lighting system  |
| [list available orders](https://github.com/bacardi55/kalliope-list-available-orders) | Let kalliope tell you what she how she can help                                         |
| [MPD](https://github.com/bacardi55/kalliope-mpd)                                     | Play music via an MPD server                                                            |
| [openweathermap](https://github.com/kalliope-project/kalliope_neuron_openweathermap) | Get the weather of a location                                                           |
| [pi camera](https://github.com/bacardi55/kalliope-picamera)                          | Take picture with your picamera                                                         |
| [pushetta](https://github.com/kalliope-project/kalliope_neuron_pushetta)             | Send a push message to a remote device like Android/iOS/Windows Phone or Chrome browser |
| [repeat](https://github.com/bacardi55/kalliope-repeat)                               | Make kalliope say whatever you want                                                     |
| [rss_reader](https://github.com/kalliope-project/kalliope_neuron_rss_reader)         | Get rss feed from website                                                               |
| [slack](https://github.com/kalliope-project/kalliope_neuron_slack)                   | Post and Read message on Slack                                                          |
| [system_status](https://github.com/bacardi55/kalliope-system-status)                 | Get info about the system (cpu, memory, …                                                               |
| [tasker](https://github.com/kalliope-project/kalliope_neuron_tasker)                 | Send a message to Android tasker app                                                    |
| [todotxt](https://github.com/bacardi55/kalliope-todotxt)                             | Manage a todolist via Kalliope                                                    |
| [twitter](https://github.com/kalliope-project/kalliope_neuron_twitter)               | Send a Twit from kalliope                                                               |
| [wake_on_lan](https://github.com/kalliope-project/kalliope_neuron_wake_on_lan)       | Wake on lan a computer                                                                  |
| [web scraper](https://github.com/bacardi55/kalliope-web-scraper)                     | Read web pages that don't provide RSS feed or APIs (by scraping html)                   |                            |
| [wikipedia](https://github.com/kalliope-project/kalliope_neuron_wikipedia)           | Search for a page on Wikipedia                                                          |


Wanna add your neuron in the list? Open [an issue](../../issues) with the link of your neuron or send a pull request to update the list directly.

To know how to install a community neuron, read the "Installation" section of the [neuron documentation](neurons.md).

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
