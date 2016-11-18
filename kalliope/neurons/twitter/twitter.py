import twitter

from kalliope.core.NeuronModule import NeuronModule, InvalidParameterException


class Twitter(NeuronModule):
    def __init__(self, **kwargs):

        super(Twitter, self).__init__(**kwargs)

        self.consumer_key = kwargs.get('consumer_key', None)
        self.consumer_secret = kwargs.get('consumer_secret', None)
        self.access_token_key = kwargs.get('access_token_key', None)
        self.access_token_secret = kwargs.get('access_token_secret', None)
        self.tweet = kwargs.get('tweet', None)

        # check parameters
        if self._is_parameters_ok():
            api = twitter.Api(consumer_key=self.consumer_key,
                              consumer_secret=self.consumer_secret,
                              access_token_key=self.access_token_key,
                              access_token_secret=self.access_token_secret)

            status = api.PostUpdate(self.tweet)
            message = {
                "tweet" : status.text
            }

            self.say(message)

    def _is_parameters_ok(self):
        """
        Check if received parameters are ok to perform operations in the neuron
        :return: true if parameters are ok, raise an exception otherwise

        .. raises:: InvalidParameterException
        """
        if self.consumer_key is None:
            raise InvalidParameterException("Twitter needs a consumer_key")
        if self.consumer_secret is None:
            raise InvalidParameterException("Twitter needs a consumer_secret")
        if self.access_token_key is None:
            raise InvalidParameterException("Twitter needs an access_token_key")
        if self.access_token_secret is None:
            raise InvalidParameterException("Twitter needs and access_token_secret")
        if self.tweet is None:
            raise InvalidParameterException("You need to provide something to tweet !")

        return True




