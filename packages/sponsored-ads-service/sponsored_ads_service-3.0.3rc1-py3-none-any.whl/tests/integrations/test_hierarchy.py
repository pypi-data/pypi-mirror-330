import pytest
import s4f.errors
from cms_navigation_client.protobuf import navigation_service_pb2 as cms_nav_pb
from pytest_lazy_fixtures import lf
from s4f_clients.compiled_protobuffs import (
    catalogue_legacy_service_pb2 as cat_legacy_pb,
)

from sponsored_ads_service.configuration.sponsored_ads_config import MemcacheContext
from sponsored_ads_service.errors import DownstreamTimeoutError

pytestmark = pytest.mark.integrations


@pytest.fixture
def memcache(mocker):
    memcache = mocker.Mock()
    memcache.get.return_value = None
    memcache.set.return_value = None
    return memcache


@pytest.fixture
def config(mocker):
    config = mocker.Mock()
    config.get_category_by_id_cache_context.return_value = MemcacheContext(enabled=True, ttl=600)
    config.get_departments_cache_context.return_value = MemcacheContext(enabled=True, ttl=600)
    return config


def test_get_category_by_id(mocker, memcache, config, unisa):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    config.get_category_by_id_cache_context.return_value = MemcacheContext(enabled=False, ttl=0)

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cat_legacy_client.list_categories.return_value = cat_legacy_pb.ListCategoriesResponse(
        categories=[
            cat_legacy_pb.Category(
                id=20176,
                name="Unisa",
                slug="unisa-20176",
                department_id=3,
                parent_id=15662,
            )
        ]
    )
    output = integration.get_category_by_id(20176)
    mock_cat_legacy_client.list_categories.assert_called_with(category_ids=[20176], limit=1)
    assert output == unisa


def test_get_category_by_id_not_found(mocker, memcache, config, unisa):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cat_legacy_client.list_categories.return_value = cat_legacy_pb.ListCategoriesResponse(
        categories=[]
    )
    output = integration.get_category_by_id(9999)
    assert output is None


def test_get_category_by_id_raises_timeout_errors(mocker, config, memcache):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cat_legacy_client.list_categories.side_effect = s4f.errors.TimeoutError("Test Error")
    with pytest.raises(DownstreamTimeoutError):
        integration.get_category_by_id(9999)


@pytest.fixture
def departments_response_pb():
    return cms_nav_pb.MerchandisedDepartmentsResponse(
        departments=[
            cms_nav_pb.MerchandisedDepartment(department_id=2, name="Gaming", slug="gaming"),
            cms_nav_pb.MerchandisedDepartment(department_id=3, name="Books", slug="books"),
        ]
    )


@pytest.fixture
def departments(gaming, books):
    return [gaming, books]


def test_get_departments(mocker, memcache, config, departments_response_pb, departments):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cms_nav_client.get_merchandised_departments.return_value = departments_response_pb
    output = integration.get_departments()
    assert output == departments


def test_get_departments_raises_timeout_errors(mocker, config, memcache):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cms_nav_client.get_merchandised_departments.side_effect = s4f.errors.TimeoutError(
        "Test Error"
    )
    with pytest.raises(DownstreamTimeoutError):
        integration.get_departments()


@pytest.mark.parametrize(
    ("slug", "expected"),
    [
        ("gaming", lf("gaming")),
        ("books", lf("books")),
        ("unknown", None),
    ],
)
def test_department_by_slug(
    mocker, memcache, config, departments_response_pb, departments, slug, expected
):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cms_nav_client.get_merchandised_departments.return_value = departments_response_pb
    output = integration.get_department_by_slug(slug)
    assert output == expected


@pytest.mark.parametrize(
    ("department_id", "expected"),
    [
        (2, lf("gaming")),
        (3, lf("books")),
        (999, None),
    ],
)
def test_department_by_id(
    mocker, memcache, config, departments_response_pb, departments, department_id, expected
):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cms_nav_client.get_merchandised_departments.return_value = departments_response_pb
    output = integration.get_department_by_id(department_id)
    assert output == expected


def test_node_path_multiple_category_levels(mocker, memcache, config, books, academic, unisa):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    integration = HierarchyIntegration(
        cms_nav_client=mocker.Mock(),
        cat_legacy_client=mocker.Mock(),
        memcache=memcache,
        config=config,
    )
    mock_category_call = mocker.patch.object(
        integration, "get_category_by_id", return_value=academic
    )
    mock_department_call = mocker.patch.object(
        integration, "get_department_by_id", return_value=books
    )

    output = integration.get_node_path(unisa)

    mock_category_call.assert_called_with(15662)
    mock_department_call.assert_called_with(3)
    assert output == [books, academic, unisa]


def test_node_path_single_category(mocker, memcache, config, books, academic):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    integration = HierarchyIntegration(
        cms_nav_client=mocker.Mock(),
        cat_legacy_client=mocker.Mock(),
        memcache=memcache,
        config=config,
    )
    mock_department_call = mocker.patch.object(
        integration, "get_department_by_id", return_value=books
    )

    output = integration.get_node_path(academic)

    mock_department_call.assert_called_with(3)
    assert output == [books, academic]


def test_node_path_only_department(mocker, memcache, config, books):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    integration = HierarchyIntegration(
        cms_nav_client=mocker.Mock(),
        cat_legacy_client=mocker.Mock(),
        memcache=memcache,
        config=config,
    )
    output = integration.get_node_path(books)
    assert output == [books]


def test_node_path_not_found_category(mocker, memcache, config, unisa):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    integration = HierarchyIntegration(
        cms_nav_client=mocker.Mock(),
        cat_legacy_client=mocker.Mock(),
        memcache=memcache,
        config=config,
    )
    mock_category_call = mocker.patch.object(integration, "get_category_by_id", return_value=None)

    output = integration.get_node_path(unisa)

    mock_category_call.assert_called_with(15662)
    assert output == []


def test_node_path_not_found_department(mocker, memcache, config, academic):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    integration = HierarchyIntegration(
        cms_nav_client=mocker.Mock(),
        cat_legacy_client=mocker.Mock(),
        memcache=memcache,
        config=config,
    )
    mock_department_call = mocker.patch.object(
        integration, "get_department_by_id", return_value=None
    )

    output = integration.get_node_path(academic)

    mock_department_call.assert_called_with(3)
    assert output == []


def test_get_department_uncached(mocker, memcache, config, departments_response_pb, departments):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    config.get_departments_cache_context.return_value = MemcacheContext(enabled=False, ttl=0)

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    mock_cms_nav_client.get_merchandised_departments.return_value = departments_response_pb

    output = integration.get_departments()

    mock_cms_nav_client.get_merchandised_departments.assert_called_once()
    memcache.get.assert_not_called()
    memcache.set.assert_not_called()

    assert output == departments


def test_get_department_cache_hit(mocker, memcache, config, departments_response_pb, departments):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    memcache.get.return_value = departments
    output = integration.get_departments()
    memcache.get.assert_called_with("get_departments", "departments")
    assert output == departments


def test_get_category_by_id_cache_hit(mocker, memcache, config, unisa):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )
    memcache.get.return_value = unisa
    output = integration.get_category_by_id(20176)
    memcache.get.assert_called_with("get_category_by_id", "20176")
    assert output == unisa


def test_get_category_by_id_cache_miss(mocker, memcache, config, unisa):
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration

    mock_cms_nav_client = mocker.Mock()
    mock_cat_legacy_client = mocker.Mock()
    mock_cat_legacy_client.list_categories.return_value = cat_legacy_pb.ListCategoriesResponse(
        categories=[
            cat_legacy_pb.Category(
                id=20176,
                name="Unisa",
                slug="unisa-20176",
                department_id=3,
                parent_id=15662,
            )
        ]
    )

    integration = HierarchyIntegration(
        cms_nav_client=mock_cms_nav_client,
        cat_legacy_client=mock_cat_legacy_client,
        memcache=memcache,
        config=config,
    )

    memcache.get.return_value = {}
    output = integration.get_category_by_id(20176)
    memcache.get.assert_called_with("get_category_by_id", "20176")
    memcache.set.assert_called_with("get_category_by_id", "20176", unisa, ttl=600)
    assert output == unisa
