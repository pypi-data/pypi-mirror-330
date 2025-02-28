import pytest

from sponsored_ads_service.protobuf import sponsored_ads_service_pb2 as pb
from sponsored_ads_service.sponsored_ads.models import (
    Background,
    Banner,
    Creative,
    DisplayAd,
    DisplayAdsRequest,
    Location,
    MultiProduct,
    Platform,
    ProductAd,
    ProductAdsRequest,
    ProductAdsResponse,
    SingleProduct,
    Targeting,
    TrackingInfo,
)


@pytest.fixture
def pb_display_ads_request():
    return pb.DisplayAdsRequest(
        location=pb.LOCATION_SEARCH,
        uuid="1234",
        platform=pb.PLATFORM_WEB,
        creatives=[pb.CREATIVE_BANNER],
        ad_units=["unit1", "unit2"],
        targeting=pb.Targeting(
            qsearch="query",
            filters={"filter1": pb.FilterValues(values=["value1", "value2"])},
            plids=[1, 2, 3],
            cms_page_slug="slug",
        ),
        limit=10,
    )


@pytest.fixture
def pb_display_ads_request_no_filters():
    return pb.DisplayAdsRequest(
        location=pb.LOCATION_SEARCH,
        uuid="1234",
        platform=pb.PLATFORM_WEB,
        creatives=[pb.CREATIVE_BANNER],
        ad_units=["unit1", "unit2"],
        targeting=pb.Targeting(
            qsearch="query",
            plids=[1, 2, 3],
            cms_page_slug="slug",
        ),
        limit=10,
    )


@pytest.fixture
def pb_product_ads_request():
    return pb.ProductAdsRequest(
        location=pb.LOCATION_SEARCH,
        uuid="1234",
        platform=pb.PLATFORM_IOS,
        targeting=pb.Targeting(
            qsearch="query",
            filters={"filter1": pb.FilterValues(values=["value1", "value2"])},
            plids=[1, 2, 3, 4, 5, 6],
            cms_page_slug=None,
        ),
        limit=10,
    )


def test_product_ads_request_from_pb(pb_product_ads_request):
    result = ProductAdsRequest.from_pb(pb_product_ads_request)

    assert result == ProductAdsRequest(
        location=Location.SEARCH,
        uuid="1234",
        platform=Platform.IOS,
        targeting=Targeting(
            qsearch="query",
            filters={"filter1": ["value1", "value2"]},
            plids=[1, 2, 3, 4, 5, 6],
            cms_page_slug="",
        ),
        limit=10,
    )


def test_product_ads_response_to_pb():
    product_ads_response = ProductAdsResponse(
        products=[
            ProductAd(
                productline_id=1001,
                variant_id=2001,
                offer_id=3001,
                tracking_info=TrackingInfo(
                    uclid="uclid_1", uuid="uuid_1", cli_ubid="cli_ubid_1", seller_id="seller_id_1"
                ),
            ),
            ProductAd(
                productline_id=1002,
                variant_id=2002,
                offer_id=3002,
                tracking_info=TrackingInfo(
                    uclid="uclid_2", uuid="uuid_2", cli_ubid="cli_ubid_2", seller_id="seller_id_2"
                ),
            ),
        ]
    )
    result = product_ads_response.to_pb()
    assert len(result.products) == 2
    assert result == pb.ProductAdsResponse(
        products=[
            pb.ProductAd(
                productline_id=1001,
                variant_id=2001,
                offer_id=3001,
                tracking=pb.TrackingInfo(
                    uclid="uclid_1", uuid="uuid_1", cli_ubid="cli_ubid_1", seller_id="seller_id_1"
                ),
            ),
            pb.ProductAd(
                productline_id=1002,
                variant_id=2002,
                offer_id=3002,
                tracking=pb.TrackingInfo(
                    uclid="uclid_2", uuid="uuid_2", cli_ubid="cli_ubid_2", seller_id="seller_id_2"
                ),
            ),
        ]
    )


def test_display_ads_request_from_pb(pb_display_ads_request):
    result = DisplayAdsRequest.from_pb(pb_display_ads_request)
    assert result.location == Location.SEARCH
    assert result.uuid == "1234"
    assert result.platform == Platform.WEB
    assert result.creatives == [Creative.BANNER]
    assert result.ad_units == ["unit1", "unit2"]
    assert result.targeting.qsearch == "query"
    assert result.targeting.filters == {"filter1": ["value1", "value2"]}
    assert result.targeting.plids == [1, 2, 3]
    assert result.targeting.cms_page_slug == "slug"
    assert result.limit == 10


def test_display_ads_request_from_pb_handles_empty_filters(pb_display_ads_request):
    pb_display_ads_request.targeting.filters.clear()
    result = DisplayAdsRequest.from_pb(pb_display_ads_request)
    assert result.targeting.filters == {}


def test_display_ads_request_from_pb_handles_no_filters(pb_display_ads_request_no_filters):
    result = DisplayAdsRequest.from_pb(pb_display_ads_request_no_filters)
    assert result.targeting.filters == {}


@pytest.fixture
def tracking_info():
    return TrackingInfo(uclid="uclid", uuid="uuid", cli_ubid="cli_ubid", seller_id="seller_id")


def test_tracking_info_to_pb(tracking_info):
    result = tracking_info.to_pb()
    assert result.uclid == "uclid"
    assert result.uuid == "uuid"
    assert result.cli_ubid == "cli_ubid"
    assert result.seller_id == "seller_id"


@pytest.fixture
def background():
    return Background(sm="small", md="medium", lg="large")


def test_background_to_pb_returns_correct_pb(background):
    result = background.to_pb()
    assert result.sm == "small"
    assert result.md == "medium"
    assert result.lg == "large"


@pytest.fixture
def product_ad():
    return ProductAd(
        productline_id=1,
        variant_id=2,
        offer_id=3,
        tracking_info=TrackingInfo(
            uclid="uclid", uuid="uuid", cli_ubid="cli_ubid", seller_id="seller_id"
        ),
    )


@pytest.fixture
def multi_product(product_ad):
    return MultiProduct(product_ads=[product_ad], title="title")


def test_multi_product_to_pb(multi_product):
    result = multi_product.to_pb()
    assert isinstance(result, pb.DisplayAd.MultiProduct)
    assert len(result.product_ads) == 1
    assert result.title == "title"


@pytest.fixture
def single_product(product_ad):
    return SingleProduct(product=product_ad, destination_url="url")


def test_single_product_to_pb(single_product):
    result = single_product.to_pb()
    assert result.product_ad.productline_id == 1
    assert result.product_ad.variant_id == 2
    assert result.product_ad.offer_id == 3
    assert result.product_ad.tracking.uclid == "uclid"
    assert result.product_ad.tracking.uuid == "uuid"
    assert result.product_ad.tracking.cli_ubid == "cli_ubid"
    assert result.product_ad.tracking.seller_id == "seller_id"
    assert result.destination_url == "url"


def single_product_to_pb_empty_product_ad():
    single_product = SingleProduct(product=None, destination_url="url")
    result = single_product.to_pb()
    assert result.product_ad is None
    assert result.destination_url == "url"


@pytest.fixture
def banner(background):
    return Banner(background=background, destination_url="url")


def test_banner_to_pb(banner):
    result = banner.to_pb()
    assert result.background.sm == "small"
    assert result.background.md == "medium"
    assert result.background.lg == "large"
    assert result.destination_url == "url"


def banner_to_pb_handles_empty_background():
    banner = Banner(background=None, destination_url="url")
    result = banner.to_pb()
    assert result.background is None
    assert result.destination_url == "url"


def test_display_ad_to_pb_for_banner(banner, tracking_info):
    display_ad = DisplayAd(
        ad_unit="unit1",
        ad_format="pdp-banner",
        creative=Creative.BANNER,
        tracking_info=tracking_info,
        value=banner,
    )
    result = display_ad.to_pb()
    assert result.creative == pb.CREATIVE_BANNER
    assert result.ad_format == "pdp-banner"
    assert result.ad_unit == "unit1"
    assert result.banner is not None


def test_display_ad_to_pb_for_single_product(single_product, tracking_info):
    display_ad = DisplayAd(
        ad_unit="unit1",
        ad_format="single-product",
        creative=Creative.SINGLE_PRODUCT,
        tracking_info=tracking_info,
        value=single_product,
    )
    result = display_ad.to_pb()
    assert result.ad_unit == "unit1"
    assert result.creative == pb.CREATIVE_SINGLE_PRODUCT
    assert result.ad_format == "single-product"


def test_display_ad_to_pb_for_multi_product(multi_product, tracking_info):
    display_ad = DisplayAd(
        ad_unit="unit1",
        ad_format="pdp-banner",
        creative=Creative.MULTI_PRODUCT,
        tracking_info=tracking_info,
        value=multi_product,
    )
    result = display_ad.to_pb()
    assert result.ad_unit == "unit1"
    assert result.creative == pb.CREATIVE_MULTI_PRODUCT
    assert result.multi_product is not None
    assert result.ad_format == "pdp-banner"


@pytest.mark.parametrize(
    ("enum", "pb"),
    [
        (Creative.MULTI_PRODUCT, pb.CREATIVE_MULTI_PRODUCT),
        (Creative.UNSPECIFIED, pb.CREATIVE_UNSPECIFIED),
        (Creative.BANNER, pb.CREATIVE_BANNER),
        (Creative.SINGLE_PRODUCT, pb.CREATIVE_SINGLE_PRODUCT),
    ],
)
def test_creative_enum_to_protobuf(enum, pb):
    result = enum.to_pb()
    assert result == pb


"""

@pytest.mark.parametrize(
    ("value", "expected_creative"),
    [
        (
            os.Display(
                ad_type="banner",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.SEARCH_BANNER,
                destination_url="https://www.test.com",
                products=[],
                images={
                    "bg_img_src_300x250": "https://www.test.com/img?300x250",
                    "bg_img_src_300x50": "https://www.test.com/img?300x50",
                    "bg_img_src_728x90": "https://www.test.com/img?728x90",
                    "bg_img_src_1292x120": "https://www.test.com/img?1292x120",
                },
            ),
            Creative.BANNER,
        ),
        (
            os.Display(
                ad_type="single-product",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.SINGLE_PRODUCT,
                destination_url="https://www.test.com",
                products=[
                    os.Product(
                        uclid="",
                        sku_id=93651156,
                        plid=72579690,
                        seller_id="R11434",
                        tsin=69311566,
                    )
                ],
            ),
            Creative.SINGLE_PRODUCT,
        ),
        (
            os.Display(
                ad_type="single-product",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.MULTI_PRODUCT_3,
                destination_url="https://www.test.com",
                products=[
                    os.Product(
                        uclid="",
                        sku_id=3001,
                        plid=2001,
                        seller_id="R100",
                        tsin=3001,
                    ),
                    os.Product(
                        uclid="",
                        sku_id=3002,
                        plid=2002,
                        seller_id="R200",
                        tsin=2001,
                    ),
                ],
            ),
            Creative.MULTI_PRODUCT,
        ),
    ],
)
def test_display_ad_from_dict(value, expected_creative):
    display_ad = DisplayAd.from_response(value, "test_uuid")
    assert display_ad.creative == expected_creative


def test_display_ad_from_dict_unknown_creative():
    with pytest.raises(SponsoredAdsServiceError):
        DisplayAd.from_response(
            os.Display(
                ad_type="banner",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.UNKNOWN,
                destination_url="https://www.test.com",
                products=[],
                images={
                    "bg_img_src_300x250": "https://www.test.com/img?300x250",
                    "bg_img_src_300x50": "https://www.test.com/img?300x50",
                    "bg_img_src_728x90": "https://www.test.com/img?728x90",
                    "bg_img_src_1292x120": "https://www.test.com/img?1292x120",
                },
            ),
            "test_uuid",
        )


def test_product_ads_response_from_dict():
    os_response = os.ProductsResponse(
        products=[
            os.Product(
                uclid="",
                sku_id=3001,
                plid=1001,
                seller_id="R100",
                tsin=2001,
            ),
            os.Product(
                uclid="",
                sku_id=3002,
                plid=1002,
                seller_id="R200",
                tsin=2002,
            ),
        ]
    )

    expected = ProductAdsResponse(
        products=[
            ProductAd(
                productline_id=1001,
                variant_id=2001,
                offer_id=3001,
                tracking_info=TrackingInfo(
                    uclid="",
                    uuid="test_uuid",
                    cli_ubid="",
                    seller_id="R100",
                ),
            ),
            ProductAd(
                productline_id=1002,
                variant_id=2002,
                offer_id=3002,
                tracking_info=TrackingInfo(
                    uclid="",
                    uuid="test_uuid",
                    cli_ubid="",
                    seller_id="R200",
                ),
            ),
        ]
    )
    assert ProductAdsResponse.from_response(os_response, "test_uuid") == expected


def test_display_ads_response_from_dict():
    os_response = os.DisplayResponse(
        ads=[
            os.Display(
                ad_type="banner",
                client_id="198501",
                ad_unit="pdp-slot-1",
                uclid="2|67890|67890",
                creative=os.Creative.SEARCH_BANNER,
                destination_url="https://www.test.com",
                products=[],
                images={
                    "bg_img_src_300x250": "https://www.test.com/img?300x250",
                    "bg_img_src_300x50": "https://www.test.com/img?300x50",
                    "bg_img_src_728x90": "https://www.test.com/img?728x90",
                    "bg_img_src_1292x120": "https://www.test.com/img?1292x120",
                },
            ),
        ]
    )
    expected = DisplayAdsResponse(
        display_ads=[
            DisplayAd(
                ad_unit="pdp-slot-1",
                creative=Creative.BANNER,
                tracking_info=TrackingInfo(
                    uclid="2|67890|67890",
                    uuid="test_uuid",
                    cli_ubid="198501",
                    seller_id="",
                ),
                value=Banner(
                    background=Background(
                        sm="https://www.test.com/img?300x50",
                        md="https://www.test.com/img?728x90",
                        lg="https://www.test.com/img?1292x120",
                    ),
                    destination_url="https://www.test.com",
                ),
            )
        ]
    )
    assert DisplayAdsResponse.from_response(os_response, "test_uuid") == expected"""
