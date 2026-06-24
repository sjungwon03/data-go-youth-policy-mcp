# data-go-youth-policy-mcp

온통청년 청년정책 API를 읽기 전용 MCP 도구로 노출하는 Python FastMCP 서버입니다.

## 공식 문서

- [공공데이터포털 청년정책 API](https://www.data.go.kr/data/15143273/openapi.do)
- [온통청년 오픈API 안내](https://www.youthcenter.go.kr/cmnFooter/openapiIntro/oaiDoc)

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

## LLM 코딩 에이전트용 설정 지침

LangChain 또는 LangGraph 프로젝트에서 LLM 코딩 에이전트가 이 README만 보고 설정해야 한다면 아래 순서로 진행하면 됩니다.

### 1. 이 MCP 서버 준비

이 저장소를 로컬에 clone하고 의존성을 설치합니다.

```bash
git clone https://github.com/sjungwon03/data-go-youth-policy-mcp.git
cd data-go-youth-policy-mcp
uv sync
```

청년정책 API key는 이 MCP 서버 프로세스의 환경변수로만 전달합니다.

```bash
export YOUTH_POLICY_API_KEY=발급받은_API_키
```

API key를 코드, prompt, LangChain state, LangGraph checkpoint에 저장하지 마세요.

### 2. LangChain/LangGraph 프로젝트 의존성 추가

호출하는 프로젝트에는 MCP adapter를 설치합니다.

```bash
uv add langchain-mcp-adapters
```

`pip` 기반 프로젝트라면 다음을 사용합니다.

```bash
python -m pip install langchain-mcp-adapters
```

### 3. MCP client 설정

LangChain/LangGraph 프로젝트 코드에서 `MultiServerMCPClient`를 사용해 이 서버를 stdio subprocess로 등록합니다.

```python
import os

from langchain_mcp_adapters.client import MultiServerMCPClient

client = MultiServerMCPClient(
    {
        "data-go-youth-policy": {
            "transport": "stdio",
            "command": "uv",
            "args": [
                "--directory",
                "/ABSOLUTE/PATH/TO/data-go-youth-policy-mcp",
                "run",
                "python",
                "-m",
                "data_go_youth_policy_mcp.server",
            ],
            "env": {
                "YOUTH_POLICY_API_KEY": os.environ["YOUTH_POLICY_API_KEY"],
            },
        }
    }
)
```

`/ABSOLUTE/PATH/TO/data-go-youth-policy-mcp`는 이 저장소의 절대 경로로 바꿉니다. `YOUTH_POLICY_API_KEY`가 설정되지 않았으면 애플리케이션 시작 단계에서 먼저 환경변수를 주입하세요.

### 4. LangChain agent에서 tools 로드

```python
tools = await client.get_tools()
```

로드되는 도구는 다음 세 개입니다.

- `youth_policy_search`
- `youth_policy_get_detail`
- `youth_policy_get_raw`

에이전트에게는 다음 규칙을 system prompt 또는 developer prompt에 넣는 것을 권장합니다.

```text
청년정책 정보가 필요하면 data-go-youth-policy MCP tools를 사용한다.
목록 검색은 youth_policy_search, 정책번호 상세 조회는 youth_policy_get_detail을 사용한다.
응답 구조 확인이 필요한 경우에만 youth_policy_get_raw를 사용한다.
apiKeyNm은 절대 직접 전달하지 않는다. 서버가 YOUTH_POLICY_API_KEY를 apiKeyNm으로 주입한다.
기본계획중점과제, 기본계획정책방향, 청년콘텐츠, 기본계획과제, 청년센터 API는 이 MCP의 범위가 아니다.
```

### 5. LangGraph node에서 사용

LangGraph에서는 graph 초기화 시 MCP tools를 한 번 로드한 뒤 tool node 또는 agent node에 전달합니다.

```python
import os

from langchain_mcp_adapters.client import MultiServerMCPClient


async def load_youth_policy_tools():
    client = MultiServerMCPClient(
        {
            "data-go-youth-policy": {
                "transport": "stdio",
                "command": "uv",
                "args": [
                    "--directory",
                    "/ABSOLUTE/PATH/TO/data-go-youth-policy-mcp",
                    "run",
                    "python",
                    "-m",
                    "data_go_youth_policy_mcp.server",
                ],
                "env": {"YOUTH_POLICY_API_KEY": os.environ["YOUTH_POLICY_API_KEY"]},
            }
        }
    )
    return await client.get_tools()
```

### 6. 빠른 동작 확인

LLM agent에 연결하기 전, tool 목록을 먼저 확인합니다.

```python
tools = await client.get_tools()
print([tool.name for tool in tools])
```

예상 결과:

```python
["youth_policy_search", "youth_policy_get_detail", "youth_policy_get_raw"]
```

API key가 없거나 잘못된 경우 서버는 시작 또는 호출 시 오류를 반환합니다. 실제 API 응답 구조는 아직 정규화하지 않으므로 agent 코드는 `ok`가 `true`인지 확인한 뒤 `data`를 읽어야 합니다.

## 도구

### `youth_policy_search`

온통청년 청년정책 목록을 검색합니다.

이 도구는 청년층의 다양한 문제와 필요를 바탕으로 수립된 정책정보를 조회합니다. 청년층과의 소통, 설문조사, 공청회, 청년자문단 등 여러 의견 수렴 과정을 통해 마련된 청년정책 중에서 사용자가 지정한 조건에 맞는 정책 목록을 찾을 때 사용합니다.

정책명, 정책키워드, 정책설명, 법정시군구코드, 정책대분류명, 정책중분류명 조건을 조합해 검색할 수 있습니다. 결과에는 공식 API가 제공하는 정책번호, 기본계획 차수, 기본계획정책방향번호, 중점과제 번호, 정책명, 정책키워드, 정책설명, 주관기관코드, 주관기관담당자명 등의 청년정책 정보가 포함됩니다.

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

정책번호로 청년정책 상세 정보를 조회합니다. 내부적으로 `pageType=2`와 `plcyNo`를 사용합니다.

`youth_policy_search` 결과에서 확인한 정책번호(`plcyNo`)를 입력하면 단일 정책의 상세 정보를 가져옵니다. 특정 정책의 지원내용, 신청방법, 심사방법, 제출서류, 사업기간, 신청기간, 지원대상 조건, 주관기관/운영기관 정보, 참고 URL 등을 확인할 때 사용합니다.

입력:

- `policy_no: string` -> `plcyNo`
- `return_type?: "json" | "xml"` -> `rtnType`, 기본값 `json`

### `youth_policy_get_raw`

실 API 응답 스키마 확인을 위해 `getPlcy`에 원시 query parameter를 전달합니다.

공식 문서와 실제 응답 구조를 대조하거나 아직 MCP 입력 모델로 감싸지 않은 파라미터를 시험할 때 사용하는 저수준 도구입니다. 일반적인 정책 검색은 `youth_policy_search`, 정책 상세 조회는 `youth_policy_get_detail`을 우선 사용하고, 응답 필드 확인이나 schema 탐색이 필요할 때만 이 도구를 사용합니다.

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
