import pytest
import logging

from iqa.utils.docker_util import DockerUtil
from docker.models.containers import Container
from iqa.instance.instance import Instance
from iqa.system.node.node import Node
from iqa.system.node.node_docker import NodeDocker
from iqa.system.executor.executor_container import ExecutorContainer

logging.basicConfig(level=logging.DEBUG)


class TestInstanceDockerUtil:
    @pytest.fixture
    def container(self) -> Container:
        return DockerUtil().get_container(name='sshd-container')

    def test_get_ip(self, container) -> None:
        DockerUtil().get_container_ip(container)


class TestInstanceNodeDocker:
    iqa_instance: Instance = Instance()

    @pytest.fixture
    def instance(self) -> Instance:
        return TestInstanceNodeDocker.iqa_instance

    @pytest.fixture
    def node(self, instance: Instance) -> Node:

        executor: ExecutorContainer = ExecutorContainer(
            name="Docker executor",
            container_name='sshd-container'
        )

        example_node: NodeDocker = NodeDocker(hostname="sshd-container", executor=executor)
        instance.nodes.append(example_node)

        node: Node = instance.nodes[0]

        return node

    def test_ping(self, node: NodeDocker) -> None:
        assert node.ping()

    def test_get_ip(self, node: NodeDocker) -> None:
        assert node.ip is not None
