import pytest

from sponsored_ads_service.errors import BadRequestError, SponsoredDisplayMissingBannerError
from sponsored_ads_service.sponsored_ads import models as dto


@pytest.fixture
def factory(config):
    from sponsored_ads_service.onlinesales.creatives import CreativeFactory

    return CreativeFactory(config)


@pytest.fixture
def factory_pre_rollout(mocker, config):
    from sponsored_ads_service.onlinesales.creatives import CreativeFactory

    mocker.patch.object(config, "get_rollout_flag_search_banner_remap", return_value=False)
    return CreativeFactory(config)


def test_from_request_creatives_maps_correctly(factory):
    from sponsored_ads_service.onlinesales.models import Creative

    banner = factory.from_request_creatives([dto.Creative.BANNER], location=dto.Location.SEARCH)
    assert banner == [Creative.SEARCH_BANNER_TOP]


def test_from_request_creatives_without_search_banner_remap(factory_pre_rollout):
    from sponsored_ads_service.onlinesales.models import Creative

    banner = factory_pre_rollout.from_request_creatives(
        [dto.Creative.BANNER], location=dto.Location.SEARCH
    )
    assert banner == [Creative.SEARCH_BANNER]


def test_from_request_creatives_invalid_combination(factory):
    with pytest.raises(BadRequestError):
        factory.from_request_creatives([dto.Creative.SINGLE_PRODUCT], location=dto.Location.HOME)


def test_from_onlinesales_creative(factory):
    from sponsored_ads_service.onlinesales.models import Creative

    banner = factory.from_onlinesales_creative(Creative.SINGLE_PRODUCT)
    assert banner == dto.Creative.SINGLE_PRODUCT


def test_from_onlinesales_creative_returns_unspecified_for_unknown_creative(factory):
    assert factory.from_onlinesales_creative("nonexistent") == dto.Creative.UNSPECIFIED


def test_build_images(factory):
    from sponsored_ads_service.onlinesales.models import Creative

    onlinesales_images = {
        "bg_img_src_300x50": "image1",
        "bg_img_src_728x90": "image2",
        "bg_img_src_1292x120": "image3",
    }
    result = factory.build_images(Creative.SEARCH_BANNER, onlinesales_images)
    assert result == dto.Background(sm="image1", md="image2", lg="image3")


def test_build_images_raises_missing_image(factory):
    from sponsored_ads_service.onlinesales.models import Creative

    onlinesales_images = {
        "bg_img_src_300x50": "image1",
        "bg_img_src_728x90": "image2",
    }
    with pytest.raises(SponsoredDisplayMissingBannerError):
        factory.build_images(Creative.SEARCH_BANNER, onlinesales_images)


def test_unknown_image(factory):
    from sponsored_ads_service.onlinesales.models import Creative

    onlinesales_images = {
        "bg_img_src_300x50": "image1",
        "bg_img_src_728x90": "image2",
        "bg_img_src_1292x120": "image3",
    }
    result = factory.build_images(Creative.UNKNOWN, onlinesales_images)
    assert result is None
