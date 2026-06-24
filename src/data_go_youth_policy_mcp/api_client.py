from __future__ import annotations

import json
import os
from dataclasses import dataclass
from types import TracebackType
from typing import Final

import httpx
from dotenv import load_dotenv

from data_go_youth_policy_mcp.models import (
    ApiResponse,
    ErrorPayload,
    ErrorResponse,
    JsonValue,
    QueryParams,
    RawParams,
    SuccessResponse,
    YouthPolicyDetailParams,
    YouthPolicySearchParams,
)

API_KEY_ENV: Final = "YOUTH_POLICY_API_KEY"
API_KEY_PARAM: Final = "apiKeyNm"
ONTONG_BASE_URL: Final = "https://www.youthcenter.go.kr/go/ythip"
YOUTH_POLICY_ENDPOINT: Final = f"{ONTONG_BASE_URL}/getPlcy"


@dataclass(frozen=True, slots=True)
class MissingApiKeyError(RuntimeError):
    env_name: str

    def __str__(self) -> str:
        return f"Missing required environment variable: {self.env_name}"


class YouthPolicyApiClient:
    def __init__(
        self,
        api_key: str | None = None,
        http_client: httpx.AsyncClient | None = None,
    ) -> None:
        load_dotenv()
        resolved_api_key = api_key or os.getenv(API_KEY_ENV)
        if not resolved_api_key:
            raise MissingApiKeyError(API_KEY_ENV)

        self._api_key = resolved_api_key
        self._http_client = http_client
        self._owns_client = http_client is None

    async def __aenter__(self) -> YouthPolicyApiClient:
        if self._http_client is None:
            self._http_client = httpx.AsyncClient(timeout=30.0)
        return self

    async def __aexit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        if self._owns_client and self._http_client is not None:
            await self._http_client.aclose()

    async def search(self, search_params: YouthPolicySearchParams) -> ApiResponse:
        return await self.fetch_raw(search_params.to_query_params())

    async def get_detail(self, detail_params: YouthPolicyDetailParams) -> ApiResponse:
        return await self.fetch_raw(detail_params.to_query_params())

    async def fetch_raw(self, params: RawParams | QueryParams) -> ApiResponse:
        return await self._fetch_endpoint(YOUTH_POLICY_ENDPOINT, params)

    async def _fetch_endpoint(self, endpoint: str, params: RawParams | QueryParams) -> ApiResponse:
        request_params: RawParams | QueryParams = {
            key: value for key, value in params.items() if key != API_KEY_PARAM
        }
        request_params[API_KEY_PARAM] = self._api_key

        client = self._require_client()
        try:
            response = await client.get(endpoint, params=request_params)
            response.raise_for_status()
        except httpx.HTTPStatusError as error:
            return ErrorResponse(
                error=ErrorPayload(
                    code="upstream_http_error",
                    message="OnTong API returned an HTTP error.",
                    details={
                        "status_code": error.response.status_code,
                        "endpoint": endpoint,
                    },
                )
            )
        except httpx.RequestError:
            return ErrorResponse(
                error=ErrorPayload(
                    code="upstream_request_error",
                    message="OnTong API request failed before receiving a response.",
                    details={"endpoint": endpoint},
                )
            )

        return SuccessResponse(data=_decode_response(response))

    def _require_client(self) -> httpx.AsyncClient:
        if self._http_client is None:
            raise RuntimeError("Use YouthPolicyApiClient as an async context manager.")
        return self._http_client


def _decode_response(response: httpx.Response) -> JsonValue:
    try:
        decoded = response.json()
    except json.JSONDecodeError:
        return response.text
    return decoded
