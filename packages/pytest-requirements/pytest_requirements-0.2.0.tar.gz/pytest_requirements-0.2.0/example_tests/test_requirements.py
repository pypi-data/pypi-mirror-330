import pytest


@pytest.mark.verifies_requirement("B-DPPS-0123")
def test_single_requirement():
    pass


@pytest.mark.verifies_requirement("B-DPPS-0123")
@pytest.mark.verifies_requirement("B-DPPS-0124")
@pytest.mark.verifies_requirement("B-DPPS-0125")
def test_multiple_requirements():
    pass


@pytest.mark.verifies_usecase("UC-130-1.2")
def test_usecase():
    pass


@pytest.mark.verifies_usecase("UC-130-1.2.1")
@pytest.mark.verifies_usecase("UC-130-1.2.2")
def test_multiple_usecases():
    pass


@pytest.mark.verifies_usecase("UC-130-1.2.1")
@pytest.mark.verifies_usecase("UC-130-1.2.2")
@pytest.mark.verifies_requirement("B-DPPS-0123")
def test_mixed():
    pass


@pytest.fixture
def foo_fixture(request):
    request.applymarker(pytest.mark.verifies_usecase("UC-130-1.2.1"))
    request.applymarker(pytest.mark.verifies_requirement("B-DPPS-0123"))
    return "foo"


def test_fixture_mark(foo_fixture):
    pass
