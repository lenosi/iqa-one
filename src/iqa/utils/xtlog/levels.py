import logging


def init():
    """ Used to suppress unused import warning
    :return: None
    """
    pass


# creating DOC log level
logging.TEST_DOC = 15

# creating PASS/FAIL/SKIP test log levels
logging.TEST_PASS = 28
logging.TEST_FAIL = 27
logging.TEST_SKIP = 26
logging.TEST = 21  # virtual log level for enabling testing logging up to TEST level

name_map = {
    'critical': logging.CRITICAL,
    'error': logging.ERROR,
    'warning': logging.WARNING,
    'pass': logging.TEST_PASS,
    'fail': logging.TEST_FAIL,
    'skip': logging.TEST_SKIP,
    'test': logging.TEST,
    'info': logging.INFO,
    'testdoc': logging.TEST_DOC,
    'debug': logging.DEBUG,
    'notset': logging.NOTSET,
}

# adding level mappings
logging.addLevelName(logging.TEST_DOC, 'DOC')
logging.addLevelName(logging.TEST_PASS, 'PASS')
logging.addLevelName(logging.TEST_FAIL, 'FAIL')
logging.addLevelName(logging.TEST_SKIP, 'SKIP')
logging.addLevelName(logging.TEST, 'TEST')


def test_doc(self, message, *args, **kwargs):
    self._log(logging.TEST_DOC, message, args, **kwargs)


def test_pass(self, message, *args, **kwargs):
    self._log(logging.TEST_PASS, message, args, **kwargs)


def test_fail(self, message, *args, **kwargs):
    self._log(logging.TEST_FAIL, message, args, **kwargs)


def test_skip(self, message, *args, **kwargs):
    self._log(logging.TEST_SKIP, message, args, **kwargs)


logging.Logger.test_doc = test_doc
logging.Logger.test_pass = test_pass
logging.Logger.test_fail = test_fail
logging.Logger.test_skip = test_skip
