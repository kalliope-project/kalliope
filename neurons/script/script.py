from core import Neurone
import subprocess
import os


class ScriptNotFound(Exception):
    pass


class ScriptNotExecutable(Exception):
    pass


class Script(Neurone):
    def __init__(self, *args , **kwargs):
        Neurone.__init__(self)

        # get message to spell out loud
        script_path = kwargs.get('path', "")

        # test that the file exist and is executable
        if self.is_exe(script_path):
            p = subprocess.Popen(script_path, stdout=subprocess.PIPE, shell=True)
            (output, err) = p.communicate()


    def is_exe(self, fpath):
        returned_value = True
        if not os.path.isfile(fpath):
            raise ScriptNotFound()
        if not os.access(fpath, os.X_OK):
            raise ScriptNotExecutable()

        return returned_value