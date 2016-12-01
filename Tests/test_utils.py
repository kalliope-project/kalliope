import unittest
import os

from kalliope.core.Utils.Utils import Utils


class TestUtils(unittest.TestCase):
    """
    Class to test Utils methods
    """

    def setUp(self):
        pass

    def test_get_current_file_parent_path(self):
        """
        Expect to get back the parent path file
        """
        path_to_test = "../kalliope/core/Utils"
        expected_result = os.path.normpath("../kalliope/core")

        self.assertEquals(Utils.get_current_file_parent_path(path_to_test),
                          expected_result,
                          "fail getting the parent parent path from the given path")

    def test_get_current_file_parent_parent_path(self):
        """
        Expect to get back the parent parent path file
        """
        path_to_test = "../kalliope/core/Utils"
        expected_result = os.path.normpath("../kalliope")

        self.assertEquals(Utils.get_current_file_parent_parent_path(path_to_test),
                          expected_result,
                          "fail getting the parent parent path from the given path")

