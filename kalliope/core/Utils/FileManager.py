import logging
import os


logging.basicConfig()
logger = logging.getLogger("kalliope")


class FileManager:
    """
    Class used to manage Files
    """
    def __init__(self):
        pass

    @staticmethod
    def create_directory(cache_path):
        """
        Create a directory at the provided `cache_path`
        :param cache_path: the path of the directory to create
        :type cache_path: str
        """
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

    @staticmethod
    def write_in_file(file_path, content):
        """
        Write contents into a file
        :param file_path: the path of the file to write on
        :type file_path: str
        :param content: the contents to write in the file
        :type content: str

        .. raises:: IOError
        """
        try:
            with open(file_path, "wb") as file_open:
                file_open.write(content)
                file_open.close()
            return not FileManager.file_is_empty(file_path)
        except IOError as e:
            logger.error("I/O error(%s): %s", e.errno, e.strerror)

    @staticmethod
    def file_is_empty(file_path):
        """
        Check if the file is empty
        :param file_path: the path of the file
        :return: True if the file is empty, False otherwise
        """
        return os.path.getsize(file_path) == 0

    @staticmethod
    def remove_file(file_path):
        """
        Remove the file locate at the provided `file_path`
        :param file_path:
        :return: True if the file has been removed successfully, False otherwise
        """
        if os.path.exists(file_path):
            return os.remove(file_path)

    @staticmethod
    def is_path_creatable(pathname):
        """
        `True` if the current user has sufficient permissions to create the passed
        pathname; `False` otherwise.
        """
        dirname = os.path.dirname(pathname) or os.getcwd()
        return os.access(dirname, os.W_OK)

    @staticmethod
    def is_path_exists_or_creatable(pathname):
        """
        `True` if the passed pathname is a valid pathname for the current OS _and_
        either currently exists or is hypothetically creatable; `False` otherwise.

        This function is guaranteed to _never_ raise exceptions.

        .. raises:: OSError
        """
        try:
            return os.path.exists(pathname) or FileManager.is_path_creatable(pathname)
        except OSError:
            return False
