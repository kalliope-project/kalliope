class Order(object):
    def __init__(self, sentence):
        self.sentence = sentence

    def __str__(self):
        return "%s: Sentence: %s" % (self.__class__.__name__, self.sentence)
