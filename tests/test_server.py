from __future__ import annotations

from dataclasses import dataclass
from types import TracebackType

import pytest

from data_go_youth_policy_mcp import server
from data_go_youth_policy_mcp.models import (
    BasicPlanAssignmentParams,
    BasicPlanFocusAssessmentParams,
    ContentParams,
    PolicyWayParams,
    RawParams,
    SpaceParams,
    SuccessResponse,
    YouthPolicyDetailParams,
    YouthPolicySearchParams,
)


@dataclass(slots=True)
class FakeClient:
    api_key: str | None = None

    async def __aenter__(self) -> FakeClient:
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        return None

    async def search(self, search_params: YouthPolicySearchParams) -> SuccessResponse:
        return SuccessResponse(data=search_params.to_query_params())

    async def get_detail(self, detail_params: YouthPolicyDetailParams) -> SuccessResponse:
        return SuccessResponse(data=detail_params.to_query_params())

    async def fetch_raw(self, params: RawParams) -> SuccessResponse:
        return SuccessResponse(data=params)

    async def get_basic_plan_focus_assessments(
        self,
        params: BasicPlanFocusAssessmentParams,
    ) -> SuccessResponse:
        return SuccessResponse(data=params.to_query_params())

    async def get_policy_ways(self, params: PolicyWayParams) -> SuccessResponse:
        return SuccessResponse(data=params.to_query_params())

    async def get_contents(self, params: ContentParams) -> SuccessResponse:
        return SuccessResponse(data=params.to_query_params())

    async def get_basic_plan_assignments(
        self,
        params: BasicPlanAssignmentParams,
    ) -> SuccessResponse:
        return SuccessResponse(data=params.to_query_params())

    async def get_spaces(self, params: SpaceParams) -> SuccessResponse:
        return SuccessResponse(data=params.to_query_params())


@pytest.mark.asyncio
async def test_youth_policy_search_returns_mapped_params(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.youth_policy_search(
        page_num=3,
        page_size=30,
        keyword_names=["채용", "구직"],
        policy_name="청년취업",
        region_codes=["11000"],
        large_categories=["일자리"],
        medium_categories=["취업지원"],
    )

    assert response["ok"] is True
    assert response["data"] == {
        "pageNum": 3,
        "pageSize": 30,
        "pageType": "1",
        "rtnType": "json",
        "plcyKywdNm": "채용,구직",
        "plcyNm": "청년취업",
        "zipCd": "11000",
        "lclsfNm": "일자리",
        "mclsfNm": "취업지원",
    }


@pytest.mark.asyncio
async def test_youth_policy_get_detail_uses_official_detail_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.youth_policy_get_detail("R202401010001")

    assert response == {
        "ok": True,
        "data": {
            "pageType": "2",
            "plcyNo": "R202401010001",
            "rtnType": "json",
        },
    }


@pytest.mark.asyncio
async def test_youth_policy_get_raw_calls_client(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.youth_policy_get_raw({"query": "청년", "display": 5})

    assert response == {"ok": True, "data": {"query": "청년", "display": 5}}


@pytest.mark.asyncio
async def test_youth_policy_search_validation_error() -> None:
    response = await server.youth_policy_search(page_num=0)

    assert response["ok"] is False
    assert response["error"]["code"] == "invalid_search_params"


@pytest.mark.asyncio
async def test_basic_plan_focus_assessment_tool_returns_mapped_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.ontong_basic_plan_focus_assessment_get_raw(return_type="xml")

    assert response == {"ok": True, "data": {"rtnType": "xml"}}


@pytest.mark.asyncio
async def test_policy_way_tool_returns_mapped_params(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.ontong_policy_way_get_raw()

    assert response == {"ok": True, "data": {"rtnType": "json"}}


@pytest.mark.asyncio
async def test_content_tool_returns_mapped_params(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.ontong_content_get_raw(
        page_num=2,
        page_size=50,
        page_type="2",
        post_sn="100",
        post_section_code="notice",
    )

    assert response == {
        "ok": True,
        "data": {
            "pageNum": 2,
            "pageSize": 50,
            "pageType": "2",
            "pstSn": "100",
            "pstSeCd": "notice",
            "rtnType": "json",
        },
    }


@pytest.mark.asyncio
async def test_basic_plan_assignment_tool_returns_mapped_params(
    monkeypatch: pytest.MonkeyPatch,
) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.ontong_basic_plan_assignment_get_raw(return_type="json")

    assert response == {"ok": True, "data": {"rtnType": "json"}}


@pytest.mark.asyncio
async def test_space_tool_returns_mapped_params(monkeypatch: pytest.MonkeyPatch) -> None:
    monkeypatch.setattr(server, "YouthPolicyApiClient", FakeClient)

    response = await server.ontong_space_get_raw(
        page_num=3,
        page_size=20,
        page_type="1",
        city_code="11",
        district_code="11000",
        place_sn="200",
        place_type="center",
    )

    assert response == {
        "ok": True,
        "data": {
            "pageNum": 3,
            "pageSize": 20,
            "pageType": "1",
            "ctpvCd": "11",
            "sggCd": "11000",
            "plcSn": "200",
            "plcType": "center",
            "rtnType": "json",
        },
    }


@pytest.mark.asyncio
async def test_content_tool_validation_error() -> None:
    response = await server.ontong_content_get_raw(page_num=0)

    assert response["ok"] is False
    assert response["error"]["code"] == "invalid_content_params"
