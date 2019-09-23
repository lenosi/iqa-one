"""
Simple example that demonstrates how to use IQA abstract and tools
to handle a Broker component.
"""
import sys
import logging



# Displaying all queues
from iqa.broker.abstract_broker_cluster import AbstractBrokerCluster
from iqa.core.instance import IQAInstance
from iqa.system.service.service import ServiceStatus

DELAY = 10
MAX_ATTEMPTS = 3


def query_queues(broker):
    """
    List all queues found on given broker instance and its message count
    :param broker:
    :return:
    """
    print("  -> List of queues on %s:" % broker.node.hostname)
    for queue in broker.queues():
        print("     - name: %-40s | message count: %s" % (queue.fqqn, queue.message_count))

logging.basicConfig(level=logging.INFO)

# Inventory file to use
inventory = sys.argv[1] if len(sys.argv) > 1 else 'inventory_docker.yml'

# Message explaining what this sample does
intro_message = """
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
iqa = IQAInstance(inventory)

# # Iterating through brokers
# for virtual_comp in iqa.get_virtual_components():
#     print("==========\n", virtual_comp.get_components())
#
#     sys.exit(0)

for cluster in iqa.broker_clusters:  # type: AbstractBrokerCluster

    print(cluster.cluster_members)
    print(cluster.node)
    print(cluster.service)
    for broker in cluster.get_brokers():
        print(broker)
        print("HA:", broker.ha_member)
        print("Cluster:", broker.cluster_member)
        print()

    # List broker node hostname and its status
    print("* Broker: %s - Status: %s" % (cluster.node.hostname, cluster.service.status().name))

    # If broker "service" is reported as not running, try starting it
    if cluster.service.status() != ServiceStatus.RUNNING:
        print("  -> starting service: %s" % cluster.service.name)
        cluster.service.start(wait_for_messaging=True)

        print("     new status: %s" % cluster.service.status().name)

    # query_queues(broker)
    # broker.service.stop()
    # broker.service.status()
    # broker.service.start(wait_for_messaging=True)
    # broker.service.status()
    #
    # broker.service.restart(wait_for_messaging=True)

    # If broker is running, then retrieve all queues and message count
    if cluster.service.status() == ServiceStatus.RUNNING:
        for broker in cluster.get_brokers():
            query_queues(broker)
