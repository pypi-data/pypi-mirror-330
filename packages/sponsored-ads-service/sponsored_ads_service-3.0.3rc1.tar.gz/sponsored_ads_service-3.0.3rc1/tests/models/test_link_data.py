from cms_navigation_client import navigation_service_pb2 as pb

from sponsored_ads_service.models.link_data import ActionType, Context, LinkData


def test_link_data_from_pb():
    link_data = LinkData(
        action=ActionType.PAGE,
        context=Context.BROWSER,
        parameters={"testParamOne": "valueOne", "testParamTwo": "valueTwo"},
        seo_info_found=False,
    )

    p = pb.LinkData(
        action="page",
        context="browser",
        parameters="""{"testParamOne": "valueOne", "testParamTwo": "valueTwo"}""",
        seo_info_found=False,
    )

    assert LinkData.from_pb(p) == link_data


def test_link_data_to_dict():
    link_data = LinkData(
        action=ActionType.PRODUCT,
        context=Context.NAVIGATION,
        parameters={"testParamOne": "valueOne", "testParamTwo": "valueTwo"},
        seo_info_found=False,
    )

    assert link_data.to_dict() == {
        "action": "product",
        "context": "navigation",
        "parameters": {"testParamOne": "valueOne", "testParamTwo": "valueTwo"},
        "seo_info_found": False,
    }
