import pytest

from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.service.service import ServiceStatus
from iqa.system.service.service_docker import ServiceDocker


class TestServiceDocker:

    @pytest.fixture
    def service(self, docker_services) -> ServiceDocker:
        executor: ExecutorDocker = ExecutorDocker(
            name='Docker executor',
            container_name='sshd-container'
        )

        service: ServiceDocker = ServiceDocker(
            name='sshd-container',
            executor=executor
        )

        return service

    def test_service_start(self, service: ServiceDocker) -> None:
        service.start()
        assert service.status() == ServiceStatus.RUNNING

    def test_service_restart(self, service: ServiceDocker) -> None:
        service.restart()
        assert service.status() == ServiceStatus.RUNNING

    def test_service_stop(self, service: ServiceDocker) -> None:
        service.stop()
        assert service.status() == ServiceStatus.STOPPED
