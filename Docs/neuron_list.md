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

| Name                                                                           | Description                                                                             |
|--------------------------------------------------------------------------------|-----------------------------------------------------------------------------------------|
| [gmail_checker](https://github.com/kalliope-project/kalliope_neuron_gmail)     | Get the number of unread email and their subjects from a gmail account                  |
| [pushetta](https://github.com/kalliope-project/kalliope_neuron_pushetta)       | Send a push message to a remote device like Android/iOS/Windows Phone or Chrome browser |
| [rss_reader](https://github.com/kalliope-project/kalliope_neuron_rss_reader)   | get rss feed from website                                                               |
| [tasker](https://github.com/kalliope-project/kalliope_neuron_tasker)           | Send a message to Android tasker app                                                    |
| [twitter](https://github.com/kalliope-project/kalliope_neuron_twitter)         | Send a Twit from kalliope                                                               |
| [wake_on_lan](https://github.com/kalliope-project/kalliope_neuron_wake_on_lan) | Wake on lan a computer                                                                  |
| [wikipedia](https://github.com/kalliope-project/kalliope_neuron_wikipedia)     | Search for a page on Wikipedia                                                          |

Wanna add your neuron in the list? Open [an issue](../../issues) with the link of your neuron or send a pull request to update the list directly.

To know how to install a community neuron, read the "Installation" section of the [neuron documentation](neurons.md).
