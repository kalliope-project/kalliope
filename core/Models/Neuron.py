

class Neuron(object):
    def __init__(self, name=None, parameters=None):
        self.name = name
        self.parameters = parameters

    def serialize(self):
        return {
            'name': self.name,
            'parameters': str(self.parameters)
        }
