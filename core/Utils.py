import logging

logging.basicConfig()
logger = logging.getLogger("jarvis")


class ModuleNotFoundError(Exception):
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
        print cls.color_list["BLUE"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def print_success(cls, text_to_print):
        print cls.color_list["GREEN"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def print_warning(cls, text_to_print):
        print cls.color_list["YELLOW"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def print_danger(cls, text_to_print):
        print cls.color_list["RED"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def print_header(cls, text_to_print):
        print cls.color_list["HEADER"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def print_header(cls, text_to_print):
        print cls.color_list["PURPLE"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def print_bold(cls, text_to_print):
        print cls.color_list["BOLD"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def print_underline(cls, text_to_print):
        print cls.color_list["UNDERLINE"] + text_to_print + cls.color_list["ENDLINE"]

    @classmethod
    def get_dynamic_class_instantiation(cls, package_name, module_name, parameters=None):

        logger.debug("Run plugin %s with parameter %s" % (module_name, parameters))
        mod = __import__(package_name, fromlist=[module_name])
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
