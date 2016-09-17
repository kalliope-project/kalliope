import yaml
import os


def get_settings():
    """
    Load settings.yml file
    :return:
    """
    filename = "settings.yml"
    return _load_yaml_file(filename)


def get_brain():
    """
    Load brain.yml file
    :return:
    """
    filename = "../brain.yml"
    return _load_yaml_file(filename)


def _load_yaml_file(file_to_load):
    """
    Load settings file
    :return:
    """
    # Load settings. Will be used to convert slot number into GPIO pin number
    __location__ = os.path.realpath(
        os.path.join(os.getcwd(), os.path.dirname(__file__)))
    with open(os.path.join(__location__, file_to_load)) as ymlfile:
        cfg = yaml.load(ymlfile)
    return cfg


def my_import(name):
    components = name.split('.')
    mod = __import__(components[0])
    for comp in components[1:]:
        mod = getattr(mod, comp)
    return mod