import pytest
import logging
logging.basicConfig(level=logging.DEBUG)

from iqa.instance.instance import Instance
from iqa.system.node.node_docker import NodeDocker
from iqa.system.executor.executor_container import ExecutorContainer


class TestInstanceNodeDocker:
    iqa_instance = Instance()

    @pytest.fixture
    def instance(self):
        return TestInstanceNodeDocker.iqa_instance

    @pytest.fixture
    def node(self, instance):

        executor = ExecutorContainer(
            name="Docker executor",
            container_name='sshd-iqa'
        )

        example_node = NodeDocker(hostname="sshd-iqa", executor=executor)
        instance.nodes.append(example_node)

        node: NodeDocker = instance.nodes[0]

        return node

    def test_ping(self, node):
        node_ping = node.ping()

        assert node_ping

    def test_get_ip(self, node):
        node_ip = node.get_ip()

        assert node_ip is not None
