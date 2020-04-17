"""
Simple example that demonstrates how to use IQA abstract and tools
to handle a Router component.
"""
import sys


# Displaying all connections
from iqa.components.routers.dispatch.dispatch import Dispatch
from iqa.components.routers.dispatch.management.query import RouterQuery
from iqa.instance.instance import Instance
from iqa.components.abstract.server.server_component import ServerComponent
from iqa.abstract.server.router import Router
from iqa.system.service.service import ServiceStatus


def query_connections(router: Dispatch) -> None:
    """
    Queries management API using given Router instance
    for existing connections.
    :param router:
    :return:
    """
    print("  -> List of connections on %s:" % router.node.hostname)
    query: RouterQuery = RouterQuery(host=router.node.get_ip())

    # The query below returns a namedtuple representing a Connection entity
    for conn in query.connection():
        print("     - %s" % conn.name)


# Inventory file to use
inventory: str = sys.argv[1] if len(sys.argv) > 1 else 'inventory_local.yml'

# Message explaining what this sample does
intro_message: str = """
This sample will iterate through all the 'router' abstract defined at
the '%s' inventory file and it will then:
- Display the router node hostname and its current status (if able to
  communicate with it)
- Attempt to start the router component if it is not running (using a
  valid system service or a docker container)
  Note: You can stop the router component and validate if it gets started
- Iterate through all 'connection' entities and displaying its 'name' property

""" % inventory
print(intro_message)

# Loading the instance
print("Loading IQAInstance using inventory file: %s" % inventory)
iqa: Instance = Instance(inventory)

# Listing all routers in inventory
print("\nList of Router abstract parsed from inventory")
for router in iqa.routers:  # type: (ServerComponent, Router)

    # List router node hostname and its status
    print("* Router: %s - Status: %s" % (router.node.hostname, router.service.status().name))

    # If router "service" is reported as not running, try starting it
    if router.service.status() != ServiceStatus.RUNNING:
        print("  -> starting service: %s" % router.service.name)
        router.service.start()
        print("     new status: %s" % router.service.status().name)

    # If router is running, then query management API
    if router.service.status() == ServiceStatus.RUNNING:
        query_connections(router)
