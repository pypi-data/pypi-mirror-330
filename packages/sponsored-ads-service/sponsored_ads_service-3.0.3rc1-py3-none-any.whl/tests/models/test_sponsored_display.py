import pytest

from sponsored_ads_service.constants import NoticeKeys
from sponsored_ads_service.models.sponsored_display import (
    AdType,
    SponsoredDisplay,
    SponsoredDisplayCreative,
)
from sponsored_ads_service.models.sponsored_product import (
    OnlineSalesAdInfo,
    SponsoredProduct,
)

pytestmark = pytest.mark.models


@pytest.mark.parametrize(
    ("model", "expected"),
    [
        (
            SponsoredDisplay(
                ad_type=AdType.BANNER,
                client_id="123345",
                ad_unit="pdp-slot-1",
                uclid="foo|bar",
                creative=SponsoredDisplayCreative.SINGLE_PRODUCT,
                destination_url="https://www.foo.bar",
                products=[
                    SponsoredProduct(
                        lineage_document={"productline": {"id": 1001}},
                        sponsored_ad=OnlineSalesAdInfo(
                            uclid="foo|bar",
                            client_id="123345",
                            cli_ubid="123-567",
                            seller_id="M16",
                            text_notices=[NoticeKeys.SPONSORED],
                            image_notices=[NoticeKeys.AGE_RESTRICTED],
                        ),
                    )
                ],
                background={},
            ),
            {
                "ad_type": "banner",
                "client_id": "123345",
                "ad_unit": "pdp-slot-1",
                "uclid": "foo|bar",
                "creative": "single-product",
                "destination_url": "https://www.foo.bar",
                "products": [
                    {
                        "lineage_document": {"productline": {"id": 1001}},
                        "sponsored_ad": {
                            "uclid": "foo|bar",
                            "client_id": "123345",
                            "cli_ubid": "123-567",
                            "seller_id": "M16",
                            "text_notices": [NoticeKeys.SPONSORED],
                            "image_notices": [NoticeKeys.AGE_RESTRICTED],
                        },
                    }
                ],
                "background": {},
            },
        ),
    ],
)
def test_to_dict(model, expected):
    assert model.to_dict() == expected


def test_sponsored_display_creative_missing():
    v = SponsoredDisplayCreative("qqqqqqq")
    assert v == SponsoredDisplayCreative.UNKNOWN
