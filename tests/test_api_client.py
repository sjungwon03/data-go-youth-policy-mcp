from __future__ import annotations

import httpx
import pytest

from data_go_youth_policy_mcp.api_client import (
    API_KEY_PARAM,
    MissingApiKeyError,
    YouthPolicyApiClient,
)
from data_go_youth_policy_mcp.models import YouthPolicySearchParams


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
