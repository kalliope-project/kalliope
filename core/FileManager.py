import logging
import os
import shutil


logging.basicConfig()
logger = logging.getLogger("kalliope")


class FileManager:
    def __init__(self):
        pass

    @staticmethod
    def create_directory(cache_path):
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

    @staticmethod
    def write_in_file(file_path, content):
        try:
            with open(file_path, "wb") as file_open:
                file_open.write(content)
                file_open.close()
            return not FileManager.file_is_empty(file_path)
        except IOError as e:
            logger.error("I/O error(%s): %s", e.errno, e.strerror)

    @staticmethod
    def wipe_cache(cache_path):
        shutil.rmtree(cache_path)

    @staticmethod
    def file_is_empty(file_path):
        return os.path.getsize(file_path) == 0

    @staticmethod
    def remove_file(file_path):
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
        """
        try:
            return os.path.exists(pathname) or FileManager.is_path_creatable(pathname)
        except OSError:
            return False
