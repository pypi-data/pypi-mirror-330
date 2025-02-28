import pytest
from storefront_product_adapter.factories.adapters import AdaptersFactory


@pytest.fixture
def johnny_walker_productline_adapter():
    doc = {
        "productline": {
            "id": 41670077,
            "title": "Johnnie Walker Red Label - 750ml",
            "attributes": {
                "brand": {
                    "display_name": "Brand",
                    "display_value": "Johnnie Walker",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "id": 6165,
                        "name": "Johnnie Walker",
                        "object": {
                            "image": "https://media.takealot.com/brands/johnnie_walker.gif",
                            "department_ids": [12],
                        },
                        "sort_order": 1097200,
                    },
                },
                "volume": {
                    "display_name": "Volume",
                    "display_value": "750 ml",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {"unit": "ml", "value": 750},
                },
                "warranty": {
                    "display_name": "Warranty",
                    "display_value": "Non-Returnable (6 months)",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {
                        "type": {"id": 3, "name": "Non-Returnable", "sort_order": 300},
                        "period": {"unit": "m", "value": 6},
                    },
                },
                "is_liquor": {
                    "display_name": "Is it liquor",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": True,
                },
                "pack_type": {
                    "display_name": "Pack Type",
                    "display_value": "Case",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {"id": 2, "name": "Case", "sort_order": 200},
                },
                "years_aged": {
                    "display_name": "Years Aged",
                    "display_value": "3",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": 3,
                },
                "whisky_type": {
                    "display_name": "Whisky Type",
                    "display_value": "Scotch Whisky",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {"id": 3, "name": "Scotch Whisky", "sort_order": 300},
                },
                "alcohol_content": {
                    "display_name": "Alcohol Content",
                    "display_value": "40",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": 40,
                },
                "whats_in_the_box": {
                    "display_name": "What's in the box",
                    "display_value": "1 x 750ml Bottle",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": "1 x 750ml Bottle",
                },
                "country_of_origin": {
                    "display_name": "Country of Origin",
                    "display_value": "United Kingdom",
                    "is_display_attribute": False,
                    "is_virtual_attribute": False,
                    "value": [
                        {
                            "id": "GB",
                            "iso3": "GBR",
                            "name": "United Kingdom",
                            "sort_order": 20200,
                            "is_subdivision": False,
                        }
                    ],
                },
                "merchandising_tags": {
                    "display_name": "Merchandising Tags",
                    "display_value": "Christmas",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": [{"id": 4, "name": "Christmas", "sort_order": 400}],
                },
                "product_dimensions": {
                    "display_name": "Assembled Dimensions",
                    "display_value": "7.5 x 7.5 x 29 cm",
                    "is_display_attribute": True,
                    "is_virtual_attribute": False,
                    "value": {"unit": "cm", "width": 7.5, "height": 29, "length": 7.5},
                },
                "requires_age_verification": {
                    "display_name": "Requires Age Verification",
                    "display_value": "Yes",
                    "is_display_attribute": False,
                    "is_virtual_attribute": True,
                    "value": True,
                },
            },
            "hierarchies": {
                "business": {
                    "lineages": [
                        [
                            {
                                "id": 14203,
                                "name": "Whiskey",
                                "slug": "whiskey-14203",
                                "parent_id": 14192,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.5},
                            },
                            {
                                "id": 14192,
                                "name": "Spirits",
                                "slug": "spirits-14192",
                                "parent_id": 15182,
                                "forest_id": None,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.5},
                            },
                            {
                                "id": 15182,
                                "name": "Liquor",
                                "slug": "liquor-15182",
                                "parent_id": None,
                                "forest_id": 1,
                                "metadata": {"rbs:buybox_leadtime_penalty": 0.3},
                            },
                        ]
                    ],
                    "forests": [{"id": 1, "name": "Consumables", "slug": None}],
                },
                "taxonomy": {
                    "lineages": [
                        [
                            {
                                "id": 15818,
                                "name": "Whiskey",
                                "slug": "whiskey-15818",
                                "parent_id": 15809,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 1926},
                            },
                            {
                                "id": 15809,
                                "name": "Liquor & Spirits",
                                "slug": "liquor-spirits-15809",
                                "parent_id": 15803,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 417},
                            },
                            {
                                "id": 15803,
                                "name": "Alcoholic Beverages",
                                "slug": "alcoholic-beverages-15803",
                                "parent_id": 15802,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 499676},
                            },
                            {
                                "id": 15802,
                                "name": "Beverages",
                                "slug": "beverages-15802",
                                "parent_id": 15801,
                                "forest_id": None,
                                "metadata": {"google_taxonomy": 413},
                            },
                            {
                                "id": 15801,
                                "name": "*Food, Beverages & Tobacco",
                                "slug": "food-beverages-tobacco-15801",
                                "parent_id": None,
                                "forest_id": 7,
                                "metadata": {"department": 12, "google_taxonomy": 412},
                            },
                        ]
                    ],
                    "forests": [{"id": 7, "name": "google", "slug": None}],
                },
                "merchandising": {
                    "lineages": [
                        [
                            {
                                "id": 28246,
                                "name": "Liquor",
                                "slug": "liquor-28246",
                                "forest_id": 12,
                                "parent_id": None,
                                "metadata": {},
                            },
                            {
                                "id": 25190,
                                "name": "Whiskey, Gin & Spirits",
                                "slug": "whiskey-gin-and-spirits-25190",
                                "forest_id": None,
                                "parent_id": 28246,
                                "metadata": {},
                            },
                            {
                                "id": 25200,
                                "name": "Whiskey",
                                "slug": "whiskey-25200",
                                "forest_id": None,
                                "parent_id": 25190,
                                "metadata": {},
                            },
                        ]
                    ],
                    "forests": [{"id": 12, "name": "Home & Kitchen", "slug": "home-kitchen"}],
                },
            },
        },
        "variants": {
            "44460819": {
                "variant": {
                    "id": 44460819,
                    "availability": {"status": "buyable", "reason": "At least one buyable offer"},
                },
                "offers": {
                    "52489543": {
                        "id": 52489543,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "53587715": {
                        "id": 53587715,
                        "availability": {"status": "buyable", "reason": "Stock on hand"},
                    },
                    "53587985": {
                        "id": 53587985,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "53941962": {
                        "id": 53941962,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "90396052": {
                        "id": 90396052,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "55430559": {
                        "id": 55430559,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "83243383": {
                        "id": 83243383,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "95858206": {
                        "id": 95858206,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "106915351": {
                        "id": 106915351,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                    "107768826": {
                        "id": 107768826,
                        "availability": {"status": "disabled", "reason": "Explicitly disabled"},
                    },
                },
            }
        },
    }
    return AdaptersFactory.from_productline_lineage(doc)
