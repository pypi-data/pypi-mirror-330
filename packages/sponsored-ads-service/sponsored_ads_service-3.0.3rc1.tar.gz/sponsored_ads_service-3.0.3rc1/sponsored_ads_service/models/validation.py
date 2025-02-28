from dataclasses import dataclass


@dataclass
class SponsoredProductsValidationConfig:
    validate_active_and_available: bool = True
    validate_attribute: bool = True
    validate_buybox: bool = True
    validate_stock: bool = True
    validate_images: bool = True
    validate_promo_price: bool = True
    validate_promo_quantity: bool = True
