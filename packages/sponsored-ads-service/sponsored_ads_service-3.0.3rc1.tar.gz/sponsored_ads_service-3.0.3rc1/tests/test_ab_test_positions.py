import pytest
from pytest_lazy_fixtures import lf

from sponsored_ads_service.models.positioning import Positions


@pytest.fixture
def app_positions():
    return Positions.create_basic([0, 1, 10, 11, 20, 21])


@pytest.fixture
def desktop_positions():
    return Positions.create_basic([0, 1, 10, 11, 20, 21])


@pytest.fixture
def variant_a():
    return Positions.create_basic([0, 4, 8, 12, 16, 20])


@pytest.fixture
def variant_b():
    return Positions.create_basic([0, 1, 6, 7, 12, 13])


@pytest.fixture
def variant_c():
    return Positions.create_basic([0, 1, 10, 11, 20, 21])


@pytest.fixture
def variants(variant_a, variant_b, variant_c):
    return {"desktop": {"a": variant_a, "b": variant_b, "c": variant_c}}


@pytest.fixture
def ab_test_data(mocker, app_positions, desktop_positions, variants):
    from sponsored_ads_service.ab_test_positions import ABTestPositions

    mocker.patch.object(ABTestPositions, "_app_positions", app_positions)
    mocker.patch.object(ABTestPositions, "_variants", variants)
    mocker.patch.object(ABTestPositions, "_desktop_positions", desktop_positions)
    mocker.patch.object(ABTestPositions, "_base_positions", desktop_positions)
    mocker.patch.object(ABTestPositions, "_platform_apps", ["android", "ios"])


def test_get_positions(mocker, desktop_positions):
    from sponsored_ads_service.ab_test_positions import ABTestPositions
    from sponsored_ads_service.validators.positions_validator import PositionsValidator

    mock_get_variant_positions = mocker.patch.object(
        ABTestPositions, "_get_variant_positions", return_value=desktop_positions
    )
    mock_validate = mocker.patch.object(PositionsValidator, "validate")
    output = ABTestPositions().get_positions(platform="DeskTop", experiment_variant=None)

    mock_get_variant_positions.assert_called_with(platform="DeskTop", experiment_variant=None)
    mock_validate.assert_called_with(positions=desktop_positions)
    assert output == mock_validate.return_value


@pytest.mark.parametrize(
    ("experiment_variant", "platform", "expected"),
    [
        ("a", "android", lf("app_positions")),
        ("b", "ANDROID", lf("app_positions")),
        ("a", "Ios", lf("app_positions")),
        ("k", "Ios", lf("app_positions")),
        ("a", "desktop", lf("variant_a")),
        ("c", "Desktop", lf("variant_c")),
        ("z", "Desktop", lf("desktop_positions")),
        (None, "Desktop", lf("desktop_positions")),
        (None, "Unknown", lf("desktop_positions")),
    ],
)
def test_get_variant_positions(ab_test_data, experiment_variant, platform, expected):
    from sponsored_ads_service.ab_test_positions import ABTestPositions

    output = ABTestPositions()._get_variant_positions(
        platform=platform, experiment_variant=experiment_variant
    )
    assert output == expected
