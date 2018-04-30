import logging
import weakref

logging.basicConfig()
logger = logging.getLogger("kalliope")


class NotificationManager(object):
    """
    Class sued to send messages to all instantiated object that use it as parent class
    """
    _instances = set()

    def __init__(self):
        self._instances.add(weakref.ref(self))
        logger.debug("[NotificationManager] Add new instance to the manager")

    @classmethod
    def get_instances(cls):
        dead = set()
        for ref in cls._instances:
            obj = ref()
            if obj is not None:
                yield obj
            else:
                dead.add(ref)
        cls._instances -= dead

    @classmethod
    def send_notification(cls, notification=None, payload=None):
        logger.debug("[NotificationManager] send notification to all child: notification: %s, payload: %s"
                     % (notification, payload))
        for instance in cls.get_instances():
            try:
                instance.on_notification_received(notification=notification, payload=payload)
            except NotImplementedError:
                logger.debug("[NotificationManager] The signal %s does not implement send_notification method"
                             % instance.__class__.__name__)
                pass
