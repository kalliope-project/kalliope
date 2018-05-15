import collections
import unittest

import mock

from kalliope.core import SignalModule
from kalliope.core.NotificationManager import NotificationManager


class FakeSignal(SignalModule):

    def __init__(self, name=None, **kwargs):
        super(FakeSignal, self).__init__(**kwargs)
        self.name = name

    def on_notification_received(self, notification=None, payload=None):
        pass

    @staticmethod
    def check_parameters(parameters):
        pass


class TestNotificationManager(unittest.TestCase):

    def setUp(self):
        if __name__ == '__main__':
            self.test_path = "__main__.FakeSignal.on_notification_received"
        else:
            self.test_path = "Tests.test_notification_manager.FakeSignal.on_notification_received"
        NotificationManager._instances.clear()

    def test_get_instances(self):
        # create a signal
        signal1 = FakeSignal()
        signal2 = FakeSignal()

        expected_list = [
            signal1, signal2
        ]
        compare = lambda x, y: collections.Counter(x) == collections.Counter(y)
        # convert received generator into list
        lst_from_notification = list(NotificationManager.get_instances())
        self.assertTrue(compare(expected_list, lst_from_notification))

    def test_send_notification(self):
        # create a signal
        signal1 = FakeSignal()
        # with mock.patch("__main__.FakeSignal.on_notification_received") \
        with mock.patch(self.test_path) \
                as mock_on_notification_received:
            test_notification = "test"

            NotificationManager.send_notification(test_notification)
            mock_on_notification_received.assert_called_once_with(notification=test_notification, payload=None)
            mock_on_notification_received.reset_mock()


if __name__ == '__main__':
    unittest.main()
