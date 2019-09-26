from dataclasses import dataclass, field

# noinspection PyDunderSlots
@dataclass(frozen=False)
class Properties:
    """
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

    The properties section is used for a defined set of standard properties of
    the message. The properties section is part of the bare message; therefore,
    if retransmitted by an intermediary, it MUST remain unaltered.


    :param message-id:	application message identifier
    Message-id, if set, uniquely identifies a message within the message system.
    The message producer is usually responsible for setting the message-id in
    such a way that it is assured to be globally unique. A broker MAY discard
    a message as a duplicate if the value of the message-id matches that of
    a previously received message sent to the same node.
    optional *

    :param user-id:	creating user id
    The identity of the user responsible for producing the message. The client
    sets this value, and it MAY be authenticated by intermediaries.
    optional binary

    to	the address of the node the message is destined for	optional *
    The to field identifies the node that is the intended destination of the
    message. On any given transfer this might not be the node at the receiving
    end of the link.

    subject	the subject of the message	optional string
    A common field for summary information about the message content and purpose.

    :param reply-to: the node to send replies to
    The address of the node to send replies to.
    optional *

    :param correlation-id: application correlation identifier	optional *
    This is a client-specific id that can be used to mark or identify messages
    between clients.

    :param content-type: MIME content type
    The RFC-2046 [RFC2046] MIME type for the message's application-data
    section (body). As per RFC-2046 [RFC2046] this can contain a charset
    parameter defining the character encoding used: e.g.,
    'text/plain; charset="utf-8"'.
    optional symbol

    For clarity, as per section 7.2.1 of RFC-2616 [RFC2616], where the content
    type is unknown the content-type SHOULD NOT be set. This allows the
    recipient the opportunity to determine the actual type. Where the section
    is known to be truly opaque binary data, the content-type SHOULD be set to
    application/octet-stream.

    When using an application-data section with a section code
    other than data, content-type SHOULD NOT be set.

    :param content-encoding: MIME content type
    The content-encoding property is used as a modifier to the content-type.
    When present, its value indicates what additional content encodings have
    been applied to the application-data, and thus what decoding mechanisms
    need to be applied in order to obtain the media-type referenced by the
    content-type header field.
    optional symbol

    Content-encoding is primarily used to allow a document to be compressed
    without losing the identity of its underlying content type.

    Content-encodings are to be interpreted as per section 3.5 of RFC 2616
    [RFC2616]. Valid content-encodings are registered at IANA [IANAHTTPPARAMS].

    The content-encoding MUST NOT be set when the application-data section is
    other than data. The binary representation of all other application-data
    section types is defined completely in terms of the AMQP type system.

    Implementations MUST NOT use the identity encoding. Instead,
    implementations SHOULD NOT set this property. Implementations SHOULD NOT
    use the compress encoding, except as to remain compatible with messages
    originally sent with other protocols, e.g. HTTP or SMTP.

    Implementations SHOULD NOT specify multiple content-encoding values
    except as to be compatible with messages originally sent with other
    protocols, e.g. HTTP or SMTP.

   :param absolute-expiry-time: the time when this message is considered expired
    An absolute time when this message is considered to be expired.
    optional timestamp

    :param creation-time: the time when this message was created
    An absolute time when this message was created.
    optional timestamp

    :param group-id: the group this message belongs to
    Identifies the group the message belongs to.
    optional string

    :param group-sequence: the sequence-no of this message within its group
    The relative position of this message within its group.
    optional sequence-no

    :param reply-to-group-id:	the group the reply message belongs to
    This is a client-specific id that is used so that client can send replies
    to this message to a specific group.
    optional string
    """
    message_id: str = None
    user_id: str = None
    to: str = None
    subject: str = None
    reply_to: str = None
    correlation_id: str = None
    content_type: str = None
    content_encoding: str = None
    absolute_expiry_time: str = None
    creation_time: str = None
    group_id: str = None
    group_sequence: str = None
    reply_to_group_id: str = None

    def __str__(self):
        text = \
            """
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
"""
        return text
