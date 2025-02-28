from __future__ import annotations

from typing import TYPE_CHECKING

import s4f.errors
from opentelemetry import trace

from sponsored_ads_service.errors import DownstreamTimeoutError
from sponsored_ads_service.models.hierarchy import Category, Department, Node

if TYPE_CHECKING:
    from cms_navigation_client import CmsNavigationClient
    from s4f_clients.catalogue_legacy import CatalogueLegacyServiceClient

    from sponsored_ads_service.configuration import SponsoredAdsConfig
    from sponsored_ads_service.configuration.sponsored_ads_config import MemcacheContext
    from sponsored_ads_service.utils.memcache import Memcache

tracer = trace.get_tracer(__name__)


class HierarchyIntegration:
    def __init__(
        self,
        cms_nav_client: CmsNavigationClient,
        cat_legacy_client: CatalogueLegacyServiceClient,
        memcache: Memcache,
        config: SponsoredAdsConfig,
    ) -> None:
        self._cms_nav_client = cms_nav_client
        self._cat_legacy_client = cat_legacy_client
        self._memcache = memcache
        self._config = config

    def get_category_by_id(self, category_id: int) -> Category | None:
        cache_context = self._config.get_category_by_id_cache_context()
        if cache_context.enabled:
            return self.get_category_by_id_cached(cache_context, category_id)
        return self.get_category_by_id_uncached(category_id)

    def get_category_by_id_cached(
        self, cache_context: MemcacheContext, category_id: int
    ) -> Category | None:
        memcache_context = self.get_category_by_id.__name__
        if result := self._memcache.get(memcache_context, str(category_id)):
            return result

        category = self.get_category_by_id_uncached(category_id)
        if category:
            self._memcache.set(
                memcache_context,
                str(category_id),
                category,
                ttl=cache_context.ttl,
            )
        return category

    @tracer.start_as_current_span("HierarchyIntegration.get_category_by_id_uncached")
    def get_category_by_id_uncached(self, category_id: int) -> Category | None:
        try:
            response = self._cat_legacy_client.list_categories(category_ids=[category_id], limit=1)
        except (s4f.errors.TimeoutError, s4f.errors.CommunicationError):
            raise DownstreamTimeoutError("s4f-catalogue-legacy")

        if response.categories:
            data = response.categories[0]
            return Category(
                id=data.id,
                name=data.name,
                parent_id=data.parent_id if data.parent_id else None,
                department_id=data.department_id,
                slug=data.slug,
            )
        return None

    def get_departments(self) -> list[Department]:
        cache_context = self._config.get_departments_cache_context()
        if cache_context.enabled:
            return self.get_departments_cached(cache_context)
        return self.get_departments_uncached()

    def get_departments_cached(self, cache_context: MemcacheContext) -> list[Department]:
        memcache_context = self.get_departments.__name__
        if result := self._memcache.get(memcache_context, "departments"):
            return result

        departments = self.get_departments_uncached()
        # since we are not filtering departments, we can cache the entire list
        self._memcache.set(
            memcache_context,
            "departments",
            departments,
            ttl=cache_context.ttl,
        )
        return departments

    @tracer.start_as_current_span("HierarchyIntegration.get_departments_uncached")
    def get_departments_uncached(self) -> list[Department]:
        try:
            response = self._cms_nav_client.get_merchandised_departments()
        except (s4f.errors.TimeoutError, s4f.errors.CommunicationError):
            raise DownstreamTimeoutError("cms-navigation-service")

        return [
            Department(id=dept.department_id, name=dept.name, slug=dept.slug)
            for dept in response.departments
        ]

    def get_department_by_slug(self, department_slug: str) -> Department | None:
        """Find a given department (or `None`) for the given slug"""
        departments = self.get_departments()
        return next((d for d in departments if d.slug == department_slug), None)

    def get_department_by_id(self, department_id: int) -> Department | None:
        """Find the list of departments which match the given list of IDs"""
        departments = self.get_departments()
        return next((d for d in departments if d.id == department_id), None)

    def get_node_path(self, node: Node) -> list[Node]:
        if isinstance(node, Department):
            return [node]
        parent_id = node.parent_id
        department_id = node.department_id
        if parent_id:
            cat = self.get_category_by_id(parent_id)
            if cat:
                return [*self.get_node_path(cat), node]
        else:
            dept = self.get_department_by_id(department_id)
            if dept:
                return [dept, node]
        return []
