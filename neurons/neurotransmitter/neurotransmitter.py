import logging

from core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Neurotransmitter(NeuronModule):
    def __init__(self, **kwargs):
        super(Neurotransmitter, self).__init__(**kwargs)

        # get links
        self.links = kwargs.get('links', None)
        self.default = kwargs.get('default', None)
        # do some check
        if self._links_content_ok():
            # the brain seems fine, we call the stt to get an audio
            self.get_audio_from_stt(callback=self.callback)

    def callback(self, audio):
        logger.debug("Neurotransmitter, receiver audio from STT: %s" % audio)
        # print self.links
        # set a bool to know if we have found a valid answer
        found = False
        for el in self.links:
            if audio in el["answers"]:
                found = True
                self.run_synapse_ny_name(el["synapse"])
                # we don't need to check to rest of answer
                break
        if not found:
            # the answer do not correspond to any answer. We run the default synapse
            self.run_synapse_ny_name(self.default)

    def _links_content_ok(self):
        """
        Check the content of the links parameter
        :return:
        """
        if self.links is None:
            raise MissingParameterException("links parameter required and must contain at least one link")
        if self.default is None:
            raise MissingParameterException("default parameter is required and must contain a valid synapse name")
        for el in self.links:
            if "synapse" not in el:
                raise MissingParameterException("Links must contain a synapse name: %s" % el)
            if "answers" not in el:
                raise MissingParameterException("Links must contain answers: %s" % el)

        return True
