from __future__ import annotations

import httpx
import pytest

from data_go_youth_policy_mcp.api_client import (
    API_KEY_PARAM,
    BASIC_PLAN_ASSIGNMENT_ENDPOINT,
    BASIC_PLAN_FOCUS_ASSESSMENT_ENDPOINT,
    CONTENT_ENDPOINT,
    POLICY_WAY_ENDPOINT,
    SPACE_ENDPOINT,
    MissingApiKeyError,
    YouthPolicyApiClient,
)
from data_go_youth_policy_mcp.models import (
    BasicPlanAssignmentParams,
    BasicPlanFocusAssessmentParams,
    ContentParams,
    PolicyWayParams,
    SpaceParams,
    YouthPolicySearchParams,
)


def test_missing_api_key_raises_clear_error(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.delenv("YOUTH_POLICY_API_KEY", raising=False)

    with pytest.raises(MissingApiKeyError, match="YOUTH_POLICY_API_KEY"):
        YouthPolicyApiClient()


def test_search_params_map_to_upstream_names() -> None:
    params = YouthPolicySearchParams(
        page_num=2,
        page_size=20,
        return_type="json",
        keyword_names=("채용", "구직"),
        description="취업 지원",
        policy_name="청년취업",
        region_codes=("11000", "11680"),
        large_categories=("일자리",),
        medium_categories=("취업지원",),
    )

    mapped = params.to_query_params()

    assert mapped == {
        "pageNum": 2,
        "pageSize": 20,
        "pageType": "1",
        "rtnType": "json",
        "plcyKywdNm": "채용,구직",
        "plcyExplnCn": "취업 지원",
        "plcyNm": "청년취업",
        "zipCd": "11000,11680",
        "lclsfNm": "일자리",
        "mclsfNm": "취업지원",
    }


def test_additional_params_map_to_upstream_names() -> None:
    assert BasicPlanFocusAssessmentParams().to_query_params() == {"rtnType": "json"}
    assert PolicyWayParams(return_type="xml").to_query_params() == {"rtnType": "xml"}
    assert BasicPlanAssignmentParams().to_query_params() == {"rtnType": "json"}

    assert ContentParams(
        page_num=2,
        page_size=50,
        page_type="2",
        post_sn="100",
        post_section_code="notice",
    ).to_query_params() == {
        "pageNum": 2,
        "pageSize": 50,
        "pageType": "2",
        "pstSn": "100",
        "pstSeCd": "notice",
        "rtnType": "json",
    }

    assert SpaceParams(
        page_num=3,
        page_size=20,
        page_type="1",
        city_code="11",
        district_code="11000",
        place_sn="200",
        place_type="center",
    ).to_query_params() == {
        "pageNum": 3,
        "pageSize": 20,
        "pageType": "1",
        "ctpvCd": "11",
        "sggCd": "11000",
        "plcSn": "200",
        "plcType": "center",
        "rtnType": "json",
    }


@pytest.mark.asyncio
async def test_fetch_raw_injects_env_key_and_ignores_caller_key() -> None:
    captured_params: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        captured_params.update(dict(request.url.params))
        return httpx.Response(200, json={"result": "ok"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        async with YouthPolicyApiClient(api_key="server-key", http_client=http_client) as client:
            response = await client.fetch_raw({API_KEY_PARAM: "caller-key", "query": "청년"})

    assert response.ok is True
    assert response.data == {"result": "ok"}
    assert captured_params[API_KEY_PARAM] == "server-key"
    assert captured_params["query"] == "청년"


@pytest.mark.parametrize(
    ("method_name", "params", "endpoint"),
    [
        (
            "get_basic_plan_focus_assessments",
            BasicPlanFocusAssessmentParams(return_type="json"),
            BASIC_PLAN_FOCUS_ASSESSMENT_ENDPOINT,
        ),
        ("get_policy_ways", PolicyWayParams(return_type="json"), POLICY_WAY_ENDPOINT),
        ("get_contents", ContentParams(post_sn="100"), CONTENT_ENDPOINT),
        (
            "get_basic_plan_assignments",
            BasicPlanAssignmentParams(return_type="json"),
            BASIC_PLAN_ASSIGNMENT_ENDPOINT,
        ),
        ("get_spaces", SpaceParams(place_sn="200"), SPACE_ENDPOINT),
    ],
)
@pytest.mark.asyncio
async def test_additional_client_methods_use_official_endpoints_and_inject_key(
    method_name: str,
    params: (
        BasicPlanFocusAssessmentParams
        | PolicyWayParams
        | ContentParams
        | BasicPlanAssignmentParams
        | SpaceParams
    ),
    endpoint: str,
) -> None:
    captured_url = ""
    captured_params: dict[str, str] = {}

    def handler(request: httpx.Request) -> httpx.Response:
        nonlocal captured_url
        captured_url = str(request.url.copy_with(query=None))
        captured_params.update(dict(request.url.params))
        return httpx.Response(200, json={"result": "ok"})

    transport = httpx.MockTransport(handler)
    async with httpx.AsyncClient(transport=transport) as http_client:
        async with YouthPolicyApiClient(api_key="server-key", http_client=http_client) as client:
            method = getattr(client, method_name)
            response = await method(params)

    assert response.ok is True
    assert captured_url == endpoint
    assert captured_params[API_KEY_PARAM] == "server-key"


@pytest.mark.asyncio
async def test_http_status_error_returns_structured_error() -> None:
    transport = httpx.MockTransport(lambda request: httpx.Response(503, request=request))

    async with httpx.AsyncClient(transport=transport) as http_client:
        async with YouthPolicyApiClient(api_key="server-key", http_client=http_client) as client:
            response = await client.fetch_raw({"query": "청년"})

    assert response.ok is False
    assert response.error.code == "upstream_http_error"
    assert response.error.details["status_code"] == 503
    assert "server-key" not in str(response.error.details)
    assert API_KEY_PARAM not in str(response.error.details)
