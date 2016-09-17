from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener

#
# oder = OrderListener()
#
# oder.start()

order = "quelle heure est il?"
order_analyser = OrderAnalyser(order)

order_analyser.start()

