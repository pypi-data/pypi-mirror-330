from unittest.mock import call

import pytest

pytestmark = pytest.mark.validators


@pytest.mark.parametrize(
    ("position", "stats_calls"),
    [
        (0, []),
        (1, [call("custom.validation.deals.errors.misconfigured")]),
        (3, [call("custom.validation.deals.errors.misconfigured")]),
        (4, [call("custom.validation.deals.errors.misconfigured")]),
        (5, [call("custom.validation.deals.errors.misconfigured")]),
        (6, [call("custom.validation.deals.errors.misconfigured")]),
        (7, [call("custom.validation.deals.errors.misconfigured")]),
        (8, [call("custom.validation.deals.errors.misconfigured")]),
        (9, [call("custom.validation.deals.errors.misconfigured")]),
        (10, [call("custom.validation.deals.errors.misconfigured")]),
        (11, [call("custom.validation.deals.errors.misconfigured")]),
        (12, []),
        (13, [call("custom.validation.deals.errors.misconfigured")]),
        (24, []),
        (30, [call("custom.validation.deals.errors.misconfigured")]),
        (36, []),
        (40, [call("custom.validation.deals.errors.misconfigured")]),
        (48, []),
    ],
)
def test_validate_deals_position(mocker, position, stats_calls):
    from sponsored_ads_service.validators.deals_validator import DealsValidator

    mock_stats_call = mocker.patch.object(DealsValidator._stats_client, "incr")
    DealsValidator._validate_deals_position(position)
    assert mock_stats_call.call_count == len(stats_calls)
    mock_stats_call.assert_has_calls(stats_calls)
