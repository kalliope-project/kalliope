import logging

logging.basicConfig()
logger = logging.getLogger("kalliope")


class ModuleNotFoundError(Exception):
    """
    The module can not been found

    .. notes: Check the case: must be in lower case.
    """
    pass


class Utils(object):

    color_list = dict(
        PURPLE='\033[95m',
        BLUE='\033[94m',
        GREEN='\033[92m',
        YELLOW='\033[93m',
        RED='\033[91m',
        ENDLINE='\033[0m',
        BOLD='\033[1m',
        UNDERLINE='\033[4m'
    )

    @classmethod
    def print_info(cls, text_to_print):
        print(cls.color_list["BLUE"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_success(cls, text_to_print):
        print(cls.color_list["GREEN"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_warning(cls, text_to_print):
        print(cls.color_list["YELLOW"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_danger(cls, text_to_print):
        print(cls.color_list["RED"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_header(cls, text_to_print):
        print(cls.color_list["HEADER"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_header(cls, text_to_print):
        print(cls.color_list["PURPLE"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_bold(cls, text_to_print):
        print(cls.color_list["BOLD"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_underline(cls, text_to_print):
        print(cls.color_list["UNDERLINE"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def get_dynamic_class_instantiation(cls, package_name, module_name, parameters=None):
        """
        Load a python class dynamically

        from my_package.my_module import my_class
        mod = __import__('my_package.my_module', fromlist=['my_class'])
        klass = getattr(mod, 'my_class')

        :param package_name: name of the package where we will find the module to load (neurons, tts, stt, trigger)
        :param module_name: name of the module from the package_name to load. This one is capitalized. Eg: Snowboy
        :param parameters:  dict parameters to send as argument to the module
        :return:
        """
        logger.debug("Run plugin %s with parameter %s" % (module_name, parameters))
        module_name_with_path = package_name + "." + module_name.lower() + "." + module_name.lower()
        mod = __import__(module_name_with_path, fromlist=[module_name])
        try:
            klass = getattr(mod, module_name)
        except AttributeError:
            logger.debug("Error: No module named %s " % module_name)
            raise ModuleNotFoundError("The module %s does not exist in package %s" % (module_name, package_name))

        if klass is not None:
            # run the plugin
            if not parameters:
                return klass()
            elif isinstance(parameters, dict):
                return klass(**parameters)
            else:
                return klass(parameters)
        return None

    @classmethod
    def print_yaml_nicely(cls, to_print):
        """
        Used for debug
        :param to_print: Dict to print nicely
        :return:
        """
        import json
        print(json.dumps(to_print, indent=2))
