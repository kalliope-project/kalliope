import inspect
import os
import unittest


class TestDynamicLoading(unittest.TestCase):

    """
    Test case for dynamic loading of python class
    This is used to test we can successfully import:
    - STT engine
    - TTS engine
    - Trigger engine
    - All core neurons
    """

    def setUp(self):
        # get current script directory path. We are in /an/unknown/path/kalliope/core/Tests
        cur_script_directory = os.path.dirname(os.path.abspath(inspect.getfile(inspect.currentframe())))
        # get parent dir. Now we are in /an/unknown/path/kalliope
        root_dir = os.path.normpath(cur_script_directory + os.sep + os.pardir)

        # get the neuron dir
        self.neurons_dir = os.path.normpath(root_dir + os.sep + "kalliope/neurons")

        # get stt dir
        self.stt_dir = os.path.normpath(root_dir + os.sep + "kalliope/stt")

        # get tts dir
        self.tts_dir = os.path.normpath(root_dir + os.sep + "kalliope/tts")

        # get trigger dir
        self.trigger_dir = os.path.normpath(root_dir + os.sep + "kalliope/trigger")

    def test_packages_present(self):
        """
        Check that the neurons folder exist in the root of the project
        """
        self.assertTrue(os.path.isdir(self.neurons_dir))
        self.assertTrue(os.path.isdir(self.stt_dir))
        self.assertTrue(os.path.isdir(self.tts_dir))
        self.assertTrue(os.path.isdir(self.trigger_dir))

    def test_can_import_neurons(self):
        """
        Try to import each neurons that are present in the neurons package
        :return:
        """
        neurons = self.get_package_in_folder(self.neurons_dir)
        package_name = "neurons"
        for neuron_name in neurons:
            module_name = neuron_name.capitalize()
            self.dynamic_import(package_name, module_name)

    def test_can_import_stt(self):
        """
        Try to import each stt that are present in the stt package
        :return:
        """
        stts = self.get_package_in_folder(self.stt_dir)
        package_name = "stt"
        for stt_name in stts:
            module_name = stt_name.capitalize()
            self.dynamic_import(package_name, module_name)

    def test_can_import_tts(self):
        """
        Try to import each tts that are present in the tts package
        :return:
        """
        ttss = self.get_package_in_folder(self.tts_dir)
        package_name = "tts"
        for tts_name in ttss:
            module_name = tts_name.capitalize()
            self.dynamic_import(package_name, module_name)

    def test_can_import_trigger(self):
        """
        Try to import each trigger that are present in the trigger package
        :return:
        """
        triggers = self.get_package_in_folder(self.trigger_dir)
        package_name = "trigger"
        for trigger in triggers:
            module_name = trigger.capitalize()
            self.dynamic_import(package_name, module_name)

    @staticmethod
    def get_package_in_folder(folder):
        """
        receive a path in <folder>, return a list of package in that folder.
        The function test if elements in that path are directory and return a list of those directory
        :param folder: Path of a folder to return package
        :return: list of package name
        """
        # get the list of neurons in the neurons packages
        el_folder = os.listdir(folder)
        # we keep only package. Because we have _init_.py or other stuff in what listdir returned
        packages_in_folder = list()
        for el in el_folder:
            if os.path.isdir(folder + os.sep + el):
                packages_in_folder.append(el)
        return packages_in_folder

    def dynamic_import(self, package_name, module_name):
        """
        Dynamic import of a module by its name.
        package name can be:
        - triggers
        - neurons
        - stt
        - tts
        :param package_name: name of the mother package
        :param module_name: module name to load
        :return:
        """
        module_name_with_path = "kalliope." + package_name + "." + module_name.lower() + "." + module_name.lower()
        mod = __import__(module_name_with_path, fromlist=[module_name])
        try:
            getattr(mod, module_name)
        except AttributeError:
            self.fail("The module %s does not exist in package %s" % (module_name, package_name))


if __name__ == '__main__':
    unittest.main()
