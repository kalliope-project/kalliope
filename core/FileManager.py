import os
import shutil


class FileManager:
    def __init__(self):
        pass

    @staticmethod
    def create_directory(cache_path):
        if not os.path.exists(cache_path):
            os.makedirs(cache_path)

    @staticmethod
    def write_in_file(file_path, content):
        with open(file_path, "wb") as file_open:
            file_open.write(content)
            file_open.close()
        return not FileManager.file_is_empty(file_path)

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
