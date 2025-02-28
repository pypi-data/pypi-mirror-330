import pytest
from storefront_product_adapter.factories.adapters import AdaptersFactory
from storefront_product_adapter.models.common import IsoDatesRange
from storefront_product_adapter.models.promotion import Promotion, PromotionGroup

from sponsored_ads_service.errors import SponsoredProductValidationError
from sponsored_ads_service.models.validation import SponsoredProductsValidationConfig
from sponsored_ads_service.validators.sponsored_product import (
    SponsoredProductValidator,
    _PromotionsValidator,
)

pytestmark = pytest.mark.validators


@pytest.fixture
def validation_config():
    return SponsoredProductsValidationConfig(
        validate_active_and_available=True,
        validate_attribute=True,
        validate_buybox=True,
        validate_stock=True,
        validate_images=True,
        validate_promo_price=True,
        validate_promo_quantity=True,
    )


@pytest.fixture
def lineage_doc():
    return {
        "productline": {
            "id": 1001,
            "availability": {"status": "buyable"},
            "attributes": {},
            "dates": {"released": "2020-01-01T00:00:00+00:00", "preorder": None},
            "cover": {"key": "test-image.png"},
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "buyable"},
                    "buyboxes": {
                        "app": {
                            "custom_1": {"new": [3001], "used": []},
                            "lowest_priced": {"new": [2999], "used": []},
                        },
                        "web": {"custom_1": {"new": [3001], "used": []}},
                    },
                    "attributes": {},
                },
                "offers": {
                    "3001": {
                        "id": 3001,
                        "pricing": {
                            "app": {"selling_price": 350},
                            "web": {"selling_price": 350},
                        },
                        "availability": {"status": "buyable"},
                        "stock": {
                            "warehouse_regions": {"cpt": 10, "jhb": 10},
                            "warehouses_total": 20,
                            "merchant": 10,
                        },
                    }
                },
            }
        },
    }


@pytest.fixture
def lineage_doc_multiple_variants():
    return {
        "productline": {
            "id": 1002,
            "availability": {"status": "buyable"},
            "attributes": {},
            "dates": {"released": "2020-01-01T00:00:00+00:00", "preorder": None},
            "cover": {"key": "test-image.png"},
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "buyable"},
                    "buyboxes": {
                        "app": {
                            "custom_1": {"new": [3001], "used": []},
                            "lowest_priced": {"new": [2999], "used": []},
                        },
                        "web": {
                            "custom_1": {"new": [3001], "used": []},
                            "lowest_priced": {"new": [2999], "used": []},
                        },
                    },
                    "attributes": {},
                },
                "offers": {
                    "3001": {
                        "id": 3001,
                        "pricing": {
                            "app": {"selling_price": 350},
                            "web": {"selling_price": 350},
                        },
                        "availability": {"status": "buyable"},
                        "stock": {
                            "warehouse_regions": {"cpt": 10, "jhb": 10},
                            "warehouses_total": 20,
                            "merchant": 10,
                        },
                    }
                },
            },
            "2002": {
                "variant": {
                    "id": 2002,
                    "availability": {"status": "buyable"},
                    "buyboxes": {
                        "app": {
                            "custom_1": {"new": [3002], "used": []},
                            "lowest_priced": {"new": [2999], "used": []},
                        },
                        "web": {
                            "custom_1": {"new": [3002], "used": []},
                            "lowest_priced": {"new": [2999], "used": []},
                        },
                    },
                    "attributes": {},
                },
                "offers": {
                    "3002": {
                        "id": 3002,
                        "pricing": {
                            "app": {"selling_price": 380},
                            "web": {"selling_price": 380},
                        },
                        "availability": {"status": "buyable"},
                        "stock": {
                            "warehouse_regions": {"cpt": 15, "jhb": 15},
                            "warehouses_total": 30,
                            "merchant": 15,
                        },
                    }
                },
            },
        },
    }


@pytest.fixture
def lineage_doc_no_winning_offers():
    return {
        "productline": {
            "id": 1001,
            "availability": {"status": "buyable"},
            "attributes": {},
            "dates": {"released": "2020-01-01T00:00:00+00:00", "preorder": None},
            "cover": {"key": "test-image.png"},
        },
        "variants": {
            "2001": {
                "variant": {
                    "id": 2001,
                    "availability": {"status": "buyable"},
                    "buyboxes": {
                        "app": {"custom_1": {"new": [], "used": []}},
                        "web": {"custom_1": {"new": [], "used": []}},
                    },
                    "attributes": {},
                },
                "offers": {},
            }
        },
    }


def test_validate_success(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    validator.validate(productline, offer_id=3001)


def test_validate_has_winning_offer_success(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    validator.validate(productline, offer_id=3001)


def test_validate_has_winning_offer_failure(
    mocker, lineage_doc_no_winning_offers, validation_config
):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    productline = AdaptersFactory.from_productline_lineage(lineage_doc_no_winning_offers)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=9999)
    assert e.value.error_type == "no_winning_offer"


def test_validate_buybox_winner_failure(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=9999)
    assert e.value.error_type == "buybox"


def test_validate_buybox_winner_multiple_variants(
    mocker, lineage_doc_multiple_variants, validation_config
):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    productline = AdaptersFactory.from_productline_lineage(lineage_doc_multiple_variants)
    validator.validate(productline, offer_id=9999)


def test_validate_buybox_winner_disabled(mocker, lineage_doc, validation_config):
    validation_config.validate_buybox = False
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    spy_validate_buybox_winner = mocker.spy(validator, "_validate_buybox_winner")
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    validator.validate(productline, offer_id=9999)
    assert spy_validate_buybox_winner.call_count == 0


def test_validate_buyable_failure(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    lineage_doc["productline"]["availability"]["status"] = "non_buyable"
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=3001)
    assert e.value.error_type == "buyable"


def test_validate_do_not_sponsor_attribute_failure(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    lineage_doc["productline"]["attributes"] = {
        "do_not_sponsor": {
            "display_name": "Do not Sponsor",
            "display_value": "Yes",
            "is_display_attribute": False,
            "is_virtual_attribute": False,
            "value": True,
        }
    }
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=3001)
    assert e.value.error_type == "do_not_sponsor"


def test_validate_is_not_sellable_attribute_failure(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    lineage_doc["variants"]["2001"]["variant"]["attributes"] = {
        "is_not_sellable": {
            "display_name": "Is Not Sellable",
            "display_value": "Yes",
            "is_display_attribute": False,
            "is_virtual_attribute": False,
            "value": True,
        }
    }
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=3001)
    assert e.value.error_type == "is_not_sellable"


def test_validate_stock_failure(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    lineage_doc["variants"]["2001"]["offers"]["3001"]["availability"]["status"] = "non_buyable"
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=3001)
    assert e.value.error_type == "stock"


def test_validate_has_images_failure(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    lineage_doc["productline"]["cover"] = {"key": None}
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=3001)
    assert e.value.error_type == "images"


def test_validate_calls_promotions_validator_when_promo_ids_present(
    mocker, lineage_doc, validation_config
):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    mock_promotions_validator = mocker.patch.object(validator, "_promotions_validator")
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)

    validator.validate(productline, offer_id=3001, promotion_ids=[1234])
    mock_promotions_validator.validate.assert_called_with(mocker.ANY, [1234])


@pytest.fixture
def promotions():
    return [
        Promotion(
            promotion_id=4001,
            deal_id=234,
            group=PromotionGroup.ON_TAB,
            quantity=3,
            active=True,
            position=999,
            product_qualifying_quantity=1,
            promotion_qualifying_quantity=1,
            display_name="Test Name",
            slug="test",
            dates=IsoDatesRange(
                start="2022-01-01T22:00:00+00:00",
                end="2023-01-31T21:59:00+00:00",
            ),
            price=100,
            promotion_price=800,
            is_lead_time_allowed=False,
        )
    ]


def test_validate_promotions_success(mocker, promotions):
    mock_variants = mocker.Mock()
    mock_variants.get_active_promotions.return_value = promotions
    validator = _PromotionsValidator(stats_client=mocker.Mock())

    validator.validate(mock_variants, promotion_ids=[4001])


def test_validate_promotions_no_matching_promo_id(mocker, promotions):
    mock_variants = mocker.Mock()
    mock_variants.get_active_promotions.return_value = promotions
    validator = _PromotionsValidator(stats_client=mocker.Mock())

    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(mock_variants, promotion_ids=[9999])
    assert e.value.error_type == "promotion_id"


@pytest.fixture
def promotions_invalid_price():
    return [
        Promotion(
            promotion_id=4002,
            deal_id=234,
            group=PromotionGroup.ON_TAB,
            quantity=3,
            active=True,
            position=999,
            product_qualifying_quantity=1,
            promotion_qualifying_quantity=1,
            display_name="Test Name",
            slug="test",
            dates=IsoDatesRange(
                start="2022-01-01T22:00:00+00:00",
                end="2023-01-31T21:59:00+00:00",
            ),
            price=0,
            promotion_price=800,
            is_lead_time_allowed=False,
        )
    ]


def test_validate_invalid_promotion_price(mocker, promotions_invalid_price):
    mock_variants = mocker.Mock()
    mock_variants.get_active_promotions.return_value = promotions_invalid_price
    validator = _PromotionsValidator(stats_client=mocker.Mock())

    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(mock_variants, promotion_ids=[4002])
    assert e.value.error_type == "promotion_price"


@pytest.fixture
def promotions_invalid_quantity():
    return [
        Promotion(
            promotion_id=4003,
            deal_id=234,
            group=PromotionGroup.ON_TAB,
            quantity=0,
            active=True,
            position=999,
            product_qualifying_quantity=1,
            promotion_qualifying_quantity=1,
            display_name="Test Name",
            slug="test",
            dates=IsoDatesRange(
                start="2022-01-01T22:00:00+00:00",
                end="2023-01-31T21:59:00+00:00",
            ),
            price=100,
            promotion_price=800,
            is_lead_time_allowed=False,
        )
    ]


def test_validate_invalid_promotion_quantity(mocker, promotions_invalid_quantity):
    mock_variants = mocker.Mock()
    mock_variants.get_active_promotions.return_value = promotions_invalid_quantity
    validator = _PromotionsValidator(stats_client=mocker.Mock())

    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(mock_variants, promotion_ids=[4003])
    assert e.value.error_type == "promotion_price"


def test_validate_offer_opt_true_and_fails_validation(mocker, lineage_doc, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    productline = AdaptersFactory.from_productline_lineage(lineage_doc)
    with pytest.raises(SponsoredProductValidationError) as e:
        validator.validate(productline, offer_id=3001, offer_opt=True)
    assert e.value.error_type == "no_winning_offer"


def test_validate_offer_opt_false(mocker, lineage_doc_multiple_variants, validation_config):
    validator = SponsoredProductValidator(
        stats_client=mocker.Mock(), validation_config=validation_config
    )
    productline = AdaptersFactory.from_productline_lineage(lineage_doc_multiple_variants)
    validator.validate(productline, offer_id=3001, offer_opt=False)
