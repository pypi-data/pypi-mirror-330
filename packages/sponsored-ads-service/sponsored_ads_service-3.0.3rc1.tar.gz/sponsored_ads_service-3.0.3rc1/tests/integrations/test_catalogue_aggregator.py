import pytest
from catalogue_aggregator_client.types import ItemType


@pytest.fixture
def filtered_lineage():
    return {
        "1101": {
            "productline": {"id": 1101, "attributes": {}},
            "variants": {
                "2101": {
                    "variant": {"id": 2101, "availability": {"status": "buyable"}},
                    "offers": {"3101": {"id": 3101, "availability": {"status": "buyable"}}},
                },
                "2102": {
                    "variant": {"id": 2102, "availability": {"status": "buyable"}},
                    "offers": {
                        "3201": {"id": 3103, "availability": {"status": "non_buyable"}},
                        "3202": {"id": 3102, "availability": {"status": "buyable"}},
                    },
                },
                "2103": {
                    "variant": {"id": 2103, "availability": {"status": "non_buyable"}},
                    "offers": {"3301": {"id": 3104, "availability": {"status": "non_buyable"}}},
                },
            },
        }
    }


@pytest.fixture
def multiple_docs_and_buyabilities():
    return {
        "1101": {
            "productline": {"id": 1101, "relative_url": "/title_1101/PLID1101", "attributes": {}},
            "variants": {
                "2101": {
                    "variant": {"id": 2101, "availability": {"status": "buyable"}},
                    "offers": {"3101": {"id": 3101, "availability": {"status": "buyable"}}},
                },
                "2102": {
                    "variant": {"id": 2102, "availability": {"status": "buyable"}},
                    "offers": {
                        "3201": {"id": 3103, "availability": {"status": "non_buyable"}},
                        "3202": {"id": 3102, "availability": {"status": "buyable"}},
                    },
                },
                "2103": {
                    "variant": {"id": 2103, "availability": {"status": "non_buyable"}},
                    "offers": {"3301": {"id": 3104, "availability": {"status": "non_buyable"}}},
                },
            },
        },
        "1201": {
            "productline": {"id": 1201, "relative_url": "/title_1201/PLID1201", "attributes": {}},
            "variants": {
                "2201": {
                    "variant": {"id": 2201, "availability": {"status": "buyable"}},
                    "offers": {"3101": {"id": 3201, "availability": {"status": "buyable"}}},
                },
                "2202": {
                    "variant": {"id": 2202, "availability": {"status": "buyable"}},
                    "offers": {
                        "3201": {"id": 3202, "availability": {"status": "non_buyable"}},
                        "3202": {"id": 3203, "availability": {"status": "buyable"}},
                    },
                },
                "2203": {
                    "variant": {"id": 2203, "availability": {"status": "non_buyable"}},
                    "offers": {"3301": {"id": 3204, "availability": {"status": "non_buyable"}}},
                },
            },
        },
        "1301": {
            "productline": {
                "id": 1301,
                "title": "title_1301",
                "relative_url": "/title_1301/PLID1301",
                "attributes": {
                    "do_not_promote_other_items_with_item": {
                        "display_name": "do_not_promote_other_items_with_item",
                        "value": "True",
                        "display_value": "do_not_promote_other_items_with_item",
                        "is_display_attribute": "false",
                        "is_virtual_attribute": "false",
                    }
                },
            },
            "variants": {
                "2301": {
                    "variant": {"id": 2301, "availability": {"status": "buyable"}},
                    "offers": {"3101": {"id": 3301, "availability": {"status": "buyable"}}},
                },
            },
        },
    }


@pytest.fixture
def multiple_docs_and_buyabilities_productlines(multiple_docs_and_buyabilities):
    from storefront_product_adapter.factories.adapters import AdaptersFactory

    return {
        i: AdaptersFactory.from_productline_lineage(d)
        for i, d in multiple_docs_and_buyabilities.items()
    }


def test_get_offer_ids_for_plids(mocker, mock_aggregator_client, multiple_docs_and_buyabilities):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = (
        multiple_docs_and_buyabilities
    )
    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = {}
    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )
    output = integration.get_offer_ids_for_plids([1001, 1002])
    assert output == [3101, 3102, 3201, 3203]


def test_get_title_for_plid(mocker, mock_aggregator_client, multiple_docs_and_buyabilities):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = {
        "1101": multiple_docs_and_buyabilities.get("1101")
    }
    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = {}
    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )
    output = integration.get_relative_url_for_plid(1101)
    assert output == "/title_1101/PLID1101"


def test_get_title_for_plid_no_result(
    mocker, mock_aggregator_client, multiple_docs_and_buyabilities
):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = {}
    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = {}
    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )
    output = integration.get_relative_url_for_plid(1101)
    assert output is None


def test_get_title_for_plid_no_result_in_map(
    mocker, mock_aggregator_client, multiple_docs_and_buyabilities
):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = {
        "1102": multiple_docs_and_buyabilities.get("1101")
    }
    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = {}
    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )
    output = integration.get_relative_url_for_plid(1101)
    assert output is None


def test_get_filtered_productline_adapters(mocker, mock_aggregator_client, filtered_lineage):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = (
        filtered_lineage
    )
    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        memcache=mocker.MagicMock(),
    )

    integration.get_filtered_productline_adapters([1001, 1002])
    integration._aggregator_client.fetch_productline_lineage_by_type_and_ids.assert_called_once_with(
        [1001, 1002],
        item_type=ItemType.PRODUCTLINE,
        filters={
            "productline": {
                "properties": [
                    "id",
                    "hierarchies",
                    "attributes",
                ],
            },
            "variants": {
                "variant": {"properties": ["id", "availability"]},
                "offers": {"properties": ["id", "availability"]},
            },
        },
    )


def test_get_offer_ids_for_plids_caching(
    mocker,
    mock_aggregator_client,
    multiple_docs_and_buyabilities,
    multiple_docs_and_buyabilities_productlines,
):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = (
        multiple_docs_and_buyabilities
    )
    config = mocker.MagicMock()
    config.get_catalogue_aggregator_cache_context.return_value = mocker.MagicMock(
        enabled=True, ttl=10
    )

    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = {}
    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=config,
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )

    integration._get_productline_adapters_uncached = mocker.MagicMock(
        return_value=multiple_docs_and_buyabilities_productlines
    )
    output = integration.get_offer_ids_for_plids([3102, 3102])
    integration._memcache.get_multi.assert_called_with(
        context="get_offer_ids_for_plids", keys=["3102", "3102"]
    )
    integration._memcache.set_multi.assert_called_with(
        context="get_offer_ids_for_plids", data=multiple_docs_and_buyabilities_productlines, ttl=10
    )
    assert output == [3101, 3102, 3201, 3203]


def test_gget_offer_ids_for_plids_caching_no_hits(mocker, mock_aggregator_client):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = {}
    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = {}
    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )
    output = integration.get_offer_ids_for_plids([1001, 1002])
    integration._memcache.get_multi.assert_called_with(
        context="get_offer_ids_for_plids", keys=["1001", "1002"]
    )
    integration._memcache.set_multi.assert_not_called()
    assert output == []


def test_get_offer_ids_for_plids_caching_no_misses(
    mocker, mock_aggregator_client, multiple_docs_and_buyabilities_productlines
):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = {}
    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = multiple_docs_and_buyabilities_productlines

    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=mocker.MagicMock(),
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )

    output = integration.get_offer_ids_for_plids([1101, 1201, 1301])
    integration._memcache.get_multi.assert_called_with(
        context="get_offer_ids_for_plids", keys=["1101", "1201", "1301"]
    )
    integration._aggregator_client.fetch_productline_lineage_by_type_and_ids.assert_not_called()
    assert output == [3101, 3102, 3201, 3203]


def test_get_offer_ids_for_plids_caching_disabled(
    mocker, mock_aggregator_client, multiple_docs_and_buyabilities_productlines
):
    from sponsored_ads_service.integrations.catalogue_aggregator import (
        CatalogueAggregatorIntegration,
    )

    mock_aggregator_client.fetch_productline_lineage_by_type_and_ids.return_value = {}
    memcache = mocker.MagicMock()
    memcache.get_multi.return_value = multiple_docs_and_buyabilities_productlines

    config = mocker.MagicMock()
    config.get_catalogue_aggregator_cache_context.return_value = mocker.MagicMock(enabled=False)

    integration = CatalogueAggregatorIntegration(
        aggregator_client=mock_aggregator_client,
        config=config,
        stats_client=mocker.MagicMock(),
        memcache=memcache,
    )

    integration._get_productline_adapters_cached = mocker.MagicMock()
    integration._get_productline_adapters_uncached = mocker.MagicMock()

    integration.get_offer_ids_for_plids([1101, 1201, 1301])

    integration._get_productline_adapters_cached.assert_not_called()
    integration._get_productline_adapters_uncached.assert_called()
