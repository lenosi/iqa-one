import logging
import iqa.utils.xtlog.levels as levels


class XTLogAdapter(logging.LoggerAdapter, object):
    """ base class that adds test logging methods
    """

    test_pass = levels.test_pass
    test_fail = levels.test_fail
    test_skip = levels.test_skip
    test_doc = levels.test_doc


class AuxAdapter(XTLogAdapter):
    """ Logging adapter that is able to supply additional info to messages
    """

    def process(self, msg, kwargs):
        """ Adding dictionary form data in extra field to the end of log message
        @param msg: log message
        @param kwargs: (internal) logging data
        @return: processed msg and pass through kwargs
        """
        tmp = []
        for k, v in self.extra.iteritems():
            tmp.append("%s=%s" % (k, v,))
        return "%s extra={%s}" % (msg, ", ".join(tmp)), kwargs


class RemoteExecAdapter(XTLogAdapter):
    """ Remote execution logger adapter, that add IP address to log messages
    """

    def __init__(self, logger, extra):
        """ overridden L{logging.LoggerAdapter} init, this will try to efficiently extra 'host' from extras
        @type logger: L{logging.Logger}
        @param logger: logger instance
        @type extra: dict
        @param extra: extra data
        @return: None
        """
        super(RemoteExecAdapter, self).__init__(logger, extra)
        self.host = self.extra.get('host', None)
        self.user = self.extra.get('user', None)

    def process(self, msg, kwargs):
        """ Adding specified 'host' (IP address) at the beginning of log message
        @param msg: log message
        @param kwargs: internal params
        @return: log message + internal params pass through
        """
        return '[%s@%s]$ %s' % (self.user, self.host, msg), kwargs


class GeneralContextAdapter(XTLogAdapter):
    """ General purpose context adapter, prepending context to a log message
    """

    def process(self, msg, kwargs):
        """ Adding specified 'context' at the beginning of log message

        @param msg: log message
        @param kwargs: internal params
        @return: post processed log message + internal params pass through
        """
        context = self.extra.get('context')
        separator = self.extra.get('separator', ':')
        return "%s%s%s" % (context, separator, msg), kwargs
