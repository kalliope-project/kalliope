import os
import unittest
from unittest import mock


def get_test_path(file_path):
    """
    return the path of a file with "Tests" depending of the current location of the execution
    :return: string path
    """
    current_path = os.getcwd()
    if "/Tests" in current_path:
        return current_path + os.sep + file_path
    else:
        return current_path + os.sep + "Tests" + os.sep + file_path


class TestTestUtils(unittest.TestCase):

    def test_get_test_path(self):
        # Tests is in path
        with mock.patch('Tests.utils.utils.os.getcwd', return_value='/home/user/Documents/kalliope/Tests'):
            expected = "/home/user/Documents/kalliope/Tests/file"
            self.assertEqual(expected, get_test_path("file"))

        # Tests not in path
        with mock.patch('Tests.utils.utils.os.getcwd', return_value='/home/user/Documents/kalliope'):
            expected = "/home/user/Documents/kalliope/Tests/file"
            self.assertEqual(expected, get_test_path("file"))
