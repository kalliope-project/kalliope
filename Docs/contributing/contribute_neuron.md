# Contributing: Create a neuron

Neurons are independent projects so they can be developed under a github project. Anyone can clone them, place them under the neurons repository and reuse them.

Creating a new Neuron must follow some rules:

## Repository Structure
1. The Neuron repository name is in __lowercase__.
1. Under the Neuron repository, the Neuron has a __README.md file__ describing the Neuron following this structure. You can get a [template here](neuron_template.md):
    - Neuron name:
    - Installation:     The CLI command used to install the neuron
    - Synopsis:         Description of the Neuron
    - Options:          A table of the incoming parameters managed by the Neuron.
    - Return Values:    A table of the returned values which can be catched by the *say_template attribute*.
    - Synapses example: An example of how to use the Neuron inside a Synapse.
    - Notes:            Something which needs to be add.
1. Under the Neuron repository, include a __Tests repository__ to manage the test of the Neuron.
1. Under the neuron repository, a [dna.yml file](dna.md) must be added that contains information about the neuron. type = "neuron"
1. Under the neuron repository, a [install.yml file](installation_file.md) must be added that contains the installation process.


## Code
1. Under the Neuron repository, the Neuron file name .py is also in __lowercase__.
1. The Neuron must be coded in __Python 2.7__.
1. Under the Neuron repository, include the __init__.py file which contains: *from neuron import Neuron* (/!\ respect the Case)
1. Inside the Neuron file, the Neuron Class name is in __uppercase__.
1. The Neuron __inherits from the NeuronModule__ coming from the Core.

    ```python
    from core.NeuronModule import NeuronModule
    class Say(NeuronModule):
    ```


1. The Neuron has a constructor __init__ which is the entry point.
The constructor has a __**kwargs argument__ which is corresponding to the Dict of incoming variables:values defined either in the brain file or in the signal.
1. The Neuron must refer to its __parent structure__ in the init by calling the super of NeuronModule.

    ```Python
    def __init__(self, **kwargs):
        super(Say, self).__init__(**kwargs)
    ```

1. You must run unit tests with success before sending a pull request. Add new tests that cover the code you want to publish.
    ```bash
    cd /path/to/kalliope
    python -m unittest discover
    ```

1. (*optionnal-> good practice*) The Neuron can implement a __private method _is_parameters_ok(self)__ which checks if entries are ok. *return: true if parameters are ok, raise an exception otherwise*
1. (*optionnal-> good practice*) The Neuron can __import and raise exceptions__ coming from NeuronModule:
    - MissingParameterException: *Some Neuron parameters are missing.*
    - InvalidParameterException: *Some Neuron parameters are invalid.*

1. The Neuron can use a __self.say(message) method__ to speak out some return values using the *say_template* attribute in the brain file.
the message variable must be a Dict of variable:values where variables can be defined as output.

1. The Neuron must (as much as possible) ensure the i18n. This means that they should __not manage a specific language__ inside its own logic.
Only [Synapse](brain.md) by the use of [Order](signals.md) must interact with the languages. This allow a Neuron to by reused by anyone, speaking any language.


## Code example

Example of neuron structure
```
myneuron/
├── __init__.py
├── myneuron.py
├── dna.yml
├── install.yml
├── README.md
└── tests
    ├── __init__.py
    └── test_myneuron.py
```

Example of neuron code
```python
class Myneuron(NeuronModule):
def __init__(self, **kwargs):
    super(Myneuron, self).__init__(**kwargs)
    # the args from the neuron configuration
    self.arg1 = kwargs.get('arg1', None)
    self.arg2 = kwargs.get('arg2', None)

    # check if parameters have been provided
    if self._is_parameters_ok():
        # -------------------
        # do amazing code
        # -------------------

def _is_parameters_ok(self):
    """
    Check if received parameters are ok to perform operations in the neuron
    :return: true if parameters are ok, raise an exception otherwise

    .. raises:: MissingParameterException
    """
    if self.arg1 is None:
        raise MissingParameterException("You must specify a arg1")
    if not isinstance(self.arg2, int):
        raise MissingParameterException("arg2 must be an integer")
    return True
```
