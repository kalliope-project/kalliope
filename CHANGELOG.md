2020-11-11 Idle wakeup enhancement
================================
- Enhancement: pause the trigger for long periods to conserve battery life on mobile devices while
  leaving current behaviour as 'Desktop' mode.
   - add signal handler for SIGCONT in kalliope::main
   - order.py 
       - add threading event 
       - add wakeup function to be called from SIGCONT signal handler
       - rewrote waiting_for_trigger_callback_thread
   - add Desktop icon that sends SIGCONT to Kalliope
- Deficiencies
   - variables are in user controlled variable file, should be app default file 
       - sorry, new to python, my brain hurts, why can't SettingLoader load dicts automagically?
       - finish_time can be an internal variable, user access is not required
