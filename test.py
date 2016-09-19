from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener

#
# oder = OrderListener()
#
# oder.start()

# test give hour
# order = "quelle heure est il?"

# test run script
# order = "lance script jarvis"

# run command
order = "playbook"
order_analyser = OrderAnalyser(order)

order_analyser.start()
# from neurons.ansible_tasks.ansible_tasks import Ansible_tasks
#
# tasks_file = "tasks.yml"
# ansible_tasks = Ansible_tasks(tasks_file)



