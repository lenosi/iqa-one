import logging


class EqualsLevelFilter(logging.Filter):
    """ Logging filter to filter only one precise log level """
    def __init__(self, level):
        """
        @type level: int
        @param level: log level to filter by
        @return: None
        @rtype: NoneType
        """
        logging.Filter.__init__(self)
        self.level = level

    def filter(self, record):
        """
        @param record: log record being logged
        @return: True - if log level match, False - otherwise
        """
        return record.levelno == self.level
