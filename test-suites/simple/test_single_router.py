from iqa.messaging_abstract.message import Message
from tests import get_func_name


def test_send_receive(in_node, out_node, sender_node, receiver_node):
    """
    Basic send & receive
    :param in_node: input node, node which where senders sends all messages
    :type in_node: Node
    :param out_node: output node, node from which all receivers receive all messages
    :type out_node: Node
    :param sender_node: node which contains sender
    :type sender_node: Node
    :param receiver_node: node which contains receiver
    :type receiver_node: Node
    :return:
    """
    message = Message()
    sender_node.send(node=in_node, address=get_func_name(), messages=[message])
    receiver_node.receive(node=out_node, address=get_func_name())
    assert sender_node.last_message._get_id() == receiver_node.last_message._get_id()
