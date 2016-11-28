import json
import unittest

from httpretty import httpretty

from kalliope.core.NeuronModule import InvalidParameterException
from kalliope.neurons.uri.uri import Uri


class TestUri(unittest.TestCase):

    def setUp(self):
        self.test_url = "http://kalliope.fr/voices/"

    def testGet(self):
        expected_content = '{"voice": "nico"}'
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, self.test_url, body=expected_content)

        parameters = {
            "url": self.test_url
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.text, expected_content)

    def testGetRaw(self):
        expected_content = 'raw line'
        httpretty.enable()
        httpretty.register_uri(httpretty.GET, self.test_url, body=expected_content)
        parameters = {
            "url": self.test_url
        }
        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.content, expected_content)

    def testPost(self):
        expected_content = '{"voice": "nico"}'
        httpretty.enable()
        httpretty.register_uri(httpretty.POST, self.test_url, body=expected_content)

        parameters = {
            "url": self.test_url,
            "method": "POST"
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.text, expected_content)

    def testPut(self):
        expected_content = '{"voice": "nico"}'
        httpretty.enable()
        httpretty.register_uri(httpretty.PUT, self.test_url, body=expected_content)

        parameters = {
            "url": self.test_url,
            "method": "PUT"
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.text, expected_content)

    def testDelete(self):
        expected_content = '{"voice": "nico"}'
        httpretty.enable()
        httpretty.register_uri(httpretty.DELETE, self.test_url, body=expected_content)

        parameters = {
            "url": self.test_url,
            "method": "DELETE"
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.text, expected_content)

    def testOptions(self):
        expected_content = '{"voice": "nico"}'
        httpretty.enable()
        httpretty.register_uri(httpretty.OPTIONS, self.test_url, body=expected_content)

        parameters = {
            "url": self.test_url,
            "method": "OPTIONS"
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.text, expected_content)

    def testHead(self):
        expected_content = '{"voice": "nico"}'
        httpretty.enable()
        httpretty.register_uri(httpretty.HEAD, self.test_url, body=expected_content)

        parameters = {
            "url": self.test_url,
            "method": "HEAD"
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.status_code, 200)

    def testPatch(self):
        expected_content = '{"voice": "nico"}'
        httpretty.enable()
        httpretty.register_uri(httpretty.PATCH, self.test_url, body=expected_content)

        parameters = {
            "url": self.test_url,
            "method": "PATCH"
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.text, expected_content)

    def testParameters(self):
        def run_test(parameters_to_test):
            with self.assertRaises(InvalidParameterException):
                Uri(**parameters_to_test)

        parameters = dict()
        run_test(parameters)

        parameters = {
            "url": self.test_url,
            "headers": 1
        }
        run_test(parameters)

        parameters = {
            "url": self.test_url,
            "timeout": "string"
        }
        run_test(parameters)

        parameters = {
            "url": self.test_url,
            "data": "this is a data",
            "data_from_file": "this is another data"
        }
        run_test(parameters)

        parameters = {
            "url": self.test_url,
            "method": "NONEXIST"
        }
        run_test(parameters)

    def testPostJsonFromFile(self):
        """
        Test that we are able to send json data through a file
        :return:
        """
        def request_callback(request, url, headers):
            data = json.loads(request.body)
            if "title" in data and "body" in data and "userId" in data:
                return 200, headers, "all key received from URL %s" % url

            return 400, headers, "server did not receive all keys from URL %s" % url

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, self.test_url, body=request_callback)

        parameters = {
            "url": self.test_url,
            "method": "POST",
            "data_from_file": "kalliope/neurons/uri/tests/data_post_test.json",
            "headers": {
                "Content-Type": 'application/json'
            }
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.status_code, 200)

    def testPostJson(self):
        """
        Test that we are able to send json data directly from the data variable
        :return:
        """
        def request_callback(request, url, headers):
            data = json.loads(request.body)
            if "title" in data and "body" in data and "userId" in data:
                return 200, headers, "all key received from URL %s" % url

            return 400, headers, "server did not receive all keys from URL %s" % url

        httpretty.enable()
        httpretty.register_uri(httpretty.POST, self.test_url, body=request_callback)

        parameters = {
            "url": self.test_url,
            "method": "POST",
            "data": "{\"id\": 1,\"title\": \"foo\", \"body\": \"bar\", \"userId\": 1}",
            "headers": {
                "Content-Type": 'application/json'
            }
        }

        uri_neuron = Uri(**parameters)
        self.assertEqual(uri_neuron.status_code, 200)

if __name__ == '__main__':
    unittest.main()
