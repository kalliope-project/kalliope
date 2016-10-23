

class Cache2(object):
    def __init__(self):
        pass

    @classmethod
    def get_file_path_from_text(cls, sentence, tts):
        """
        Get a sentence (a text) an return the full path of the file

        Path syntax:
        </path/in/settings>/<tts.name>/tts.parameter["language"]/<md5_of_sentence.tts

        E.g:
        /tmp/kalliope/voxygene/fr/abcd12345.tts

        :param sentence:
        :param tts: The Tts model instance that contain parameter like language, key, etc...
        :type tts: Tts
        :return: path String
        """
        pass

    @classmethod
    def delete_file(cls, file_path):
        """
        Delete the file in path <file_path>
        :param file_path:
        :return:
        """
        pass

    @staticmethod
    def _generate_md5_from_text(text):
        """
        Local function to generate a md5 hash from a string sentence
        :param text:
        :return: String
        """
        pass