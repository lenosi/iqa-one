def pytest_addoption(parser):
    """
    This particular suite requires that the router1 ip address is informed,
    as it is used internally in the related inventory files.

    :param parser:
    :return:
    """
    # Router 1 IP is a mandatory argument
    parser.addoption("--router1-ip", action="store", required=True, help="Openshift cluster IP where router is deployed")


def pytest_generate_tests(metafunc):
    """
    Iterate through tests with length parameter and make
    sure tests will be executed with 1024 increment.
    """
    if 'length' in metafunc.fixturenames:
        metafunc.parametrize("length", [x*1024 for x in [1, 5, 10]])
