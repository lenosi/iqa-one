"""
Ansible Node implementation of Node Interface.
"""

import logging
from typing import Optional

from docker.models.containers import Container
from docker.errors import APIError, NotFound

from iqa.system.executor import ExecutorContainer
from iqa.system.node import Node
from iqa.utils.docker_util import DockerUtil


class NodeDocker(Node):
    """Ansible implementation for Node interface."""

    def __init__(self, hostname: str, executor: ExecutorContainer,
                 ip: str = None) -> None:
        super(NodeDocker, self).__init__(hostname, executor, ip)
        self.docker_util: DockerUtil = DockerUtil()
        self.ip: Optional[str] = ip
        self.executor: ExecutorContainer = executor
        logging.getLogger().info('Initialization of NodeDocker: %s' %
                                 self.hostname)

    def ping(self) -> bool:
        """Send ping to Docker node"""
        try:
            container: Container = self.docker_util.get_container(
                self.executor.container_name)
            return container.attrs['State']['Running']
        except APIError or NotFound:
            logging.info("Unable to get container status for: %s" %
                         self.executor.container_name)
            return False

    def get_ip(self) -> Optional[str]:
        """Get ip of Docker node"""
        if self.ip is not None:
            return self.ip

        try:
            docker_network = self.executor.docker_network or 'bridge'
            logging.debug("Retrieving container's ip for network: %s" %
                          docker_network)
            ip: str = self.docker_util.get_container_ip(
                self.executor.container_name, docker_network)
        except:
            logging.debug("Unable to determine IP for container: %s" %
                          self.executor.container_name)
            # TODO fix this
            return None

        logging.debug("Container [%s] - IP [%s]" %
                      (self.executor.container_name, ip))
        self.ip = ip
        return ip
