import pytest

from sponsored_ads_service.models.positioning import Breakpoints, Positions
from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb


@pytest.fixture
def positions():
    return Positions(
        apps=Breakpoints(sm=[0, 1, 2, 3, 4], medium=[0, 1, 2, 3, 4]),
        web=Breakpoints(sm=[0, 1, 2, 3, 4], medium=[0, 1, 2, 3, 4]),
    )


@pytest.fixture
def positions_pb():
    return pb.Positions(
        apps=pb.Breakpoints(sm=[0, 1, 2, 3, 4], medium=[0, 1, 2, 3, 4]),
        web=pb.Breakpoints(sm=[0, 1, 2, 3, 4], medium=[0, 1, 2, 3, 4]),
    )
