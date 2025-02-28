"""
Tooling for Filters
"""

from sponsored_ads_service.models.request_response import Filters


def get_brands(filters: Filters) -> list[str]:
    """Get the list of applied brands from given `filters`"""

    return filters.get("Brand", [])


def get_keywords(
    filters: Filters,
    qsearch: str | None = None,
    custom: str | None = None,
) -> list[str]:
    """Get the list of applied keywords derived from `filters`, `qsearch` or `custom`"""

    keywords: list[str] = []
    if qsearch:
        keywords.append(qsearch)
    if custom:
        keywords.append(custom.replace("-", " ").replace("_", " "))
    if filters.get("MerchandisingTags"):
        keywords.extend(filters["MerchandisingTags"])
    return keywords
