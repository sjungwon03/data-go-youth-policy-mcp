from __future__ import annotations

from typing import Literal, TypeAlias

from pydantic import BaseModel, ConfigDict, Field, JsonValue

JsonObject: TypeAlias = dict[str, JsonValue]
RawParamValue: TypeAlias = str | int | float | bool
RawParams: TypeAlias = dict[str, RawParamValue]
QueryParams: TypeAlias = dict[str, str | int]
ReturnType: TypeAlias = Literal["json", "xml"]


class YouthPolicySearchParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    page_num: int = Field(default=1, ge=1)
    page_size: int = Field(default=10, ge=1)
    return_type: ReturnType = "json"
    keyword_names: tuple[str, ...] = Field(default=())
    description: str | None = None
    policy_name: str | None = None
    region_codes: tuple[str, ...] = Field(default=())
    large_categories: tuple[str, ...] = Field(default=())
    medium_categories: tuple[str, ...] = Field(default=())

    def to_query_params(self) -> QueryParams:
        params: QueryParams = {
            "pageNum": self.page_num,
            "pageSize": self.page_size,
            "pageType": "1",
            "rtnType": self.return_type,
        }

        if self.keyword_names:
            params["plcyKywdNm"] = ",".join(self.keyword_names)
        if self.description:
            params["plcyExplnCn"] = self.description
        if self.policy_name:
            params["plcyNm"] = self.policy_name
        if self.region_codes:
            params["zipCd"] = ",".join(self.region_codes)
        if self.large_categories:
            params["lclsfNm"] = ",".join(self.large_categories)
        if self.medium_categories:
            params["mclsfNm"] = ",".join(self.medium_categories)

        return params


class YouthPolicyDetailParams(BaseModel):
    model_config = ConfigDict(frozen=True)

    policy_no: str = Field(min_length=1)
    return_type: ReturnType = "json"

    def to_query_params(self) -> QueryParams:
        return {
            "pageType": "2",
            "plcyNo": self.policy_no,
            "rtnType": self.return_type,
        }


class ErrorPayload(BaseModel):
    model_config = ConfigDict(frozen=True)

    code: str
    message: str
    details: JsonObject = Field(default_factory=dict)


class SuccessResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    ok: Literal[True] = True
    data: JsonValue


class ErrorResponse(BaseModel):
    model_config = ConfigDict(frozen=True)

    ok: Literal[False] = False
    error: ErrorPayload


ApiResponse: TypeAlias = SuccessResponse | ErrorResponse
