from __future__ import annotations

import re
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from sponsored_ads_service.integrations.hierarchy import HierarchyIntegration
    from sponsored_ads_service.models.hierarchy import Category, Department, Node
    from sponsored_ads_service.models.request_response import Filters


class HierarchyFactory:
    """
    Factory tooling for hierarchies (departments and categories)
    """

    def __init__(self, hierarchy_integration: HierarchyIntegration) -> None:
        self._hierarchy_integration = hierarchy_integration

    def build_node_path(
        self,
        filters: Filters,
        department_slug: str | None = None,
        category_slug: str | None = None,
    ) -> list[str]:
        """
        Build and return an ordered list of hierarchies, derived from the given request
        department and/or category slugs, or the request `filters`.
        """

        node: Node | None = self._get_category_by_filter(filters, category_slug)
        if not node:
            node = self._get_department_by_filter(filters, department_slug)
        if node:
            path = self._hierarchy_integration.get_node_path(node)
            return [item.name for item in path]
        return []

    def _get_department_by_filter(
        self, filters: Filters, department_slug: str | None = None
    ) -> Department | None:
        """
        Return a `Department` model, derived from the given request `department_slug`,
        or `filters`.

        If `department_slug` is given, this takes precedence. Else, a `Type` filter
        is used (if present).
        """

        if department_slug:
            dept = self._hierarchy_integration.get_department_by_slug(department_slug)
            if dept:
                return dept

        type_filters = filters.get("Type")
        if type_filters and type_filters[0].isdigit():
            dept_id = int(type_filters[0])
            return self._hierarchy_integration.get_department_by_id(dept_id)

        return None

    def _get_category_by_filter(
        self, filters: Filters, category_slug: str | None = None
    ) -> Category | None:
        """
        Return a `Category` model, derived from the given request `category_slug`,
        or `filters`.

        If `category_slug` is given, this takes precedence. Else, a `Category` filter
        is used (if present).
        """

        if category_slug:
            match = re.match(
                r"^[a-zA-Z-]+-(?P<cat_id>\d{2,})$",
                category_slug,
            )
            if match and match.group("cat_id"):
                cat_id = int(match.group("cat_id"))
                cat = self._hierarchy_integration.get_category_by_id(cat_id)
                if cat:
                    return cat

        cat_filters = filters.get("Category")
        if cat_filters and cat_filters[0].isdigit():
            cat_id = int(cat_filters[0])
            return self._hierarchy_integration.get_category_by_id(cat_id)

        return None
