from . import Header, DeliveryAnnotations, MessageAnnotations,\
    Properties, ApplicationProperties, ApplicationData, Footer


class Message:
    """
    @TODO Create just abstract message class

    Mapping to specification is '1:1'

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
    def __init__(
            self,
            header=Header(),
            delivery_annotations=DeliveryAnnotations(),
            message_annotations=MessageAnnotations(),
            properties=Properties(),
            application_properties=None,
            application_data=ApplicationData(),
            footer=Footer()):

        if application_properties is None:
            application_properties = ApplicationProperties()
        self.header = header
        self.delivery_annotations = delivery_annotations
        self.message_annotations = message_annotations
        self.properties = properties
        self.application_properties = application_properties
        self.application_data = application_data
        self.footer = footer
