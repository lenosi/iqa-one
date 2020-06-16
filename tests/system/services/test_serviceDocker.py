import pytest

from iqa.system.executor import ExecutionBase
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

    @pytest.mark.asyncio
    async def test_service_start(self, service: ServiceDocker) -> None:
        start: ExecutionBase = await service.start()
        await start.wait()
        assert service.status() == ServiceStatus.RUNNING

    @pytest.mark.asyncio
    async def test_service_restart(self, service: ServiceDocker) -> None:
        restart: ExecutionBase = await service.restart()
        await restart.wait()
        assert service.status() == ServiceStatus.RUNNING

    @pytest.mark.asyncio
    async def test_service_stop(self, service: ServiceDocker) -> None:
        stop: ExecutionBase = await service.stop()
        await stop.wait()
        assert service.status() == ServiceStatus.STOPPED
