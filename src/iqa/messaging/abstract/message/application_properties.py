class Property:
    """
    The keys of this map are restricted to be of type string (which excludes the possibility of a null key)
    and the values are restricted to be of simple types only, that is, excluding map, list, and array types.
    """

    def __init__(self, name, value=None):
        self.name = name
        self.value = value


class ApplicationProperties(list):
    """
    The application-properties section is a part of the bare message used for structured application data.
    Intermediaries can use the data within this structure for the purposes of filtering or routing.

    """

    def add_property(self, name, value):
        """
        Add property to message Application properties
        :param name:
        :param value:
        :return:
        """
        self.append(Property(name=name, value=value))
