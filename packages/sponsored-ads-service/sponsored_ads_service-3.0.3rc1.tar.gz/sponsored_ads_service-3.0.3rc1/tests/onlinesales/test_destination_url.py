import pytest


@pytest.fixture
def config(mocker):
    mock_config = mocker.Mock()
    mock_config.get_link_data_hostname.return_value = "www.takealot.com"
    mock_config.get_sponsored_display_search_filters_plid_limit.return_value = 5
    return mock_config


@pytest.fixture
def catalogue_integration(mocker):
    mock_catalogue = mocker.Mock()
    mock_catalogue.get_relative_url_for_plid.return_value = "/product-title/PLID123"
    return mock_catalogue


@pytest.fixture
def link_validator(mocker):
    mock_validator = mocker.Mock()
    mock_validator.validate.side_effect = lambda link, action: mocker.Mock(
        parameters={"url": link}
    )
    return mock_validator


@pytest.fixture
def destination_url_factory(config, catalogue_integration, link_validator):
    from sponsored_ads_service.onlinesales.destination_url_factory import DestinationUrlFactory

    return DestinationUrlFactory(config, catalogue_integration, link_validator)


def test_returns_existing_destination_url(mocker, destination_url_factory):
    display_ad = mocker.Mock(destination_url="https://www.takealot.com/existing-url")
    result = destination_url_factory.from_display_ad(display_ad)
    assert result == "https://www.takealot.com/existing-url"


def test_builds_url_for_single_product(mocker, destination_url_factory):
    product = mocker.Mock(plid=123)
    display_ad = mocker.Mock(destination_url=None, products=[product])
    result = destination_url_factory.from_display_ad(display_ad)
    assert result == "https://www.takealot.com/product-title/PLID123"


def test_builds_single_product_url(mocker, destination_url_factory):
    product = mocker.Mock(plid=123)
    result = destination_url_factory._from_products([product])
    assert result == "https://www.takealot.com/product-title/PLID123"


def test_returns_none_for_invalid_product_title(mocker, destination_url_factory):
    product = mocker.Mock(plid=999)
    destination_url_factory._catalogue_integration.get_relative_url_for_plid.return_value = None
    result = destination_url_factory._from_products([product])
    assert result is None


def test_builds_multiple_products_url(mocker, destination_url_factory):
    products = [mocker.Mock(plid=i) for i in range(1, 4)]
    result = destination_url_factory._from_products(products)
    assert result == "https://www.takealot.com/all?filter=Id:1|2|3"


def test_respects_plid_limit(mocker, destination_url_factory):
    products = [mocker.Mock(plid=i) for i in range(1, 10)]
    result = destination_url_factory._from_products(products)
    assert result == "https://www.takealot.com/all?filter=Id:1|2|3|4|5"
