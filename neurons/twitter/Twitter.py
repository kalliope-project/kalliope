import twitter

from core.NeuronModule import NeuronModule


class Twitter(NeuronModule):
    def __init__(self, **kwargs):

        super(Twitter, self).__init__(**kwargs)

        consumer_key = kwargs.get('consumer_key', None)
        consumer_secret = kwargs.get('consumer_secret', None)
        access_token_key = kwargs.get('access_token_key', None)
        access_token_secret = kwargs.get('access_token_secret', None)
        tweet = kwargs.get('tweet', None)

        if consumer_key is None:
            raise NotImplementedError("Twitter needs a consumer_key")
        if consumer_secret is None:
            raise NotImplementedError("Twitter needs a consumer_secret")
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
        message = {
            "tweet" : status
        }

        self.say(message)




