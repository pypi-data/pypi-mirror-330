import pytest


@pytest.mark.parametrize(
    ("filters", "qsearch", "custom", "expected"),
    [
        ({}, None, None, []),
        ({}, "test qsearch", None, ["test qsearch"]),
        ({}, None, "test-custom", ["test custom"]),
        ({"MerchandisingTags": ["test-tag"]}, None, None, ["test-tag"]),
        (
            {"MerchandisingTags": ["test-tag", "test-other-tag"]},
            "test qsearch",
            "test-custom",
            ["test qsearch", "test custom", "test-tag", "test-other-tag"],
        ),
    ],
)
def test_get_keywords(filters, qsearch, custom, expected):
    from sponsored_ads_service.factories.tools.filter import get_keywords

    output = get_keywords(filters=filters, qsearch=qsearch, custom=custom)
    assert output == expected
