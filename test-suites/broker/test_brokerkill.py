# -*- coding: utf-8 -*-

from proton import Message, Event
from proton.handlers import MessagingHandler
from proton.reactor import Container
import time

from iqa.components.brokers import Artemis


class SendMessage(MessagingHandler):
    """Simply send and receive client"""
    def __init__(self, server, address):
        SendMessage.__init__()
        self.server = server
        self.address = address

    def on_start(self, event: Event):
        conn = event.container.connect(self.server)
        event.container.create_receiver(conn, self.address)
        event.container.create_sender(conn, self.address)

    def on_sendable(self, event: Event):
        event.sender.send(Message(body="Test message"))
        event.sender.close()
        event.receiver.close()
        event.connection.close()

    def on_message(self, event):
        print(event.message.body)
        event.connection.close()


def test_node_ip(master1: Artemis, slave1: Artemis, slave2: Artemis):

    # Client01.start(master1.lister('test_listener'))
    # Client01.send(address=broker2.address('abcd') msg=message)

    exec = master1.node.execute(['killall', 'java'])
    assert True if exec.get_ecode() == 0 else False

    time.sleep(15)

    # message = Message(content='Test message')
    # Client01.send(broker2.lister('test_listener'), address=broker2.address('abcd') msg=message)

    client = Container(SendMessage("%s:5672" % slave1.node.ip, "examples"))
    client.run()
