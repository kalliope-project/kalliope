import unittest

from core.NeuronModule import MissingParameterException
from neurons.twitter.twitter import Twitter


class TestTwitter(unittest.TestCase):

    def setUp(self):
        self.consumer_key="kalliokey"
        self.consumer_secret = "kalliosecret"
        self.access_token_key = "kalliotokenkey"
        self.access_token_secret = "kalliotokensecret"
        self.tweet = "kalliotweet"

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(MissingParameterException):
                Twitter(**parameters_to_test)

        # empty
        parameters = dict()
        run_test(parameters)

        # missing tweet
        parameters = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
            "access_token_key": self.access_token_key,
            "access_token_secret": self.access_token_secret
        }
        run_test(parameters)

        # missing consumer_key
        parameters = {
            "consumer_secret": self.consumer_secret,
            "access_token_key": self.access_token_key,
            "access_token_secret": self.access_token_secret,
            "tweet": self.tweet
        }
        run_test(parameters)

        # missing consumer_secret
        parameters = {
            "consumer_key": self.consumer_key,
            "access_token_key": self.access_token_key,
            "access_token_secret": self.access_token_secret,
            "tweet": self.tweet
        }
        run_test(parameters)

        # missing access_token_key
        parameters = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
            "access_token_secret": self.access_token_secret,
            "tweet": self.tweet
        }
        run_test(parameters)

        # missing access_token_secret
        parameters = {
            "consumer_key": self.consumer_key,
            "consumer_secret": self.consumer_secret,
            "access_token_key": self.access_token_key,
            "tweet": self.tweet
        }
        run_test(parameters)
