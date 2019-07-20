import json
import unittest

from Tests.test_api.base import RestAPITestBase
from kalliope._version import version_str


class TestMainView(RestAPITestBase):

    def test_server_is_up_and_running(self):
        # response = urllib2.urlopen(self.get_server_url())
        response = self.client.get(self.get_server_url())
        self.assertEqual(response.status_code, 200)

    def test_get_main_page(self):
        url = self.get_server_url() + "/"
        response = self.client.get(url)
        expected_content = {
            "Kalliope version": "%s" % version_str
        }
        self.assertEqual(json.dumps(expected_content, sort_keys=True),
                         json.dumps(json.loads(response.get_data().decode('utf-8')), sort_keys=True))


if __name__ == '__main__':
    unittest.main()
