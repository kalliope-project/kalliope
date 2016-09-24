class NeuroneNotFoundError(Exception):
    pass


def _run_plugin(plugin, parameters=None):
    """
    Dynamic loading of a module
    :param plugin: Module name to load
    :param parameters: Parameter of the module
    :return:
    """
    print "Run plugin %s with parameter %s" % (plugin, parameters)
    mod = __import__('neurons', fromlist=[plugin])
    try:
        klass = getattr(mod, plugin)
    except AttributeError:
        print "Error: No module named %s " % plugin
        raise NeuroneNotFoundError

    if klass is not None:
        # run the plugin
        if not parameters:
            klass()
        elif isinstance(parameters, dict):
            klass(**parameters)
        else:
            klass(parameters)


class NeuroneLauncher:

    def __init__(self):
        pass

    @classmethod
    def start_neurone(cls, neuron):
        """
        Neuron dict to start. {'neurone_name': {'args1': 'value1',  'args2': 'value2'}}
        :param neuron: Dict with neuron declaration
        :type neuron: Dict
        :return:
        """
        if isinstance(neuron, dict):
            for plugin, parameters in neuron.items():
                # capitalizes the first letter (because classes have first letter upper case)
                plugin = plugin.capitalize()
                _run_plugin(plugin, parameters)
        else:
            plugin = neuron
            # capitalizes the first letter (because classes have first letter upper case)
            plugin = plugin.capitalize()
            _run_plugin(plugin)

