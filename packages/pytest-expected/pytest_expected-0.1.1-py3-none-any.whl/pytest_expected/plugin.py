import inspect
import pickle
import sys
import pytest


def pytest_addoption(parser):
    group = parser.getgroup("expected")
    group.addoption(
        "--record",
        action="store_true",
        default=False,
        help="Record comparisons with the `expected` fixture.",
    )


class ExpectedError(Exception):
    pass


UNSET = object()


class Expected:
    """
    A per-function...ohh
    """
    def __init__(self, *, request, root, record=False):
        self.record = record
        self.nodeid = request.node.nodeid
        self.path = root / ".expected" / self.nodeid
        self.n = 0
        # request.node.nodeid  # <- use this for storage?
        self.values = []
        if not record:
            for file in sorted(self.path.glob("*"), key=lambda p: int(p.name)):
                with file.open("rb") as f:
                    self.values.append(pickle.load(f))
            self.values = iter(self.values)
        self.last_value = UNSET

    def __eq__(self, other):
        # f = sys._getframe()
        # while f.f_code != self.request.function.__code__:
        #     f = f.f_back
        if self.record:
            self.values.append(other)
            return True
        try:
            value = next(self.values)
            self.last_value = value
            return value == other
        except StopIteration:
            raise ExpectedError(f"Need to --record expected value for {self.nodeid}") from None

    def __repr__(self):
        if self.last_value is not UNSET:
            return repr(self.last_value)
        return "<Expected>"

    def finalize(self):
        if self.record:
            self.path.mkdir(exist_ok=True, parents=True)
            for i, value in enumerate(self.values):
                with (self.path / str(i)).open("wb") as f:
                    pickle.dump(value, f)


@pytest.fixture
def expected(pytestconfig, request):
    # print(request.node)
    # print(request.path)
    e = Expected(
        record=pytestconfig.getoption("record"),
        root=pytestconfig.rootpath,
        request=request,
    )
    yield e
    e.finalize()
