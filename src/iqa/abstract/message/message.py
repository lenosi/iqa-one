from dataclasses import dataclass, field

import iqa.abstract.message as message

# noinspection PyDunderSlots
@dataclass(frozen=False)
class Message:
    """Mapping to specification is '1:1'

    This class is based on AMQP 1.0 specifics (3.2) Message Format

                                                              Bare Message
                                                                |
                                          .---------------------+--------------------.
                                          |                                          |
     +--------+-------------+-------------+------------+--------------+--------------+--------+
     | header | delivery-   | message-    | properties | application- | application- | footer |
     |        | annotations | annotations |            | properties   | data (body)  |        |
     +--------+-------------+-------------+------------+--------------+--------------+--------+
     |                                                                                        |
     '-------------------------------------------+--------------------------------------------'
                                                 |
                                          Annotated Message
    """
    # __slots__ = ['header', 'delivery_annotations', 'message_annotations',
    #              'properties', 'application_properties', 'application_data',
    #              'footer']

    header: message.Header = \
        field(default_factory=message.Header)

    delivery_annotations: message.DeliveryAnnotations = \
        field(default_factory=message.DeliveryAnnotations)

    message_annotations: message.MessageAnnotations = \
        field(default_factory=message.MessageAnnotations)

    properties: message.Properties = \
        field(default_factory=message.Properties)

    application_properties: message.ApplicationProperties = \
        field(default_factory=message.ApplicationProperties)

    application_data: message.ApplicationData = \
        field(default_factory=message.ApplicationData)

    footer: message.Footer = \
        field(default_factory=message.Footer)
