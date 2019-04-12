class Properties:
    """
    @TODO

    Immutable properties of the message.

    <type name="properties" class="composite" source="list" provides="section">
        <descriptor name="amqp:properties:list" code="0x00000000:0x00000073"/>
        <field name="message-id" type="*" requires="message-id"/>
        <field name="user-id" type="binary"/>
        <field name="to" type="*" requires="address"/>
        <field name="subject" type="string"/>
        <field name="reply-to" type="*" requires="address"/>
        <field name="correlation-id" type="*" requires="message-id"/>
        <field name="content-type" type="symbol"/>
        <field name="content-encoding" type="symbol"/>
        <field name="absolute-expiry-time" type="timestamp"/>
        <field name="creation-time" type="timestamp"/>
        <field name="group-id" type="string"/>
        <field name="group-sequence" type="sequence-no"/>
        <field name="reply-to-group-id" type="string"/>
    </type>

    The properties section is used for a defined set of standard properties of the message. The properties section
    is part of the bare message; therefore, if retransmitted by an intermediary, it MUST remain unaltered.
    """
    def __init__(self,
                 message_id=None,
                 user_id=None,
                 to=None,
                 subject=None,
                 reply_to=None,
                 correlation_id=None,
                 content_type=None,
                 content_encoding=None,
                 absolute_expiry_time=None,
                 creation_time=None,
                 group_id=None,
                 group_sequence=None,
                 reply_to_group_id=None):

        self.message_id = message_id
        self.user_id = user_id
        self.to = to
        self.subject = subject
        self.reply_to = reply_to
        self.correlation_id = correlation_id
        self.content_type = content_type
        self.content_encoding = content_encoding
        self.absolute_expiry_time = absolute_expiry_time
        self.creation_time = creation_time
        self.group_id = group_id
        self.group_sequence = group_sequence
        self.reply_to_group_id = reply_to_group_id
