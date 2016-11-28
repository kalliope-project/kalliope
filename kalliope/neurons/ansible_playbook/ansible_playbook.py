from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars import VariableManager
from ansible.inventory import Inventory
from ansible.executor.playbook_executor import PlaybookExecutor

from kalliope.core.NeuronModule import NeuronModule, MissingParameterException


class Ansible_playbook(NeuronModule):
    def __init__(self, **kwargs):
        super(Ansible_playbook, self).__init__(**kwargs)

        self.task_file = kwargs.get('task_file', None)

        # check if parameters have been provided
        if self._is_parameters_ok():

            Options = namedtuple('Options',
                                 ['connection', 'forks', 'become', 'become_method', 'become_user', 'check', 'listhosts',
                                  'listtasks', 'listtags', 'syntax', 'module_path'])

            variable_manager = VariableManager()
            loader = DataLoader()
            options = Options(connection='local', forks=100, become=None, become_method=None, become_user=None, check=False,
                              listhosts=False, listtasks=False, listtags=False, syntax=False, module_path="")
            passwords = dict(vault_pass='secret')

            inventory = Inventory(loader=loader, variable_manager=variable_manager, host_list='localhost')
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
        return True
