from sponsored_ads_service.constants import NoticeKeys, get_notices
from sponsored_ads_service.models.notices import ImageNotice, TextNotice


def test_get_notices():
    notices = get_notices()

    assert isinstance(notices, list)

    assert len(notices) == 4

    assert isinstance(notices[0], TextNotice)
    assert notices[0].key == NoticeKeys.SPONSORED
    assert notices[0].text == "Sponsored"
    assert "relevance to your search query" in notices[0].description

    assert isinstance(notices[1], TextNotice)
    assert notices[1].key == NoticeKeys.SPONSORED_PLID
    assert notices[1].text == "Sponsored"
    assert "relevance to the product categories" in notices[1].description

    assert isinstance(notices[2], TextNotice)
    assert notices[2].key == NoticeKeys.SPONSORED_DEALS
    assert notices[2].text == "Sponsored"
    assert "relevance to the promotion" in notices[2].description

    assert isinstance(notices[3], ImageNotice)
    assert notices[3].key == NoticeKeys.AGE_RESTRICTED
    assert (
        notices[3].image_url == "https://static.takealot.com/images/sponsored-ads/under-18-x2.png"
    )
    assert notices[3].alt_text == "18+"
    assert "not for sale to persons under the age of 18" in notices[3].description

    assert get_notices() is not notices
