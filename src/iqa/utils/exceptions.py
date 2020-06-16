class IQAException(Exception):
    def __init__(self, message) -> None:
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)


class IQAConfigurationException(IQAException):
    def __init__(self, message) -> None:
        # Call the base class constructor with the parameters it needs
        super(IQAConfigurationException, self).__init__(message)


class IQAHostTimeoutException(IQAException):
    """Host timeout error with IP address"""

    def __init__(self, ip_address):
        self.ip_address = ip_address
        self.msg = "Host {} Timeout Error".format(ip_address)
        super().__init__(self.msg)


class IQAHostDisconnectException(IQAException):
    """Host disconnect error with IP address"""

    def __init__(self, ip_address, reason):
        self.ip_address = ip_address
        self.reason = reason
        self.msg = "Host {} Disconnect Error: {}".format(ip_address, reason)
        super().__init__(self.msg)
