import unittest

from kalliope.core.NeuronModule import InvalidParameterException
from kalliope.neurons.wikipedia_searcher import Wikipedia_searcher


class TestWikipediaSearcher(unittest.TestCase):
    def setUp(self):
        pass

    def test_parameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(InvalidParameterException):
                Wikipedia_searcher(**parameters_to_test)

        parameters = dict()
        run_test(parameters)

        # sentences must be an integer
        parameters = {
            "language": "en",
            "query": "this is the query",
            "sentences": "invalid"

        }
        run_test(parameters)

        # test non existing language
        parameters = {
            "language": "foo",
            "query": "this is the query",
            "sentences": 1

        }
        run_test(parameters)

    # def test_get_DisambiguationError(self):
    #
    #     parameters = {
    #         "language": "fr",
    #         "query": "bot",
    #         "sentences": 1
    #     }
    #
    #     wiki = Wikipedia_searcher(**parameters)
    #     self.assertEqual(wiki.returncode, "DisambiguationError")
    #
    # def test_page_error(self):
    #     parameters = {
    #         "language": "fr",
    #         "query": "fudu foo bar non exist",
    #         "sentences": 1
    #     }
    #
    #     wiki = Wikipedia_searcher(**parameters)
    #     self.assertEqual(wiki.returncode, "PageError")
    #
    # def test_summary_found(self):
    #     parameters = {
    #         "language": "fr",
    #         "query": "kalliope"
    #     }
    #     wiki = Wikipedia_searcher(**parameters)
    #     self.assertEqual(wiki.returncode, "SummaryFound")

if __name__ == '__main__':
    unittest.main()
