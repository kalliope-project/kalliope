from core import Neurone
import subprocess


class Script(Neurone):
    def __init__(self, script_path):
        Neurone.__init__(self)
        p = subprocess.Popen(script_path, stdout=subprocess.PIPE, shell=True)
        (output, err) = p.communicate()
