import contextlib

import pytest
from circuitbreaker.breaker import CircuitOpenError

from sponsored_ads_service.configuration.sponsored_ads_config import CircuitBreakerConfig
from sponsored_ads_service.utils.circuitbreaker import ContextBreakerSet


def test_circuitbreaker_enabled(mocker):
    # === Setup ===
    mock_logger = mocker.MagicMock()
    cfg = CircuitBreakerConfig(enabled=True, reset_timeout_s=3, max_fail=2)
    cb_set = ContextBreakerSet(
        config=cfg,
        upstream="far_away",
        error_types=[ValueError],
        logger=mock_logger,
        stats_client=mocker.MagicMock(),
    )

    def do_broken_thing():
        for n in range(4):  # Why 4? Figure this out one day
            with contextlib.suppress(ValueError), cb_set.context("endpoint", action="beep"):
                msg = f"boom {n}"
                raise ValueError(msg)

    # === Execute to Verify ===
    # Force it to open
    with pytest.raises(CircuitOpenError):
        do_broken_thing()


def test_circuitbreaker_disabled(mocker):
    # === Setup ===
    mock_logger = mocker.MagicMock()
    cfg = CircuitBreakerConfig(enabled=False, reset_timeout_s=3, max_fail=2)
    cb_set = ContextBreakerSet(
        config=cfg,
        upstream="far_away",
        error_types=[ValueError],
        logger=mock_logger,
        stats_client=mocker.MagicMock(),
    )

    def do_broken_thing():
        for n in range(4):  # Why 4? Figure this out one day
            with contextlib.suppress(ValueError), cb_set.context("endpoint", action="beep"):
                msg = f"boom {n}"
                raise ValueError(msg)

    # === Execute to Verify ===
    # We suppress the ValueError and should not see any CircuitOpenError raised
    do_broken_thing()
