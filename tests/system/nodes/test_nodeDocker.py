import pytest
import logging
logging.basicConfig(level=logging.DEBUG)

from iqa.system.node.node_docker import NodeDocker
from iqa.system.executor.executor_container import ExecutorContainer


class TestNodeDocker:

    @pytest.fixture
    def node(self):

        executor = ExecutorContainer(
            name="Docker executor",
            container_name='sshd-iqa'
        )

        node = NodeDocker(hostname="sshd-iqa", executor=executor)

        return node

    def test_ping(self, node):
        node_ping = node.ping()

        assert node_ping

    def test_get_ip(self, node):
        node_ip = node.get_ip()

        assert node_ip is not None
