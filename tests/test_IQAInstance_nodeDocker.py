import pytest

from iqa.instance.instance import IQAInstance
from iqa.system.node.node_docker import NodeDocker
from iqa.system.executor.executor_container import ExecutorContainer


class TestIQAInstanceNodeDocker:
    iqa_instance = IQAInstance()

    @pytest.fixture
    def instance(self):
        return TestIQAInstanceNodeDocker.iqa_instance

    @pytest.fixture
    def node(self, instance):

        executor = ExecutorContainer(
            name="Docker executor",
            container_name='iqa-example-node'
        )

        example_node = NodeDocker(hostname="iqa-example-node", executor=executor)
        instance.nodes.append(example_node)

        node: NodeDocker = instance.nodes[0]

        return node

    def test_ping(self, node):
        node_ping = node.ping()

        assert node_ping

    def test_get_ip(self, node):
        node_ip = node.get_ip()

        assert node_ip is not None
