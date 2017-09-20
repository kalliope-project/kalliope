#
# def test_check_event_dict(self):
#     valid_event = {
#         "hour": "18",
#         "minute": "16"
#     }
#     invalid_event = None
#     invalid_event2 = ""
#     invalid_event3 = {
#         "notexisting": "12"
#     }
#
#     self.assertTrue(ConfigurationChecker.check_event_dict(valid_event))
#
#     with self.assertRaises(NoEventPeriod):
#         ConfigurationChecker.check_event_dict(invalid_event)
#     with self.assertRaises(NoEventPeriod):
#         ConfigurationChecker.check_event_dict(invalid_event2)
#     with self.assertRaises(NoEventPeriod):
#         ConfigurationChecker.check_event_dict(invalid_event3)