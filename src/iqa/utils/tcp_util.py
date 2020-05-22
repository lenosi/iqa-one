"""
Provides utility classes and methods to deal with TCP communication.
"""
import asyncio
import logging
import socket
import time


def is_tcp_port_available(port, host) -> bool:
    """
    Returns True if a given port is accessibly on the specified host.
    :param port:
    :param host:
    :return:
    """
    test_port: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    try:
        test_port.connect((host, port))
        test_port.close()
        return True
    except OSError or ValueError:
        logging.getLogger(__name__).debug(
            '%s:%s is_tcp_port_available failed' % (host, port), exc_info=True
        )
        return False


async def wait_host_port(host, port, duration=5, delay=0.1):
    """Repeatedly try if a port on a host is open until duration seconds passed

    Args:
        host: host host address or hostname
        port: port number
        duration: Total duration in seconds to wait
        delay: delay in seconds between each try

    Returns:
        awaitable bool
    """

    tmax = time.time() + duration
    while time.time() < tmax:
        try:
            _reader, writer = await asyncio.wait_for(asyncio.open_connection(host, port), timeout=5)
            writer.close()
            await writer.wait_closed()
            return True
        except:
            if delay:
                await asyncio.sleep(delay)
    return False
