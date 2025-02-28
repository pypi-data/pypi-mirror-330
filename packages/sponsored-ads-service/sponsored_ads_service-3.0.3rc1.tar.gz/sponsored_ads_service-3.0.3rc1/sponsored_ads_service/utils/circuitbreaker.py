"""A minimal set of utility functions to make using tal-circuitbreaker easier."""

from __future__ import annotations

import time
from contextlib import nullcontext
from typing import TYPE_CHECKING

from circuitbreaker.breaker import CircuitBreaker, CircuitBreakerSet

if TYPE_CHECKING:
    import logging
    from collections.abc import Iterable

    from statsd import StatsClient

    from sponsored_ads_service.configuration.sponsored_ads_config import CircuitBreakerConfig


class ContextBreakerSet:
    def __init__(
        self,
        *,
        config: CircuitBreakerConfig,
        upstream: str,
        error_types: Iterable[type[Exception]],
        stats_client: StatsClient,
        logger: logging.Logger,
    ) -> None:
        self._upstream = upstream
        self._config = config

        self._cb_set = CircuitBreakerSet(
            clock=time.time,
            log=logger,
            error_types=error_types,
            stats_counter=stats_client,
            max_fail=self._config.max_fail,
            reset_timeout=self._config.reset_timeout_s,
            time_unit=60,
        )

    def context(self, endpoint: str, action: str = "get") -> CircuitBreaker | nullcontext:
        if not self._config.enabled:
            return nullcontext()
        return self._cb_set.context(f"{self._upstream}.{endpoint}.{action}")
