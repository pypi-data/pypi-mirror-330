import logging

from sponsored_ads_service.configuration import Clients

logger = logging.getLogger(__name__)


class DealsValidator:
    _stats_client = Clients().stats_client
    _stats_prefix = "custom.validation.deals.errors"

    @classmethod
    def _validate_deals_position(cls, position: int) -> bool:
        """Validate that the given 0-indexed position is multiples of 12"""
        if position % 12:
            cls._stats_client.incr(f"{cls._stats_prefix}.misconfigured")
            logger.error("The position has an incorrect value: %d", position)
            return False
        return True
