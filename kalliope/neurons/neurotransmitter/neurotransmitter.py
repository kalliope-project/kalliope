import logging

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException, InvalidParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Neurotransmitter(NeuronModule):
    def __init__(self, **kwargs):
        super(Neurotransmitter, self).__init__(**kwargs)

        # get parameters
        self.from_answer_link = kwargs.get('from_answer_link', None)
        self.default = kwargs.get('default', None)
        self.direct_link = kwargs.get('direct_link', None)

        # do some check
        if self._is_parameters_ok():
            if self.direct_link is not None:
                logger.debug("Neurotransmitter directly call to the synapse name: %s" % self.direct_link)
                self.run_synapse_by_name(self.direct_link)
            else:
                # the user is using a from_answer_link, we call the stt to get an audio
                self.get_audio_from_stt(callback=self.callback)

    def callback(self, audio):
        """
        The callback used by the STT module to get the linked synapse

        :param audio: the audio to play by STT
        """
        logger.debug("Neurotransmitter, receiver audio from STT: %s" % audio)
        # print self.links
        # set a bool to know if we have found a valid answer
        if audio is None:
            self.run_synapse_by_name(self.default)
        else:
            found = False
            for el in self.from_answer_link:
                for answer in el["answers"]:
                    if self.is_order_matching(audio, answer):
                        found = self.run_synapse_by_name_with_order(order=audio,
                                                                    synapse_name=el["synapse"],
                                                                    order_template=answer)
            if not found: # the answer do not correspond to any answer. We run the default synapse
                self.run_synapse_by_name(self.default)

    def _is_parameters_ok(self):
        """
        Check if received links are ok to perform operations
        :return: true if the neuron is well configured, raise an exception otherwise

        .. raises:: MissingParameterException, InvalidParameterException
        """
        # with the neuron the user has the choice of a direct link that call another synapse,
        #  or a link with an answer caught from the STT engine

        # we cannot use at the same time a direct redirection and a link with question
        if self.direct_link is not None and self.from_answer_link is not None:
            raise InvalidParameterException("neurotransmitter cannot be used with both direct_link and from_answer_link")

        if self.direct_link is None and self.from_answer_link is None:
            raise MissingParameterException("neurotransmitter must be used with direct_link or from_answer_link")

        if self.from_answer_link is not None:
            if self.default is None:
                raise InvalidParameterException("default parameter is required and must contain a valid synapse name")
            for el in self.from_answer_link:
                if "synapse" not in el:
                    raise MissingParameterException("Links must contain a synapse name: %s" % el)
                if "answers" not in el:
                    raise MissingParameterException("Links must contain answers: %s" % el)

        return True
