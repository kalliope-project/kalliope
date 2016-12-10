# -*- coding: utf-8 -*-
import logging
import feedparser

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Rss_reader(NeuronModule):
    def __init__(self, **kwargs):
        super(Rss_reader, self).__init__(**kwargs)

        self.feedUrl = kwargs.get('feed_url', None)
        self.limit = kwargs.get('max_items', 30)

        # check if parameters have been provided
        if self._is_parameters_ok():

            # prepare a returned dict
            returned_dict = dict()

            logging.debug("Reading feed from: %s" % self.feedUrl)

            feed = feedparser.parse( self.feedUrl )

            logging.debug("Read title from feed: %s" % feed["channel"]["title"])

            returned_dict["feed"] = feed["channel"]["title"]
            returned_dict["items"] = feed["items"][:self.limit]
            
            self.say(returned_dict)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: MissingParameterException
        """
        if self.feedUrl is None:
            raise MissingParameterException("feed url parameter required")

        return True
