"""
Ansible Node implementation of Node Interface.
"""

import logging

from docker.errors import APIError, NotFound
from docker.models.containers import Container

from iqa.system.executor import ExecutorContainer
from iqa.system.node.node import Node
from iqa.utils.docker_util import DockerUtil

logger = logging.getLogger()
docker_util: DockerUtil = DockerUtil()


class NodeDocker(Node):
    """Docker implementation for Node interface."""

    def __init__(
            self, hostname: str,
            executor: ExecutorContainer,
            docker_host: str = '',
            docker_network: str = '',
            ip: str = ''
    ) -> None:

        logger.info('Initialization of NodeDocker: %s' % hostname)
        self.hostname = hostname
        self.docker_network: str = docker_network
        self.container = self._get_container(docker_host=docker_host)
        super(NodeDocker, self).__init__(hostname, executor, ip)

    def ping(self) -> bool:
        """Send ping to Docker node"""
        try:
            return self.container.attrs['State']['Running']
        except Exception or APIError or NotFound:
            logger.info(
                'Unable to get container status for: %s' % self.executor.container_name
            )
            return False

    def _get_container(self, docker_host: str = '') -> Container:
        """Get Container instance"""
        logger.debug('Retrieving %s container\'s ip of %s docker host.' % (self.hostname, self.docker_network))
        container = DockerUtil.get_container(
            name=self.hostname,
            docker_host=docker_host
        )
        return container

    def _get_ip(self) -> None:
        """Get ip of Docker node"""
        logger.debug('Retrieving %s container\'s ip for network: %s' % (self.hostname, self.docker_network))
        self.ip: str = docker_util.get_container_ip(
            container=self.container,
            network_name=self.docker_network
        )

