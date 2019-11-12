import pytest

from iqa.system.node.node_docker import NodeDocker
from iqa.system.executor.executor_container import ExecutorContainer


class TestNodeDocker:

    @pytest.fixture
    def node(self) -> NodeDocker:

        executor: ExecutorContainer = ExecutorContainer(
            name="Docker executor",
            container_name='sshd-iqa'
        )

        node: NodeDocker = NodeDocker(hostname="sshd-iqa", executor=executor)

        return node

    def test_ping(self, node) -> None:
        node_ping: bool = node.ping()

        assert node_ping

    def test_get_ip(self, node) -> None:
        node_ip: str = node.get_ip()

        assert node_ip is not None
