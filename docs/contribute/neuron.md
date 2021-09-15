# Contributing: Create a neuron

Neurons are independent projects so they can be developed under a github project. Anyone can clone them, place them under the neurons repository and reuse them.

Creating a new Neuron must follow some rules:

## Repository Structure

1. The Neuron repository name is in **lowercase**.
2. Under the Neuron repository, the Neuron has a **README.md file** describing the Neuron following this structure:
   - Neuron name:
   - Installation: The CLI command used to install the neuron
   - Synopsis: Description of the Neuron
   - Options: A table of the incoming parameters managed by the Neuron.
   - Return Values: A table of the returned values which can be catched by the _say_template attribute_.
   - Synapses example: An example of how to use the Neuron inside a Synapse.
   - Notes: Something which needs to be added.
3. Under the Neuron repository, include a **Tests repository** to manage the test of the Neuron.
4. Under the neuron repository, a [dna.yml file](dna.md) must be added that contains information about the neuron. type = "neuron"
5. Under the neuron repository, a [install.yml file](installation_file.md) must be added that contains the installation process.

## Code

1. Under the Neuron repository, the Neuron file name .py is also in **lowercase**.
2. The Neuron must be coded in **Python 2.7**.
3. Under the Neuron repository, include the **init**.py file which contains: _from neuron import Neuron_ (/!\ respect the Case)
4. Inside the Neuron file, the Neuron Class name is in **uppercase**.
5. The Neuron **inherits from the NeuronModule** coming from the Core.

   ```python
   from core.NeuronModule import NeuronModule
   class Say(NeuronModule):
   ```

6. The Neuron has a constructor **init** which is the entry point.
   The constructor has a **\*\*kwargs argument** which is corresponding to the Dict of incoming variables: values defined either in the brain file or in the signal.
7. The Neuron must refer to its **parent structure** in the init by calling the super of NeuronModule.

   ```Python
    def __init__(self, **kwargs):
       super(Say, self).__init__(**kwargs)
   ```

8. You must run unit tests with success before sending a pull request. Add new tests that cover the code you want to publish.

   ```bash
   cd /path/to/kalliope
   python -m unittest discover
   ```

9. (_optionnal-> good practice_) The Neuron can implement a **private method \_is_parameters_ok(self)** which checks if entries are ok. _return: true if parameters are ok, raise an exception otherwise_
10. (_optionnal-> good practice_) The Neuron can **import and raise exceptions** coming from NeuronModule:

    - MissingParameterException: _Some Neuron parameters are missing._
    - InvalidParameterException: _Some Neuron parameters are invalid._

11. The Neuron can use a **self.say(message) method** to speak out some return values using the _say_template_ attribute in the brain file.
    the message variable must be a Dict of variable: values where variables can be defined as output.

12. The Neuron must (as much as possible) ensure the i18n. This means that they should **not manage a specific language** inside its own logic.
    Only synapse by the use of order must interact with the languages. This allow a Neuron to be reused by anyone, speaking any language.

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

## Share it

We are maintaining a list of all the Neurons available from the community, let us know you've developed your own by opening [an issue](https://github.com/kalliope-project/kalliope/issues) with the link of your neuron or send a pull request to update the [neuron list](https://kalliope-project.github.io/neurons_marketplace.html) on the Kalliope's website directly.
