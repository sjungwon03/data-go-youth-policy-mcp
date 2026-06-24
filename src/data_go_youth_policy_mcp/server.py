from __future__ import annotations

import json

from mcp.server.fastmcp import FastMCP
from pydantic import ValidationError

from data_go_youth_policy_mcp.api_client import YouthPolicyApiClient
from data_go_youth_policy_mcp.models import (
    ErrorPayload,
    ErrorResponse,
    JsonObject,
    RawParams,
    YouthPolicyDetailParams,
    YouthPolicySearchParams,
)

mcp = FastMCP("data-go-youth-policy-mcp")


@mcp.tool()
async def youth_policy_search(
    page_num: int = 1,
    page_size: int = 10,
    return_type: str = "json",
    keyword_names: list[str] | None = None,
    description: str | None = None,
    policy_name: str | None = None,
    region_codes: list[str] | None = None,
    large_categories: list[str] | None = None,
    medium_categories: list[str] | None = None,
) -> JsonObject:
    """온통청년 청년정책 목록을 검색합니다.

    청년층의 다양한 문제와 필요를 조사하고, 청년층과의 소통,
    설문조사, 공청회, 청년자문단 등을 통해 수렴된 의견을 바탕으로
    수립된 정책정보를 조회합니다. 정책명, 정책키워드, 정책설명,
    법정시군구코드, 정책대분류명, 정책중분류명 조건을 사용할 수
    있습니다. 결과에는 정책번호, 정책명, 정책키워드, 정책설명,
    기본계획 차수, 기본계획정책방향번호, 중점과제 번호,
    주관기관코드, 주관기관담당자명 등 공식 API가 제공하는
    청년정책 필드가 포함됩니다.
    """
    try:
        search_params = YouthPolicySearchParams(
            page_num=page_num,
            page_size=page_size,
            return_type=return_type,
            keyword_names=tuple(keyword_names or ()),
            description=description,
            policy_name=policy_name,
            region_codes=tuple(region_codes or ()),
            large_categories=tuple(large_categories or ()),
            medium_categories=tuple(medium_categories or ()),
        )
    except ValidationError as error:
        return ErrorResponse(
            error=ErrorPayload(
                code="invalid_search_params",
                message="Search parameters failed validation.",
                details={"errors": json.loads(error.json())},
            )
        ).model_dump()

    async with YouthPolicyApiClient() as client:
        response = await client.search(search_params)
    return response.model_dump()


@mcp.tool()
async def youth_policy_get_detail(policy_no: str, return_type: str = "json") -> JsonObject:
    """정책번호로 온통청년 청년정책 상세 정보를 조회합니다.

    `youth_policy_search` 결과의 정책번호(`plcyNo`)를 사용해 단일
    정책의 상세 내용을 가져옵니다. 정책명, 정책키워드, 정책설명,
    지원내용, 신청방법, 주관기관/운영기관 정보, 신청기간, 대상 조건,
    참고 URL 등 공식 청년정책 API가 제공하는 상세 필드를 확인할 때
    사용합니다.
    """
    try:
        detail_params = YouthPolicyDetailParams(policy_no=policy_no, return_type=return_type)
    except ValidationError as error:
        return ErrorResponse(
            error=ErrorPayload(
                code="invalid_detail_params",
                message="Detail parameters failed validation.",
                details={"errors": json.loads(error.json())},
            )
        ).model_dump()

    async with YouthPolicyApiClient() as client:
        response = await client.get_detail(detail_params)
    return response.model_dump()


@mcp.tool()
async def youth_policy_get_raw(params: RawParams | None = None) -> JsonObject:
    """청년정책 API에 원시 query parameter를 전달해 응답 구조를 확인합니다.

    공식 `getPlcy` endpoint의 신규 파라미터나 실제 응답 schema를
    탐색할 때 사용합니다. 서버가 `YOUTH_POLICY_API_KEY`를
    `apiKeyNm`으로 주입하므로 호출자는 인증키를 직접 전달하지
    않아야 하며, 입력된 `apiKeyNm`은 무시됩니다.
    """
    async with YouthPolicyApiClient() as client:
        response = await client.fetch_raw(params or {})
    return response.model_dump()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
