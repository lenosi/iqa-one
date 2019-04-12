class Header:
    """
    3.2.1 Header
    Transport headers for a message.

    <type name="header" class="composite" source="list" provides="section">
        <descriptor name="amqp:header:list" code="0x00000000:0x00000070"/>
        <field name="durable" type="boolean" default="false"/>
        <field name="priority" type="ubyte" default="4"/>
        <field name="ttl" type="milliseconds"/>
        <field name="first-acquirer" type="boolean" default="false"/>
        <field name="delivery-count" type="uint" default="0"/>
    </type>

    The header section carries standard delivery details about the transfer of a message through the AMQP network.
    If the header section is omitted the receiver MUST assume the appropriate default values (or the meaning implied
    by no value being set) for the fields within the header unless other target or node specific defaults have
    otherwise been set.
    """

    def __init__(self, durable=None, priority=None, ttl=None, first_acquirer=None, delivery_count=None):
        """
        :param durable: specify durability requirements (optional)
        :param priority: relative message priority (optional)
        :param ttl: time to live in ms (optional)
        :param first_acquirer: (optional)
        :param delivery_count: the number of prior unsuccessful delivery attempts (optional)
        """
        self._durable = durable
        self._priority = priority
        self._ttl = ttl
        self._first_acquirer = first_acquirer
        self._delivery_count = delivery_count

    # Durable
    @property
    def durable(self):
        """

        Durable messages MUST NOT be lost even if an intermediary is unexpectedly terminated and restarted. A target
        which is not capable of fulfilling this guarantee MUST NOT accept messages where the durable header is set
        to true: if the source allows the rejected outcome then the message SHOULD be rejected with the
        precondition-failed error, otherwise the link MUST be detached by the receiver with the same error.
        :return: boolean
        """
        return self._durable

    @durable.setter
    def durable(self, value):
        self._durable = value

    # Priority
    @property
    def priority(self):
        """
        This field contains the relative message priority. Higher numbers indicate higher priority messages.
        Messages with higher priorities MAY be delivered before those with lower priorities.

        An AMQP intermediary implementing distinct priority levels MUST do so in the following manner:

        If n distinct priorities are implemented and n is less than 10 -- priorities 0 to (5 - ceiling(n/2))
        MUST be treated equivalently and MUST be the lowest effective priority. The priorities (4 + floor(n/2))
        and above MUST be treated equivalently and MUST be the highest effective priority.
        The priorities (5 - ceiling(n/2)) to (4 + floor(n/2)) inclusive MUST be treated as distinct priorities.

        If n distinct priorities are implemented and n is 10 or greater -- priorities 0 to (n - 1) MUST be distinct,
        and priorities n and above MUST be equivalent to priority (n - 1).

        Thus, for example, if 2 distinct priorities are implemented, then levels 0 to 4 are equivalent,
        and levels 5 to 9 are equivalent and levels 4 and 5 are distinct. If 3 distinct priorities are implements
        the 0 to 3 are equivalent, 5 to 9 are equivalent and 3, 4 and 5 are distinct.

        This scheme ensures that if two priorities are distinct for a server which implements m separate priority
        levels they are also distinct for a server which implements n different priority levels where n > m.

        :return: ubyte
        """
        return self._priority

    @priority.setter
    def priority(self, value):
        """
        :param value: ubyte
        """
        self._priority = value

    # TTL
    @property
    def ttl(self):
        """
        Duration in milliseconds for which the message is to be considered "live". If this is set then a message
        expiration time will be computed based on the time of arrival at an intermediary. Messages that live longer
        than their expiration time will be discarded (or dead lettered). When a message is transmitted by an
        intermediary that was received with a ttl, the transmitted message's header SHOULD contain a ttl that is
        computed as the difference between the current time and the formerly computed message expiration time, i.e.,
        the reduced ttl, so that messages will eventually die if they end up in a delivery loop.
        :return: int (milliseconds)
        """
        return self._ttl

    @ttl.setter
    def ttl(self, value):
        """
        :param value: int (milliseconds)
        """
        self._ttl = value

    # First acquirer
    @property
    def first_acquirer(self):
        """
        If this value is true, then this message has not been acquired by any other link (see section 3.3).
        If this value is false, then this message MAY have previously been acquired by another link or links.
        :return boolean
        """
        return self._first_acquirer

    @first_acquirer.setter
    def first_acquirer(self, value):
        """
        :param value: boolean
        """
        self._first_acquirer = value

    # Delivery count
    @property
    def delivery_count(self):
        """
        The number of unsuccessful previous attempts to deliver this message. If this value is non-zero it can be
        taken as an indication that the delivery might be a duplicate. On first delivery, the value is zero. It is
        incremented upon an outcome being settled at the sender, according to rules defined for each outcome.
        :return: uint
        """
        return self._delivery_count

    @delivery_count.setter
    def delivery_count(self, value):
        """
        The number of prior unsuccessful delivery attempts	(optional)
        :param value: uint
        """
        self._delivery_count = value
