import sys

from core.Models.Neurone import Neurone


class Kill_switch(Neurone):

    def __init__(self, *args , **kwargs):
        Neurone.__init__(self)

        sys.exit()
