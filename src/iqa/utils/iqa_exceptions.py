class IQAException(Exception):
    def __init__(self, message) -> None:
        # Call the base class constructor with the parameters it needs
        super(Exception, self).__init__(message)


class IQAConfigurationException(IQAException):
    def __init__(self, message) -> None:
        # Call the base class constructor with the parameters it needs
        super(IQAConfigurationException, self).__init__(message)
