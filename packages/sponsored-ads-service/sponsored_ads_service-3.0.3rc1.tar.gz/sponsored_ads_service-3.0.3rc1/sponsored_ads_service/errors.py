from s4f.errors import ServiceError


# === Internal errors ===
class ConfigurationError(Exception): ...


class SponsoredProductValidationError(Exception):
    def __init__(self, message: str, error_type: str = "unknown"):
        self.error_type = error_type
        super().__init__(message)


class SponsoredProductPromotionValidationError(Exception): ...


class LinkValidationError(Exception): ...


class UnsupportedLocationError(Exception): ...


# === Service errors ===
class SponsoredAdsServiceError(ServiceError):
    def __init__(self, error_message: str, error_code: int = 500) -> None:
        super().__init__(error_code=error_code, error_message=error_message)


class DownstreamTimeoutError(SponsoredAdsServiceError):
    def __init__(self, service_name: str) -> None:
        super().__init__(f"Timeout to Downstream Service: {service_name}")


class BadRequestError(SponsoredAdsServiceError):
    def __init__(self, error_message: str) -> None:
        super().__init__(error_code=400, error_message=error_message)


class SponsoredDisplayMissingBannerError(SponsoredAdsServiceError):
    def __init__(self, message: str, error_type: str = "unknown"):
        self.error_type = error_type
        super().__init__(message)


class DownstreamError(SponsoredAdsServiceError):
    def __init__(self, service_name: str) -> None:
        super().__init__(f"Error with Downstream: {service_name}")
