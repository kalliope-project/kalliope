from core.OrderAnalyser import OrderAnalyser
from core.OrderListener import OrderListener

#
# oder = OrderListener()
#
# oder.start()

# test give hour
# order = "quelle heure est il?"

# test run script
order = "lance script jarvis"


order_analyser = OrderAnalyser(order)

order_analyser.start()

