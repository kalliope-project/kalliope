class Synapse(object):
    def __init__(self, name, neurons, signals):
        self.name = name
        self.neurons = neurons
        self.signals = signals

    def serialize(self):
        return {
            'name': self.name,
            'neurons': [e.serialize() for e in self.neurons],
            'signals': [e.serialize() for e in self.signals]
        }
