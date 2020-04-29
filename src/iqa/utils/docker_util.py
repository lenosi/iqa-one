
"""
Utility classes to retrieve information from local docker environment.
"""
import logging
import os

import docker
from docker.errors import APIError, NotFound
from docker.models.containers import Container

logger: logging.Logger = logging.getLogger(__name__)

_env: dict = os.environ.copy()


class DockerUtil:
    """
    Utility class to interact with local docker environment, providing
    basic information on images and containers.
    """

    CONTAINER_STATUS_RUNNING: str = 'running'
    CONTAINER_STATUS_EXITED: str = 'exited'
    client = docker.from_env(environment=_env)

    @staticmethod
    def get_client(docker_host: str = ''):
        if docker_host:
            _env['DOCKER_HOST'] = docker_host
        return docker.from_env(environment=_env)

    @staticmethod
    def get_container(name: str, docker_host: str = '') -> Container:
        """
        Returns the container instance for the given name.
        A docker.errors.NotFound exception is raised in case the given
        container does not exist.
        :param docker_host:
        :param name:
        :return:
        """
        client = DockerUtil.get_client(docker_host=docker_host)
        return client.containers.get(name)

    @staticmethod
    def get_container_ip(container: Container, network_name='') -> str:
        """
        Returns the IPAddress assigned to the given container name (on the given network).
        :param container:
        :param network_name:
        :return:
        """
        try:
            if network_name:
                ip_addr: str = container.attrs['NetworkSettings']['Networks'][network_name]['IPAddress']
            else:
                ip_addr: str = list(container.attrs['NetworkSettings']['Networks'].values())[0]['IPAddress']

            logger.debug('Container [%s] - IP [%s]' % (container.name, ip_addr))

        except Exception or APIError or NotFound:
            logger.debug(
                'Unable to determine IP for container: %s'
                % container.name
            )
            ip_addr = ''

        return ip_addr

    @staticmethod
    def stop_container(container: Container) -> None:
        """
        Stops a given container based on its name or id.
        :param container:
        :return:
        """
        container.stop()

    @staticmethod
    def start_container(container: Container) -> None:
        """
        Starts the given container based on its name or id.
        :param container:
        :return:
        """
        container.start()
