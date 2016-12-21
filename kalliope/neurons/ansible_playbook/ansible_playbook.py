from collections import namedtuple

import logging
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException

logging.basicConfig()
logger = logging.getLogger("kalliope")


class Ansible_playbook(NeuronModule):
    def __init__(self, **kwargs):
        super(Ansible_playbook, self).__init__(**kwargs)

        self.task_file = kwargs.get('task_file', None)
        self.sudo = kwargs.get('sudo', False)
        self.sudo_user = kwargs.get('sudo_user', False)
        self.sudo_password = kwargs.get('sudo_password', False)

        # check if parameters have been provided
        if self._is_parameters_ok():

            variable_manager = VariableManager()
            loader = DataLoader()
            options = self._get_options()
            passwords = {'become_pass': self.sudo_password}

            inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list="localhost")
            variable_manager.set_inventory(inventory)
            playbooks = [self.task_file]

            executor = PlaybookExecutor(
                playbooks=playbooks,
                inventory=inventory,
                variable_manager=variable_manager,
                loader=loader,
                options=options,
                passwords=passwords)

            executor.run()

    def _is_parameters_ok(self):
        if self.task_file is None:
            raise MissingParameterException("task_file parameter required")

        # check if the user want to use sudo for root privileges
        if self.sudo:
            # the user must set a login and password
            if not self.sudo_user:
                raise MissingParameterException("sudo_user parameter required with sudo True")
            if not self.sudo_password:
                raise MissingParameterException("sudo_password parameter required with sudo True")

        return True

    def _get_options(self):
        """
        Return a valid dict of option usable by Ansible depending on the sudo value if set
        :return: dict of option
        """
        Options = namedtuple('Options',
                             ['connection', 'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts',
                              'listtasks', 'listtags', 'syntax', 'module_path'])
        if self.sudo:
            options = Options(connection='local', forks=100, become=True, become_method="sudo",
                              become_user=self.sudo_user, check=False, listhosts=False, listtasks=False, listtags=False,
                              syntax=False, module_path="")
        else:
            options = Options(connection='local', forks=100, become=None, become_method=None, become_user=None,
                              check=False, listhosts=False, listtasks=False, listtags=False, syntax=False,
                              module_path="")

        logger.debug("Ansible options: %s" % str(options))
        return options
