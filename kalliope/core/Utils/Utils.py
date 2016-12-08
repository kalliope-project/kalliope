import logging
import os
import inspect

logging.basicConfig()
logger = logging.getLogger("kalliope")


def pipe_print(line):
    print(line.encode('utf-8'))


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

    ##################
    #
    # Shell properly displayed
    #
    #########
    @classmethod
    def print_info(cls, text_to_print):
        pipe_print(cls.color_list["BLUE"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_success(cls, text_to_print):
        pipe_print(cls.color_list["GREEN"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_warning(cls, text_to_print):
        pipe_print(cls.color_list["YELLOW"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_danger(cls, text_to_print):
        pipe_print(cls.color_list["RED"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_header(cls, text_to_print):
        pipe_print(cls.color_list["HEADER"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_header(cls, text_to_print):
        pipe_print(cls.color_list["PURPLE"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_bold(cls, text_to_print):
        pipe_print(cls.color_list["BOLD"] + text_to_print + cls.color_list["ENDLINE"])

    @classmethod
    def print_underline(cls, text_to_print):
        pipe_print(cls.color_list["UNDERLINE"] + text_to_print + cls.color_list["ENDLINE"])

    @staticmethod
    def print_yaml_nicely(to_print):
        """
        Used for debug
        :param to_print: Dict to print nicely
        :return:
        """
        import json
        pipe_print(json.dumps(to_print, indent=2))

    ##################
    #
    # Dynamic loading
    #
    #########
    @staticmethod
    def get_dynamic_class_instantiation(package_name, module_name, parameters=None):
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
        module_name_with_path = "kalliope." + package_name + "." + module_name.lower() + "." + module_name.lower()
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

    ##################
    #
    # Paths management
    #
    #########
    @staticmethod
    def get_current_file_parent_parent_path(current_script_path):
        parent_parent_path = os.path.normpath(current_script_path + os.sep + os.pardir + os.sep + os.pardir)
        return parent_parent_path

    @staticmethod
    def get_current_file_parent_path(current_script_path):
        parent_path = os.path.normpath(current_script_path + os.sep + os.pardir)
        return parent_path

    @classmethod
    def get_real_file_path(cls, file_path_to_test):
        """
        Try to return a full path from a given <file_path_to_test>
        If the path is an absolute on, we return it directly.

        If the path is relative, we try to get the full path in this order:
        - from the current directory where kalliope has been called + the file_path_to_test.
        Eg: /home/me/Documents/kalliope_config
        - from /etc/kalliope + file_path_to_test
        - from the default file passed as <file_name> at the root of the project

        :param file_path_to_test file path to test
        :type file_path_to_test: str
        :return: absolute path to the file file_path_to_test or None if is doen't exist
        """

        if not os.path.isabs(file_path_to_test):
            current_script_path = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
            path_order = {
                1: os.getcwd() + os.sep + file_path_to_test,
                2: "/etc/kalliope" + os.sep + file_path_to_test,
                # In this case 'get_current_file_parent_parent_path' is corresponding to kalliope root path
                # from /an/unknown/path/kalliope/kalliope/core/Utils to /an/unknown/path/kalliope/kalliope
                3: cls.get_current_file_parent_parent_path(current_script_path) + os.sep + file_path_to_test
            }

            for key in sorted(path_order):
                new_file_path_to_test = path_order[key]
                logger.debug("Try to load file from %s: %s" % (key, new_file_path_to_test))
                if os.path.isfile(new_file_path_to_test):
                    logger.debug("File found in %s" % new_file_path_to_test)
                    return new_file_path_to_test

        else:
            if os.path.isfile(file_path_to_test):
                return file_path_to_test
            else:
                return None
