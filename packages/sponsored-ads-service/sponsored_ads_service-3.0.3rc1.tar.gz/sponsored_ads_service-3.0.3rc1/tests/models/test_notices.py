import pytest

from sponsored_ads_service.models.notices import ImageNotice, TextNotice
from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb

pytestmark = pytest.mark.models


def test_text_notice_to_pb():
    model = TextNotice(key="key", text="text", description="desc")
    expected = pb.Notice(text_notice=pb.TextNotice(key="key", text="text", description="desc"))
    assert model.to_pb() == expected


def test_image_notice_to_pb():
    model = ImageNotice(
        key="key",
        image_url="https://media.takealot.com",
        alt_text="text",
        description="desc",
    )
    expected = pb.Notice(
        image_notice=pb.ImageNotice(
            key="key",
            image_url="https://media.takealot.com",
            alt_text="text",
            description="desc",
        )
    )
    assert model.to_pb() == expected
