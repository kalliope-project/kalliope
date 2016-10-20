import logging

from core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Neurotransmitter(NeuronModule):
    def __init__(self, **kwargs):
        super(Neurotransmitter, self).__init__(**kwargs)

        # get links
        self.links = kwargs.get('links', None)
        # do some check
        if self._links_content_ok():
            # the brain seems fine, we call the stt to get an audio
            self.get_audio_from_stt(callback=self.callback)

    def callback(self, audio):
        logger.debug("Neurotransmitter, receiver audio from STT: %s" % audio)
        print self.links
        for el in self.links:
            if audio in el["answers"]:
                print "found"
                self.run_synapse_ny_name(el["synapse"])
                # we don't need to check to rest of answer
                break

    def _links_content_ok(self):
        """
        Check the content of the links parameter
        :return:
        """
        if self.links is None:
            raise MissingParameterException("links parameter required and must contain at least one link")
        for el in self.links:
            if "synapse" not in el:
                raise MissingParameterException("Links must contain a synapse name: %s" % el)
            if "answers" not in el:
                raise MissingParameterException("Links must contain answers: %s" % el)

        return True
