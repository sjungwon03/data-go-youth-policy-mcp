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
    """Search OnTong youth policies with pagination and official filters."""
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
    """Get a single OnTong youth policy by policy number."""
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
    """Call the youth policy endpoint with raw query params for schema discovery."""
    async with YouthPolicyApiClient() as client:
        response = await client.fetch_raw(params or {})
    return response.model_dump()


def main() -> None:
    mcp.run(transport="stdio")


if __name__ == "__main__":
    main()
