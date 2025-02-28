from sponsored_ads_service.constants import NoticeKeys
from sponsored_ads_service.models.sponsored_product import AdInfo, SponsoredProduct


def test_sponsored_product_to_dict():
    model = SponsoredProduct(
        lineage_document={"productline": {"id": 1001}},
        sponsored_ad=AdInfo(text_notices=[NoticeKeys.SPONSORED], image_notices=[]),
    )
    output = model.to_dict()
    assert output == {
        "lineage_document": {"productline": {"id": 1001}},
        "sponsored_ad": {"text_notices": ["sponsored"], "image_notices": []},
    }
