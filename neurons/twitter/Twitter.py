import twitter

from core.NeuronModule import NeuronModule


class Twitter(NeuronModule):
    def __init__(self, **kwargs):

        consumer_key = ''
        consumer_secret = ''

        access_token_key = kwargs.get('access_token_key', None)
        access_token_secret = kwargs.get('access_token_secret', None)
        tweet = kwargs.get('tweet', None)

        if access_token_key is None:
            raise NotImplementedError("Twitter needs an access_token_key")
        if access_token_secret is None:
            raise NotImplementedError("Twitter needs and access_token_secret")
        if tweet is None:
            raise NotImplementedError("You need to provide something to tweet !")

        api = twitter.Api(consumer_key=consumer_key,
                          consumer_secret=consumer_secret,
                          access_token_key=access_token_key,
                          access_token_secret=access_token_secret)

        status = api.PostUpdate(tweet)


