import logging

from sponsored_ads_service.configuration import Clients
from sponsored_ads_service.models.positioning import Breakpoints, Positions

logger = logging.getLogger(__name__)


class PositionsValidator:
    _stats_client = Clients().stats_client
    _stats_prefix = "custom.validation.positions.errors"

    @classmethod
    def validate(cls, positions: Positions) -> Positions:
        """
        Validate that the given `positions` object has breakpoint lists that are of the
        required size (based on the number of positions).
        """
        sanitised = Positions(
            apps=cls._validate_breakpoints(positions.apps),
            web=cls._validate_breakpoints(positions.web),
        )
        cls._log_changes(original=positions, sanitised=sanitised)
        return sanitised

    @classmethod
    def _validate_breakpoints(cls, breakpoints: Breakpoints) -> Breakpoints:
        """Validate that the given breakpoints are sanitised"""
        return Breakpoints(
            sm=cls._dedupe_and_sort(breakpoints.sm),
            medium=cls._dedupe_and_sort(breakpoints.medium),
        )

    @classmethod
    def _dedupe_and_sort(cls, items: list[int]) -> list[int]:
        """
        Create a new list where duplicates have been removed and the list sorted.
        """
        return sorted(set(items))

    @classmethod
    def _log_changes(cls, original: Positions, sanitised: Positions) -> None:
        """
        If the sanitised positions differs from the original, then log an error
        so that it is visible in sentry
        """
        if original != sanitised:
            cls._stats_client.incr(f"{cls._stats_prefix}.misconfigured")
            logger.error(
                "The positions object is misconfigured and had to be sanitised",
                extra={"original": original, "sanitised": sanitised},
            )
