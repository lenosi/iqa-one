from messaging_components.routers.dispatch.dispatch import Dispatch as Router


def test_isinstance(router: Router):
    assert isinstance(router, Router)


def test_name(router: Router):
    assert router.name == 'Qpid Dispatch Router'


def test_status_started(router: Router):
    print(router.service.status)
#     assert router.service._status().get_ecode() == 0


def test_restart(router: Router):
    assert router.service.restart().get_ecode() == 0


def test_stop(router: Router):
    assert router.service.stop().get_ecode() == 0


def test_start(router: Router):
    assert router.service.start().get_ecode() == 0


def test_enable(router: Router):
    assert router.service.enable().get_ecode() == 0


def test_disable(router: Router):
    assert router.service.disable().get_ecode() == 0
