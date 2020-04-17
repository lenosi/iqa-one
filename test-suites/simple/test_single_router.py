from iqa.abstract.message.message import Message
from iqa.utils.types import NodeType


def test_send_receive(in_node: NodeType, out_node: NodeType, sender_node: NodeType, receiver_node: NodeType):
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
    message: Message = Message()
    sender_node.send(node=in_node, messages=[message])
    receiver_node.receive(node=out_node)
    assert sender_node.last_message._get_id() == receiver_node.last_message._get_id()
