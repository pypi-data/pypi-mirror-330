from __future__ import annotations

import logging
from typing import TYPE_CHECKING

from sponsored_ads_service.errors import LinkValidationError

if TYPE_CHECKING:
    from tal_stats_client import StatsClient

    from sponsored_ads_service.integrations.route import RouteIntegration
    from sponsored_ads_service.models.link_data import ActionType, LinkData

logger = logging.getLogger(__name__)

_STATS_PREFIX = "custom.validation.links.errors"


class LinkValidator:
    """
    Validator for given URL links.

    This makes use of `cms-navigation-service` to determine if the given link is a valid
    Takealot link, for the required `ActionType`.
    """

    def __init__(self, stats_client: StatsClient, route_integration: RouteIntegration) -> None:
        self._stats_client = stats_client
        self._route_integration = route_integration

    def validate(self, link: str, action: ActionType) -> LinkData:
        """
        Validate a `link`.

        Returns a `LinkData` object, if the given link passes validation for the given
        `ActionType`. Else, raises a `LinkValidationError`
        """

        return self._validate_action(link=link, action=action)

    def _validate_action(self, link: str, action: ActionType) -> LinkData:
        """
        Return a `LinkData` object, if the given link is to a valid for the specified
        `action`. Else, raises a `LinkValidationError`
        """

        link_data = self._route_integration.get_link_data(link)
        if link_data.action != action:
            self._raise_error(
                "invalid_link_action", f"Link {link} is not a valid {action.value} link"
            )

        return link_data

    def _raise_error(self, error_type: str, message: str) -> None:
        self._stats_client.incr(f"{_STATS_PREFIX}.{error_type}")
        raise LinkValidationError(message)
