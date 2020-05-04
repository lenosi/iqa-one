import pytest
import logging

from iqa.system.node.node import Node
from iqa.system.node.node_docker import NodeDocker
from iqa.system.executor.executor_container import ExecutorContainer


logging.basicConfig(level=logging.DEBUG)


class TestNodeDocker:

    @pytest.fixture
    def node(self, docker_services) -> Node:

        executor: ExecutorContainer = ExecutorContainer(
            name="Docker executor",
            container_name='sshd-container'
        )
        node: NodeDocker = NodeDocker(hostname="sshd-container", executor=executor)
        return node

    def test_ping(self, node) -> None:
        node_ping: bool = node.ping()

        assert node_ping

    def test_get_ip(self, node) -> None:
        node_ip: str = node.ip

        assert node_ip is not None
