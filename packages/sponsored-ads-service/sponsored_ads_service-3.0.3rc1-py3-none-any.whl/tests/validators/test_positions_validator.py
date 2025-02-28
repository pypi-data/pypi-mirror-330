from unittest.mock import call

import pytest

from sponsored_ads_service.models.positioning import Breakpoints, Positions

pytestmark = pytest.mark.validators


def test_validate(mocker):
    from sponsored_ads_service.validators.positions_validator import PositionsValidator

    apps_breakpoints = Breakpoints(sm=[0, 1, 2], medium=[0, 1, 2, 3])
    web_breakpoints = Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3, 4, 5])
    positions = Positions(apps=apps_breakpoints, web=web_breakpoints)

    sanistied_breakpoints = Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3])
    mock_validate_breakpoints = mocker.patch.object(
        PositionsValidator, "_validate_breakpoints", return_value=sanistied_breakpoints
    )
    mock_log_changes = mocker.patch.object(PositionsValidator, "_log_changes")

    output = PositionsValidator.validate(positions=positions)
    expected = Positions(apps=sanistied_breakpoints, web=sanistied_breakpoints)

    mock_validate_breakpoints.assert_any_call(apps_breakpoints)
    mock_validate_breakpoints.assert_any_call(web_breakpoints)
    mock_log_changes.assert_called_with(original=positions, sanitised=expected)
    assert output == expected


def test_validate_breakpoints(mocker):
    from sponsored_ads_service.validators.positions_validator import PositionsValidator

    sm = [0, 1, 2]
    medium = [0, 1, 2, 3]
    breakpoints = Breakpoints(sm=sm, medium=medium)

    sanitised = [0, 1, 2, 3]
    mock_dedupe_and_sort = mocker.patch.object(
        PositionsValidator, "_dedupe_and_sort", return_value=sanitised
    )

    output = PositionsValidator._validate_breakpoints(breakpoints)
    expected = Breakpoints(sm=sanitised, medium=sanitised)

    mock_dedupe_and_sort.assert_any_call(sm)
    mock_dedupe_and_sort.assert_any_call(medium)
    assert output == expected


@pytest.mark.parametrize(
    ("items", "expected"),
    [
        ([0, 4, 9, 14], [0, 4, 9, 14]),
        ([0, 4], [0, 4]),
        ([0, 4, 9, 14, 19, 24], [0, 4, 9, 14, 19, 24]),
        ([14, 4, 9, 0], [0, 4, 9, 14]),
        ([0, 4, 4, 9], [0, 4, 9]),
        ([0, 4, 4, 9, 14], [0, 4, 9, 14]),
        ([0, 0], [0]),
    ],
)
def test_dedupe_and_sort(items, expected):
    from sponsored_ads_service.validators.positions_validator import PositionsValidator

    output = PositionsValidator._dedupe_and_sort(items)
    assert output == expected


@pytest.mark.parametrize(
    ("original", "sanitised", "stats_calls"),
    [
        (
            Positions(
                apps=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
                web=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
            ),
            Positions(
                apps=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
                web=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
            ),
            [],
        ),
        (
            Positions(
                apps=Breakpoints(sm=[0, 1], medium=[0, 1]),
                web=Breakpoints(sm=[0, 1], medium=[0, 1]),
            ),
            Positions(
                apps=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
                web=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
            ),
            [call("custom.validation.positions.errors.misconfigured")],
        ),
        (
            Positions(
                apps=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
                web=Breakpoints(sm=[0, 1, 2, 3], medium=[0, 1, 2, 3]),
            ),
            Positions(
                apps=Breakpoints(sm=[0, 1], medium=[0, 1]),
                web=Breakpoints(sm=[0, 1], medium=[0, 1]),
            ),
            [call("custom.validation.positions.errors.misconfigured")],
        ),
    ],
)
def test_log_changes(mocker, original, sanitised, stats_calls):
    from sponsored_ads_service.validators.positions_validator import PositionsValidator

    mock_stats_call = mocker.patch.object(PositionsValidator._stats_client, "incr")
    PositionsValidator._log_changes(original, sanitised)
    assert mock_stats_call.call_count == len(stats_calls)
    mock_stats_call.assert_has_calls(stats_calls)
