from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener

#
# oder = OrderListener()
#
# oder.start()

order = "jarvis dit bonjour s'il te plait"
order_analyser = OrderAnalyser(order)

order_analyser.start()

