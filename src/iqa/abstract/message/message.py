from dataclasses import dataclass, field

from iqa.abstract.message.application_data import ApplicationData
from iqa.abstract.message.application_properties import ApplicationProperties
from iqa.abstract.message.delivery_annotations import DeliveryAnnotations
from iqa.abstract.message.footer import Footer
from iqa.abstract.message.header import Header
from iqa.abstract.message.message_annotations import MessageAnnotations
from iqa.abstract.message.properties import Properties

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

    header: Header = field(default_factory=Header)

    delivery_annotations: DeliveryAnnotations = field(
        default_factory=DeliveryAnnotations
    )

    message_annotations: MessageAnnotations = field(default_factory=MessageAnnotations)

    properties: Properties = field(default_factory=Properties)

    application_properties: ApplicationProperties = field(
        default_factory=ApplicationProperties
    )

    application_data: ApplicationData = field(default_factory=ApplicationData)

    footer: Footer = field(default_factory=Footer)
