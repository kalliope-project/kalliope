import logging

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException
import wikipedia

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Wikipedia(NeuronModule):
    def __init__(self, **kwargs):
        # we don't need the TTS cache for this neuron
        cache = kwargs.get('cache', None)
        if cache is None:
            cache = False
            kwargs["cache"] = cache
        super(Wikipedia, self).__init__(**kwargs)

        # get parameters form the neuron
        self.query = kwargs.get('query', None)
        self.language = kwargs.get('language', None)
        self.sentences = kwargs.get('sentences', None)

        self.may_refer = None
        self.returncode = None

        # check parameters
        if self._is_parameters_ok():
            # set the language
            wikipedia.set_lang(self.language)
            # do the summary search
            try:
                summary = wikipedia.summary(self.query, auto_suggest=True, sentences=self.sentences)
                # if we are here, no exception raised, we got a summary
                self.returncode = "SummaryFound"
            except wikipedia.exceptions.DisambiguationError as e:
                # Exception raised when a page resolves to a Disambiguation page.
                # The options property contains a list of titles of Wikipedia pages that the query may refer to.
                self.may_refer = e.options
                # Removing duplicates in lists.
                self.may_refer = list(set(self.may_refer))
                self.returncode = "DisambiguationError"
                summary = ""
            except wikipedia.exceptions.PageError:
                # Exception raised when no Wikipedia matched a query.
                self.returncode = "PageError"
                summary = ""

            message = {
                "summary": summary,
                "may_refer": self.may_refer,
                "returncode": self.returncode
            }
            logger.debug("Wikipedia returned message: %s" % str(message))

            self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: InvalidParameterException
        """

        if self.query is None:
            raise InvalidParameterException("Wikipedia needs a query")
        if self.language is None:
            raise InvalidParameterException("Wikipedia needs a language")

        valid_language = wikipedia.languages().keys()
        if self.language not in valid_language:
            raise InvalidParameterException("Wikipedia needs a valid language: %s" % valid_language)

        return True
