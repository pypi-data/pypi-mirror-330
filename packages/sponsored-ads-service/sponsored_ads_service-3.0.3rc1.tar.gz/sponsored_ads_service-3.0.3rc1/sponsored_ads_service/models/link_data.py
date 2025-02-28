from __future__ import annotations

import json
from dataclasses import dataclass
from enum import Enum, StrEnum
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from cms_navigation_client import navigation_service_pb2 as pb


class ActionType(StrEnum):
    SEARCH = "search"
    PAGE = "page"
    DEALS = "deals"
    PRODUCT = "product"
    NOT_FOUND = "notfound"
    EXTERNAL = "external"


class Context(Enum):
    NAVIGATION = "navigation"
    BROWSER = "browser"


@dataclass
class LinkData:
    action: ActionType
    context: Context
    parameters: dict
    seo_info_found: bool = False

    def to_dict(self) -> dict:
        return {
            "action": self.action.value,
            "context": self.context.value,
            "parameters": self.parameters,
            "seo_info_found": self.seo_info_found,
        }

    @staticmethod
    def from_pb(p: pb.LinkData) -> LinkData:
        return LinkData(
            action=ActionType(p.action),
            context=Context(p.context),
            parameters=json.loads(p.parameters),
            seo_info_found=p.seo_info_found,
        )
