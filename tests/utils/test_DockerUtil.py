import pytest
import logging

from docker.models.containers import Container
from iqa.utils.docker_util import get_container, get_container_ip

logging.basicConfig(level=logging.DEBUG)


class TestInstanceDockerUtil:
    @pytest.fixture
    def container(self, docker_services) -> Container:
        return get_container(name='sshd-container')

    def test_get_ip(self, container) -> None:
        get_container_ip(container)
