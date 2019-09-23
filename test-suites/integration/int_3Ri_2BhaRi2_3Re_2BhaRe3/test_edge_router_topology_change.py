import logging

from iqa.components.abstract.component import ServiceStatus
from messaging_components.routers.dispatch.management import RouterQuery


class TestEdgeRouterNotChangingTopology:
    """
    Test that validates adding or removing an Edge router wont change the topology.
    """

    @classmethod
    def setup_class(cls):
        # Stores topology change date from each interior router
        cls.last_topology_change = {}

    def test_nodes_in_topology(self, router):
        """
        Validates that edge routers do not show any node when queried, and
        interior routers are showing other nodes.
        It also stores last topology change from each interior router and it
        will be used later, after edge routers are restarted.
        :param router:
        :return:
        """
        query = RouterQuery(router.node.get_ip(), router.port, router)

        # Get router mode
        router_info = query.router()[0]
        mode = router_info.mode

        # Query nodes in network
        nodes = query.node()

        # If edge, expect no nodes returned
        if mode == 'edge':
            assert not nodes
            return

        # Following applies just to interior
        assert nodes
        assert len(nodes) > 1

        # Loop through nodes and store lastTopoChange for current instance
        for node in nodes:
            if node.nextHop == '(self)':
                self.last_topology_change[router_info.name] = node.lastTopoChange
                logging.debug("Last topology change for: %s = %s" % (router_info.name, node.lastTopoChange))

    def test_restart_edge_routers(self, router_edge):
        """
        Restart all edge routers and ensure they have stopped and started.
        :param router_edge:
        :return:
        """
        router_edge.service.stop()
        assert router_edge.service.status() == ServiceStatus.STOPPED

        router_edge.service.start()
        assert router_edge.service.status() == ServiceStatus.RUNNING

    def test_topology_not_changed(self, router_interior):
        """
        Query all interior routers one more time and expect last topology change variable
        to return the same value and that the number of nodes in the network remains the same.
        :param router_interior:
        :return:
        """

        query = RouterQuery(router_interior.node.get_ip(),
                            router_interior.port,
                            router_interior)

        # Retrieving router info
        router_info = query.router()[0]

        # Must be set to False after loop is processed
        topology_changed = True
        nodes = query.node()

        for node in nodes:
            if node.nextHop != '(self)':
                continue

            topology_changed = self.last_topology_change[router_info.name] != node.lastTopoChange
            logging.debug("Last topology change for: %s = %s [before: %s]"
                          % (router_info.name, self.last_topology_change[router_info.name], node.lastTopoChange))

            break

        assert not topology_changed
        assert len(nodes) == len(self.last_topology_change.keys())
