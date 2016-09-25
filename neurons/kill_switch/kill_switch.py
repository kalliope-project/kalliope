from neurons import Neurone
import sys

class Kill_switch(Neurone):

    def __init__(self, *args , **kwargs):
        Neurone.__init__(self)

        sys.exit()
