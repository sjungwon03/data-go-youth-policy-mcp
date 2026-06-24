# data-go-youth-policy-mcp

온통청년 청년정책 API를 읽기 전용 MCP 도구로 노출하는 Python FastMCP 서버입니다.

## 현재 범위

- 청년정책 목록 검색: `youth_policy_search`
- 청년정책 상세 조회: `youth_policy_get_detail`
- 청년정책 API 원시 호출: `youth_policy_get_raw`
- `stdio` transport 실행
- 테스트는 `httpx.MockTransport`와 monkeypatch만 사용하며 실제 API 키나 네트워크 호출이 필요하지 않습니다.

기본계획중점과제, 기본계획정책방향, 청년콘텐츠, 기본계획과제, 청년센터 API는 각각 별도 설정/인증 범위를 전제로 후속 작업에서 별도 MCP로 다룹니다. 이 서버는 청년정책 API(`getPlcy`)만 호출합니다.

아직 실 API 응답 구조가 환경별로 확인되지 않았으므로 도구 출력은 정규화 모델이 아니라 다음 구조를 사용합니다.

```json
{"ok": true, "data": {}}
```

오류는 다음 구조로 반환합니다.

```json
{"ok": false, "error": {"code": "...", "message": "...", "details": {}}}
```

## 설치

권장 설치 방식은 `uv`입니다.

```bash
uv sync --extra dev
```

`pip`를 사용하는 경우:

```bash
python -m pip install -e ".[dev]"
```

## 환경변수

청년정책 API 인증키를 설정합니다.

```bash
cp .env.example .env
```

```bash
YOUTH_POLICY_API_KEY=발급받은_API_키
```

서버는 이 값을 upstream 요청 파라미터 `apiKeyNm`으로 주입합니다. 도구 입력으로 전달된 `apiKeyNm`은 서버 소유 키를 덮어쓸 수 없습니다.

## 실행

```bash
data-go-youth-policy-mcp
```

또는:

```bash
python -m data_go_youth_policy_mcp.server
```

## MCP 설정 예시

```json
{
  "mcpServers": {
    "data-go-youth-policy": {
      "command": "data-go-youth-policy-mcp",
      "env": {
        "YOUTH_POLICY_API_KEY": "발급받은_API_키"
      }
    }
  }
}
```

개발 중 editable install 없이 실행하려면 `command`를 `python`으로 두고 `args`를 사용할 수 있습니다.

```json
{
  "mcpServers": {
    "data-go-youth-policy": {
      "command": "python",
      "args": ["-m", "data_go_youth_policy_mcp.server"],
      "env": {
        "PYTHONPATH": "src",
        "YOUTH_POLICY_API_KEY": "발급받은_API_키"
      }
    }
  }
}
```

## 도구

### `youth_policy_search`

청년정책 목록을 검색합니다.

입력:

- `page_num?: number` -> `pageNum`, 기본값 `1`
- `page_size?: number` -> `pageSize`, 기본값 `10`
- `return_type?: "json" | "xml"` -> `rtnType`, 기본값 `json`
- `keyword_names?: string[]` -> `plcyKywdNm`
- `description?: string` -> `plcyExplnCn`
- `policy_name?: string` -> `plcyNm`
- `region_codes?: string[]` -> `zipCd`
- `large_categories?: string[]` -> `lclsfNm`
- `medium_categories?: string[]` -> `mclsfNm`

예시:

```json
{
  "page_num": 1,
  "page_size": 10,
  "return_type": "json",
  "policy_name": "청년취업",
  "keyword_names": ["채용", "구직"],
  "region_codes": ["11000", "11680"]
}
```

### `youth_policy_get_detail`

정책번호로 청년정책 상세를 조회합니다. 내부적으로 `pageType=2`와 `plcyNo`를 사용합니다.

입력:

- `policy_no: string` -> `plcyNo`
- `return_type?: "json" | "xml"` -> `rtnType`, 기본값 `json`

### `youth_policy_get_raw`

실 API 응답 스키마 확인을 위해 `getPlcy`에 원시 query parameter를 전달합니다.

입력:

- `params?: object`

제약:

- `apiKeyNm`은 직접 지정해도 무시됩니다.
- 호출 대상은 `https://www.youthcenter.go.kr/go/ythip/getPlcy`로 고정됩니다.

## 개발 검증

```bash
uv run python -m compileall src tests
uv run pytest
uv run ruff check .
uv run ruff format --check .
```

## 남은 확인 사항

- 실제 JSON 응답을 받기 위한 추가 파라미터 필요 여부
- 정확한 응답 필드명과 오류 payload 형식
- 공식 `pageSize` 최대값
- 다른 온통청년 API를 각각 별도 MCP로 분리할 때 필요한 인증/설정 방식
