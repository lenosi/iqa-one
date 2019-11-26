"""
Simple example that demonstrates how to use IQA abstract and tools
to handle a Broker component.
"""
import sys
import time

# Displaying all queues
from iqa.system.service.service import ServiceStatus
from iqa.abstract.server.broker import Broker
from iqa.components.abstract.server import ServerComponent
from iqa.utils.tcp_util import TcpUtil
from iqa.instance.instance import Instance

DELAY: int = 10
MAX_ATTEMPTS: int = 3


def query_queues(broker) -> None:
    """
    List all queues found on given broker instance and its message count
    :param broker:
    :return:
    """
    print("  -> List of queues on %s:" % broker.node.hostname)
    for queue in broker.queues():
        print("     - name: %-40s | message count: %s" % (queue.fqqn, queue.message_count))


# Inventory file to use
inventory: str = sys.argv[1] if len(sys.argv) > 1 else 'inventory_docker.yml'

# Message explaining what this sample does
intro_message: str = """
This sample will iterate through all the 'broker' abstract defined at
the '%s' inventory file and it will then:
- Display the broker node hostname and its current status (if able to
  communicate with it)
- Attempt to start the broker component if it is not running (using a
  valid system service or a docker container)
  Note: You can stop the broker component and validate if it gets started
- Iterate through all queues and displaying its FQQN and the message count

""" % inventory
print(intro_message)

# Loading the instance
print("Loading IQAInstance using inventory file: %s" % inventory)
iqa: Instance = Instance(inventory)

# Iterating through brokers
for broker in iqa.brokers:  # type: (ServerComponent, Broker)

    # List broker node hostname and its status
    print("* Broker: %s - Status: %s" % (broker.node.hostname, broker.service.status().name))

    # If broker "service" is reported as not running, try starting it
    if broker.service.status() != ServiceStatus.RUNNING:
        print("  -> starting service: %s" % broker.service.name)
        broker.service.start()

        # Wait till broker web port is available
        for attempt in range(MAX_ATTEMPTS):
            if attempt == MAX_ATTEMPTS-1:
                print("     broker is not reachable after %d attempts" % MAX_ATTEMPTS)

            if TcpUtil.is_tcp_port_available(broker.web_port, host=broker.node.get_ip()):
                break

            time.sleep(DELAY)

        print("     new status: %s" % broker.service.status().name)

    # If broker is running, then retrieve all queues and message count
    if broker.service.status() == ServiceStatus.RUNNING:
        query_queues(broker)
