import unittest
import os

from kalliope.core.Utils.FileManager import FileManager


class TestFileManager(unittest.TestCase):
    """
    Class to test FileManager
    """

    def setUp(self):
        pass

    def test_create_directory(self):
        """
        Test to create a new directory.
        """
        # set up
        cache_path = "/tmp/kalliope/tests/testDirectory"
        if os.path.exists(cache_path):
            os.removedirs(cache_path)

        # Test FileManager.create_directory
        FileManager.create_directory(cache_path)
        self.assertTrue(os.path.exists(cache_path),
                        "Fail creating a directory to the path ")

        # Remove the directory
        os.removedirs(cache_path)

    def test_write_in_file(self):
        """
        Test to write in file.
        """

        # set up the context
        dir_path = "/tmp/kalliope/tests/"
        file_name = "test_FileManager_writeInFile"
        file_path = os.path.join(dir_path,file_name)
        in_file_text = "[Kalliope] Testing the write_in_file method from Utils.FileManager"
        if os.path.exists(file_path):
            os.remove(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Test FileManager.write_in_file
        FileManager.write_in_file(file_path=file_path, content=in_file_text)
        with open(file_path, 'r') as content_file:
            content = content_file.read()
            self.assertEqual(content, in_file_text,
                             "Fail writing in the file ")

        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_file_is_empty(self):
        """
        Test that the file is empty
        """

        # set up the context
        dir_path = "/tmp/kalliope/tests/"
        file_name = "test_FileManager_fileIsEmpty"
        file_path = os.path.join(dir_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Test FileManager.file_is_empty
        with open(file_path, "wb") as file_open:
            file_open.write("")
            file_open.close()
        self.assertTrue(FileManager.file_is_empty(file_path=file_path),
                        "Fail matching to verify that file is empty ")

        # Clean up
        if os.path.exists(file_path):
            os.remove(file_path)

    def test_remove_file(self):
        """
        Test to remove a file
        """

        # set up the context
        dir_path = "/tmp/kalliope/tests/"
        file_name = "test_FileManager_fileRemove"
        file_path = os.path.join(dir_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Test to remove the file
        # FileManager.remove_file
        with open(file_path, "wb") as file_open:
            file_open.write("")
            file_open.close()
        FileManager.remove_file(file_path=file_path)
        self.assertFalse(os.path.exists(file_path),
                         "Fail removing the file")

    def test_is_path_creatable(self):
        """
        Test if the path is creatable for the user
        Does the user has the permission to use this path ?
        """

        # set up the context
        dir_path = "/tmp/kalliope/tests/"
        file_name = "test_FileManager_filePathCreatable"
        file_path = os.path.join(dir_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # test not allowed : return False
        not_allowed_root_path = "/root/"
        not_allowed_path = os.path.join(not_allowed_root_path, file_name)
        self.assertFalse(FileManager.is_path_creatable(not_allowed_path),
                         "Fail to assert not accessing this path ")
        # test allowed : return True
        self.assertTrue(FileManager.is_path_creatable(file_path))

    def test_is_path_exists_or_creatable(self):
        """
        Test the _is_path_exists_or_creatable
        4 scenarii :
            - the file exists and is creatable : return True
            - the file does not exist but is creatable : return True
            - the file exists but is not allowed : return True --> need a review !
            - the file does not exist and is not allowed : return False
        """

        # set up the context
        dir_path = "/tmp/kalliope/tests/"
        file_name = "test_FileManager_fileIsPathExistsOrCreatable"
        file_path = os.path.join(dir_path, file_name)
        if os.path.exists(file_path):
            os.remove(file_path)
        if not os.path.exists(dir_path):
            os.makedirs(dir_path)

        # Test the file exist and creatable : return True
        with open(file_path, "wb") as file_open:
            file_open.write("[Kalliope] Test Running the test_is_path_exists_or_creatable method")
            file_open.close()
        self.assertTrue(FileManager.is_path_exists_or_creatable(file_path),
                        "Fail to assert the file exist ")

        # test the file not exist but creatable : return True
        os.remove(file_path)
        self.assertTrue(FileManager.is_path_exists_or_creatable(file_path),
                         "Fail asserting the file does not exist ")

        # test the file exist but not creatable : return True
        # file_exist_not_allowed = "/root/.ssh/known_hosts"
        # self.assertTrue(FileManager.is_path_creatable(file_exist_not_allowed))

        # test the file not exist and not allowed : return False
        not_allowed_root_path = "/root/"
        not_allowed_path = os.path.join(not_allowed_root_path, file_name)
        self.assertFalse(FileManager.is_path_creatable(not_allowed_path),
                         "Fail to assert not accessing this path ")

if __name__ == '__main__':
    unittest.main()