import pytest

from sponsored_ads_service.factories.hierarchy import HierarchyFactory

pytestmark = pytest.mark.factories


def test_build_node_path_category_id(mocker, books, academic):
    mock_hierarchy_integration = mocker.Mock()
    factory = HierarchyFactory(hierarchy_integration=mock_hierarchy_integration)
    mock_hierarchy_integration.get_category_by_id.return_value = academic
    mock_hierarchy_integration.get_node_path.return_value = [books, academic]
    output = factory.build_node_path(filters={"Type": ["3"], "Category": ["15662"]})
    assert output == ["Books", "Academic"]


def test_build_node_path_category_slug(mocker, books, academic):
    mock_hierarchy_integration = mocker.Mock()
    factory = HierarchyFactory(hierarchy_integration=mock_hierarchy_integration)
    mock_hierarchy_integration.get_category_by_slug.return_value = academic
    mock_hierarchy_integration.get_node_path.return_value = [books, academic]
    output = factory.build_node_path(filters={}, category_slug="academic-15662")
    assert output == ["Books", "Academic"]


def test_build_node_path_department_id(mocker, books):
    mock_hierarchy_integration = mocker.Mock()
    factory = HierarchyFactory(hierarchy_integration=mock_hierarchy_integration)
    mock_hierarchy_integration.get_department_by_id.return_value = books
    mock_hierarchy_integration.get_node_path.return_value = [books]
    output = factory.build_node_path(filters={"Type": ["3"]})
    assert output == ["Books"]


def test_build_node_path_department_slug(mocker, books):
    mock_hierarchy_integration = mocker.Mock()
    factory = HierarchyFactory(hierarchy_integration=mock_hierarchy_integration)
    mock_hierarchy_integration.get_department_by_slug.return_value = books
    mock_hierarchy_integration.get_node_path.return_value = [books]
    output = factory.build_node_path(filters={}, department_slug="books")
    assert output == ["Books"]


def test_build_node_path_by_filter_no_returned_department(mocker):
    mock_hierarchy_integration = mocker.Mock()
    factory = HierarchyFactory(hierarchy_integration=mock_hierarchy_integration)
    mock_hierarchy_integration.get_department_by_slug.return_value = None
    output = factory.build_node_path(filters={}, department_slug="unknown")
    assert output == []


def test_build_node_path_by_filter_no_returned_category(mocker):
    mock_hierarchy_integration = mocker.Mock()
    factory = HierarchyFactory(hierarchy_integration=mock_hierarchy_integration)
    mock_hierarchy_integration.get_category_by_id.return_value = None
    output = factory.build_node_path(filters={}, category_slug="unknown-1234")
    assert output == []


def test_build_node_path_by_filter_invalid_category_slug(mocker):
    mock_hierarchy_integration = mocker.Mock()
    factory = HierarchyFactory(hierarchy_integration=mock_hierarchy_integration)
    output = factory.build_node_path(filters={}, category_slug="INVALID")
    assert output == []
