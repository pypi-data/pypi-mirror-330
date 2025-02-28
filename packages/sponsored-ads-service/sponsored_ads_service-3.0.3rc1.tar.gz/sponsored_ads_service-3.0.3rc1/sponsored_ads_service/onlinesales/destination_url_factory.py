from sponsored_ads_service.configuration import SponsoredAdsConfig
from sponsored_ads_service.integrations.catalogue_aggregator import CatalogueAggregatorIntegration
from sponsored_ads_service.models.link_data import ActionType
from sponsored_ads_service.onlinesales.models import Display, Product
from sponsored_ads_service.validators.link_validator import LinkValidator


class DestinationUrlFactory:
    def __init__(
        self,
        config: SponsoredAdsConfig,
        catalogue_integration: CatalogueAggregatorIntegration,
        link_validator: LinkValidator,
    ) -> None:
        self._config = config
        self._catalogue_integration = catalogue_integration
        self._link_validator = link_validator

        self._hostname = self._config.get_link_data_hostname()

    def from_display_ad(self, display_ad: Display) -> str | None:
        if display_ad.destination_url:
            return display_ad.destination_url
        return self._from_products(display_ad.products)

    def _from_products(self, products: list[Product]) -> str | None:
        if len(products) == 1:
            return self._build_product_display_link_data(products[0])

        link = self._create_plids_destination_link(products)

        # Validate that the given link is a valid search link, and sanitise any tags
        # from the link before sending to frontends.
        validated_link = self._link_validator.validate(link=link, action=ActionType.SEARCH)
        return validated_link.parameters["url"]

    def _build_product_display_link_data(self, product: Product) -> str | None:
        """
        Link Generation for Product Display Ad click destination URLs:

        Create a link to the Product Display Page for the ad's product
        """
        productline_relative_url = self._catalogue_integration.get_relative_url_for_plid(
            product.plid
        )
        if not productline_relative_url:
            return None
        link = f"https://{self._hostname}{productline_relative_url}"
        link_data = self._link_validator.validate(link=link, action=ActionType.PRODUCT)
        return link_data.parameters["url"]

    def _create_plids_destination_link(self, products: list[Product]) -> str:
        """
        Create a search URL that contains an `Id` filter for the given products.

        The maximum number of products (PLIDs) to include in the filter list is defined
        by `SPONSORED_DISPLAY_SEARCH_FILTERS_PLID_LIMIT`.
        """

        plid_limit = self._config.get_sponsored_display_search_filters_plid_limit()
        slice_len = min(plid_limit, len(products))

        linked_plids: list[str] = []
        for product in products[:slice_len]:
            linked_plids.append(str(product.plid))

        id_filter = "|".join(linked_plids)

        return f"https://{self._hostname}/all?filter=Id:{id_filter}"
