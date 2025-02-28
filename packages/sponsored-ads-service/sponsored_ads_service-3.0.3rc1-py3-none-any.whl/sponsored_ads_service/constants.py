from enum import StrEnum

from sponsored_ads_service.models.notices import ImageNotice, Notice, TextNotice


class NoticeKeys(StrEnum):
    SPONSORED = "sponsored"
    SPONSORED_PLID = "sponsored-plid"
    AGE_RESTRICTED = "age-restricted"
    SPONSORED_DEALS = "sponsored-deals"


def get_notices() -> list[Notice]:
    """
    A function to return a new list instance on each usage so that callers can modify
    the list freely.
    """
    return [
        TextNotice(
            key=NoticeKeys.SPONSORED,
            text="Sponsored",
            description="You're seeing this ad based on the product's relevance to your search query.",  # noqa: E501
        ),
        TextNotice(
            key=NoticeKeys.SPONSORED_PLID,
            text="Sponsored",
            description="You're seeing these ads based on its relevance to the product categories.",  # noqa: E501
        ),
        TextNotice(
            key=NoticeKeys.SPONSORED_DEALS,
            text="Sponsored",
            description="You're seeing these ads based on its relevance to the promotion.",
        ),
        ImageNotice(
            key=NoticeKeys.AGE_RESTRICTED,
            image_url="https://static.takealot.com/images/sponsored-ads/under-18-x2.png",
            alt_text="18+",
            description="This product is not for sale to persons under the age of 18.",
        ),
    ]
