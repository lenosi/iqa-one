import time
from typing import Tuple
from iqa.components.routers.dispatch.dispatch import Dispatch
from iqa.components.routers.dispatch.management.query import RouterQuery
from iqa.instance.instance import Instance
from iqa.system.executor.execution import Execution
from iqa.utils.openshift_util import OpenShiftUtil

MESH_SIZE: int = 3


def test_scale_up_router(router_cluster: Tuple[Dispatch, str, str]):
    """
    Executes "oc" command to scale up the number of PODs according to value defined in MESH_SIZE constant.
    It also uses 'amq-interconnect' as the deployment config name (standard in official templates).

    Test passes if command is executed without errors.
    Note: the oc command expects that current session is logged to Openshift cluster (you can do it manually,
          but it will be also done through the CI job).
    :param router_cluster:
    :return:
    """

    router: Dispatch = router_cluster[0]
    cluster: str = router_cluster[1]
    token: str = router_cluster[2]

    # OCP Instance
    ocp: OpenShiftUtil = OpenShiftUtil(router.node.executor, 'https://%s:8443' % cluster, token)

    execution: Execution = ocp.scale(MESH_SIZE, 'amq-interconnect')
    assert execution.completed_successfully()


def test_router_mesh_after_scale_up(router_cluster: Tuple[Dispatch, str, str], iqa: Instance):
    """
    Queries Router for all Node Entities available in the topology.
    It expects the number of nodes matches number of PODs (mesh is correctly formed).
    :param router_cluster:
    :return:
    """
    router: Dispatch = router_cluster[0]
    validate_mesh_size(router, MESH_SIZE * len(iqa.get_routers()))


def validate_mesh_size(router: Dispatch, new_size: int):
    """
    Asserts that router topology size matches "new_size" value.
    :param router:
    :param new_size:
    :return:
    """
    time.sleep(90)
    query: RouterQuery = RouterQuery(host=router.node.ip, port=router.port, router=router)
    node_list: list = query.node()
    assert len(node_list) == new_size
