import unittest

import mock

from kalliope.signals.order import Order


class TestOrder(unittest.TestCase):

    def test_on_notification_received(self):
        testing_order = Order()

        # received valid notification skip_trigger
        notification = "skip_trigger"
        payload = {
            "status": True
        }
        with mock.patch("kalliope.signals.order.order.Order.switch_trigger") as mock_switch_trigger_method:
            testing_order.on_notification_received(notification=notification, payload=payload)
            mock_switch_trigger_method.assert_called_once_with(payload)

        # received valid notification skip_trigger_max_retry
        notification = "skip_trigger_max_retry"
        payload = {
            "max_retry": 5
        }
        with mock.patch("kalliope.signals.order.order.Order.set_counter_max_retry") as mock_set_counter_max_retry_method:
            testing_order.on_notification_received(notification=notification, payload=payload)
            mock_set_counter_max_retry_method.assert_called_once()

        # received valid notification skip_trigger_decrease_max_retry
        notification = "skip_trigger_decrease_max_retry"
        payload = None
        with mock.patch(
                "kalliope.signals.order.order.Order.decrease_max_retry") as mock_decrease_max_retry_method:
            testing_order.on_notification_received(notification=notification, payload=payload)
            mock_decrease_max_retry_method.assert_called_once()

    def test_set_counter_max_retry(self):

        # test valid payload
        testing_order = Order()
        payload = {
            "max_retry": 5
        }
        testing_order.set_counter_max_retry(payload)
        self.assertEqual(testing_order.counter_max_retry, 5)

        # test invalid payload
        testing_order = Order()
        payload = {
            "max_retry": -12
        }
        testing_order.set_counter_max_retry(payload)
        self.assertEqual(testing_order.counter_max_retry, 0)

        testing_order = Order()
        payload = {
            "wrong_key": 5
        }
        testing_order.set_counter_max_retry(payload)
        self.assertEqual(testing_order.counter_max_retry, 0)

    def decrease_max_retry(self):

        # counter should not move because 0 by default
        testing_order = Order()
        testing_order.decrease_max_retry()
        self.assertEqual(testing_order.counter_max_retry, 0)

        # update the counter
        testing_order = Order()
        testing_order.counter_max_retry = 5
        testing_order.decrease_max_retry()
        self.assertEqual(testing_order.counter_max_retry, 4)

        # update the counter and reach 0
        testing_order = Order()
        testing_order.skip_trigger = True
        testing_order.counter_max_retry = 1
        testing_order.decrease_max_retry()
        self.assertEqual(testing_order.counter_max_retry, 0)
        self.assertFalse(testing_order.skip_trigger)

    def test_switch_trigger(self):

        # valid payload
        testing_order = Order()
        payload = {
            "status": True
        }
        testing_order.switch_trigger(payload)
        self.assertTrue(testing_order.skip_trigger)

        testing_order = Order()
        payload = {
            "status": "True"
        }
        testing_order.switch_trigger(payload)
        self.assertTrue(testing_order.skip_trigger)

        testing_order = Order()
        payload = {
            "status": False
        }
        testing_order.switch_trigger(payload)
        self.assertFalse(testing_order.skip_trigger)

        testing_order = Order()
        payload = {
            "status": "False"
        }
        testing_order.switch_trigger(payload)
        self.assertFalse(testing_order.skip_trigger)

        # invalid payload
        testing_order = Order()
        payload = {
            "non-existing": "False"
        }
        testing_order.switch_trigger(payload)
        self.assertFalse(testing_order.skip_trigger)

        testing_order = Order()
        payload = {
            "status": "test"
        }
        testing_order.switch_trigger(payload)
        self.assertFalse(testing_order.skip_trigger)


if __name__ == '__main__':
    unittest.main()
