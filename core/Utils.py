

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