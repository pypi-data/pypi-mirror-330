from typing import ClassVar

from sponsored_ads_service.models.positioning import Positions
from sponsored_ads_service.validators.positions_validator import PositionsValidator

_VariantsDict = dict[str, dict[str, Positions]]


class ABTestPositions:
    # NOTE: Make sure that the platform and variant keys are lowercase
    _platform_apps = ("android", "ios")
    _app_positions = Positions.create_basic([0, 1, 6, 7, 10, 11, 20, 21])
    _desktop_positions = Positions.create_basic([0, 1, 6, 7, 10, 11, 20, 21])
    _base_positions = Positions.create_basic([0, 1, 6, 7, 10, 11, 20, 21])
    _deals_positions = (0, 12)
    _variants: ClassVar[_VariantsDict] = {}  # For future AB tests

    def get_positions(self, platform: str, experiment_variant: str | None = None) -> Positions:
        positions = self._get_variant_positions(
            platform=platform, experiment_variant=experiment_variant
        )
        return PositionsValidator.validate(positions=positions)

    def _get_variant_positions(
        self, platform: str, experiment_variant: str | None = None
    ) -> Positions:
        if experiment_variant:
            platform_variants = self._variants.get(platform.lower())
            if platform_variants:
                positions = platform_variants.get(experiment_variant.lower())
                if positions:
                    return positions
        if platform.lower() in self._platform_apps:
            return self._app_positions
        if platform.lower() == "desktop":
            return self._desktop_positions

        return self._base_positions
