from collections import namedtuple

import logging

import yaml
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.inventory.manager import InventoryManager
from ansible.parsing.dataloader import DataLoader
from ansible.playbook.play import Play
from ansible.vars.manager import VariableManager

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
            options = self._get_options()

            # initialize needed objects
            loader = DataLoader()

            passwords = {'become_pass': self.sudo_password}

            inventory = InventoryManager(loader=loader, sources="localhost,")

            # variable manager takes care of merging all the different sources to give you a unified
            # view of variables available in each context
            variable_manager = VariableManager(loader=loader, inventory=inventory)
            variable_manager.set_inventory(inventory)

            playbooks = None
            with open(self.task_file, 'r') as stream:
                try:
                    playbooks = yaml.full_load(stream)
                except yaml.YAMLError as exc:
                    print(exc)

            play = Play().load(playbooks[0], variable_manager=variable_manager, loader=loader)

            # Run it - instantiate task queue manager, which takes care of forking and setting up all objects
            # to iterate over host list and tasks
            tqm = None
            try:
                tqm = TaskQueueManager(
                    inventory=inventory,
                    variable_manager=variable_manager,
                    loader=loader,
                    options=options,
                    passwords=passwords,
                    stdout_callback='default',
                    # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
                )
                tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
            finally:
                # we always need to cleanup child procs and the structres we use to communicate with them
                if tqm is not None:
                    tqm.cleanup()

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
                              'listtasks', 'listtags', 'syntax', 'module_path', 'diff'])
        if self.sudo:
            options = Options(connection='local', forks=100, become=True, become_method="sudo",
                              become_user=self.sudo_user, check=False, listhosts=False, listtasks=False, listtags=False,
                              syntax=False, module_path="", diff=False)
        else:
            options = Options(connection='local', forks=100, become=None, become_method=None, become_user=None,
                              check=False, listhosts=False, listtasks=False, listtags=False, syntax=False,
                              module_path="", diff=False)

        logger.debug("Ansible options: %s" % str(options))
        return options
