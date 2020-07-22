import pytest

from iqa.system.executor.docker.executor_docker import ExecutorDocker
from iqa.system.service.service import ServiceStatus
from iqa.system.service.service_docker import ServiceDocker


class TestServiceDocker:

    @pytest.fixture
    def service(self, docker_services) -> ServiceDocker:
        executor: ExecutorDocker = ExecutorDocker(
            container_name='sshd-container'
        )

        service: ServiceDocker = ServiceDocker(
            name='sshd-container',
            executor=executor
        )

        return service

    @pytest.mark.asyncio
    async def test_service_start(self, service: ServiceDocker) -> None:
        await service.start()
        assert service.status == ServiceStatus.RUNNING

    @pytest.mark.asyncio
    async def test_service_restart(self, service: ServiceDocker) -> None:
        await service.restart()
        assert service.status == ServiceStatus.RUNNING

    @pytest.mark.asyncio
    async def test_service_stop(self, service: ServiceDocker) -> None:
        await service.stop()
        assert service.status == ServiceStatus.STOPPED
