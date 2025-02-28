import pytest

from sponsored_ads_service.errors import LinkValidationError
from sponsored_ads_service.models.link_data import ActionType, Context, LinkData

pytestmark = pytest.mark.validators


def test_validate_success(mocker):
    from sponsored_ads_service.validators.link_validator import LinkValidator

    link_data = LinkData(action=ActionType.SEARCH, context=Context.NAVIGATION, parameters={})

    mock_route_integration = mocker.Mock()
    mock_route_integration.get_link_data.return_value = link_data

    validator = LinkValidator(stats_client=mocker.Mock(), route_integration=mock_route_integration)
    output = validator.validate("https://foo.bar", action=ActionType.SEARCH)

    assert output == link_data


def test_validate_error(mocker):
    from sponsored_ads_service.validators.link_validator import LinkValidator

    mock_route_integration = mocker.Mock()
    mock_route_integration.get_link_data.return_value = LinkData(
        action=ActionType.SEARCH, context=Context.BROWSER, parameters={}
    )
    validator = LinkValidator(stats_client=mocker.Mock(), route_integration=mock_route_integration)
    with pytest.raises(LinkValidationError):
        validator.validate("https://foo.bar", action=ActionType.PRODUCT)
