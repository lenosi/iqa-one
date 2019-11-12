import pytest

from iqa.instance.instance import Instance
from iqa.system.node import Node
from iqa.system.node.node_docker import NodeDocker
from iqa.system.executor.executor_container import ExecutorContainer


class TestInstanceNodeDocker:
    iqa_instance: Instance = Instance()

    @pytest.fixture
    def instance(self) -> Instance:
        return TestInstanceNodeDocker.iqa_instance

    @pytest.fixture
    def node(self, instance: Instance) -> Node:

        executor: ExecutorContainer = ExecutorContainer(
            name="Docker executor",
            container_name='sshd-iqa'
        )

        example_node: NodeDocker = NodeDocker(hostname="sshd-iqa", executor=executor)
        instance.nodes.append(example_node)

        node: Node = instance.nodes[0]

        return node

    def test_ping(self, node: NodeDocker) -> None:
        node_ping: bool = node.ping()

        assert node_ping

    def test_get_ip(self, node: NodeDocker) -> None:
        node_ip: str = node.get_ip()

        assert node_ip is not None
