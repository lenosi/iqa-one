from iqa.abstract import Listener
from iqa.components import protocols
from iqa.components.abstract.component import Component
from iqa.components.clients.external import ClientCommand
from iqa.components.clients.external import ClientExternal


class ClientJava(ClientExternal, Component):
    """Java Qpid JMS client (base abstract class)."""

    def _new_command(self, stdout: bool = False, stderr: bool = False, daemon: bool = False, timeout: int = 0,
                     encoding: str = "utf-8") -> ClientCommand:
        pass

    def _set_url(self, url: str):
        pass

    def set_auth_mechs(self, mechs: str):
        pass

    def set_ssl_auth(self, pem_file: str = None, key_file: str = None, keystore: str = None, keystore_pass: str = None,
                     keystore_alias: str = None):
        pass

    def set_endpoint(self, listener: Listener):
        pass

    def connect(self):
        pass

    supported_protocols = [protocols.Amqp10()]
    implementation = 'java'
    version = '1.0.1'

    def __init__(self, name: str, node, **kwargs):
        super(ClientJava, self).__init__(name, node, **kwargs)
