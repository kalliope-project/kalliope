# coding: utf8
import logging

from gmail import Gmail
from email.header import decode_header
from core.NeuronModule import NeuronModule

logging.basicConfig()
logger = logging.getLogger("jarvis")


class MissingParameterException(Exception):
    pass


class Gmail_checker(NeuronModule):
    def __init__(self, **kwargs):
        super(Gmail_checker, self).__init__(**kwargs)

        # check if parameters have been provided
        username = kwargs.get('username', None)
        password = kwargs.get('password', None)

        if username is None:
            raise MissingParameterException("Username parameter required")

        if password is None:
            raise MissingParameterException("Password parameter required")

        # prepare a returned dict
        returned_dict = dict()

        g = Gmail()
        g.login(username, password)

        # check if login succeed
        logging.debug("Gmail loggin ok: %s" % g.logged_in)  # Should be True, AuthenticationError if login fails

        # get unread mail
        unread = g.inbox().mail(unread=True)

        returned_dict["unread"] = len(unread)

        if len(unread) > 0:
            # add a list of subject
            subject_list = list()
            for email in unread:
                email.fetch()
                encoded_subject = email.subject
                subject = self._parse_subject(encoded_subject)
                subject_list.append(subject)

            returned_dict["subjects"] = subject_list

        print returned_dict
        # logout of gmail
        g.logout()

    @staticmethod
    def _parse_subject(encoded_subject):
        dh = decode_header(encoded_subject)
        # TODO decode that shit
        print str(encoded_subject.decode("ascii").encode("utf8"))
        default_charset = 'ASCII'
        string = ''.join([unicode(t[0], t[1] or default_charset) for t in dh])
        print type(string)
        return string.encode('utf8')

