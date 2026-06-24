# `Koomook/data-go-mcp-servers` 참고 메모

Source: <https://github.com/Koomook/data-go-mcp-servers>

조사 기준 HEAD: `dd27f99490400b31fa14f96045a138fa217580a4`

## 구조

- 루트 `pyproject.toml` 이 `uv` workspace 를 관리한다.
- workspace 멤버는 `src/*`.
- 각 API 서버는 `src/<api-name>/` 아래 독립 패키지로 둔다.
- Python 패키지는 `data_go_mcp/<api_name_underscore>/` 형태.

## 런타임 / 프레임워크

- Python 기반.
- MCP SDK: `mcp[cli]`
- 서버: `FastMCP`
- HTTP 클라이언트: `httpx.AsyncClient`
- 모델: `pydantic`
- 환경변수: `python-dotenv`
- 실행 transport: `stdio`

## 반복 패턴

### 서버

- `from mcp.server.fastmcp import FastMCP`
- `mcp = FastMCP("...")`
- 도구는 `@mcp.tool()` 로 등록.
- 엔트리포인트에서 `mcp.run(transport="stdio")`.

### API 클라이언트

- API key 는 환경변수에서 읽는다.
- 없으면 `ValueError`.
- `httpx.AsyncClient(timeout=30.0)` 사용.
- async context manager (`__aenter__`, `__aexit__`) 패턴.
- 응답은 `response.raise_for_status()` 로 HTTP 오류 처리.

### 오류 처리

- 클라이언트 레벨: 인증키 누락은 명시적 `ValueError`.
- 도구 레벨: 일부 서버는 `{"error": str(e), ...}` 형태로 오류를 구조화.
- 새 서버도 LLM이 복구할 수 있게 오류 메시지에 필요한 조치(키 확인, 파라미터 수정, 호출 제한 확인)를 포함한다.

## 참고할 파일 경로

- `README.md`: 전체 프로젝트 설명, 설치/테스트/개발 명령.
- `pyproject.toml`: uv workspace, lint/test/build 설정.
- `CONTRIBUTING.md`: 수동 서버 추가 흐름.
- `TEMPLATE_USAGE.md`: 템플릿 사용법.
- `docs/creating-new-mcp-server.md`: 새 서버 생성 절차.
- `scripts/create_mcp_server.py`: 대화형 서버 생성기.
- `template/cookiecutter.json`: 템플릿 변수.
- `template/{{cookiecutter.api_name}}/pyproject.toml`: 서버별 패키징/엔트리포인트.
- `template/{{cookiecutter.api_name}}/data_go_mcp/{{cookiecutter.api_name_underscore}}/api_client.py`: API client 템플릿.
- `template/{{cookiecutter.api_name}}/data_go_mcp/{{cookiecutter.api_name_underscore}}/models.py`: 모델 템플릿.
- `template/{{cookiecutter.api_name}}/data_go_mcp/{{cookiecutter.api_name_underscore}}/server.py`: MCP server 템플릿.
- `src/nps-business-enrollment/...`: API key + FastMCP 기본 패턴.
- `src/nts-business-verification/...`: 여러 tool + request flow 예시.
- `src/pps-narajangteo/...`: helper + multiple tools 예시.

## 새 서버 최소 생성 경로

1. `template/` 구조를 `src/youth-policy/` 로 복사 또는 cookiecutter 생성.
2. 패키지명은 `data-go-mcp.youth-policy` 계열로 둔다.
3. Python module 은 `data_go_mcp/youth_policy/` 로 둔다.
4. `api_client.py` 에 온통청년 API 호출 로직을 넣는다.
5. `models.py` 에 검색 입력/정책 출력 모델을 둔다.
6. `server.py` 에 읽기 전용 MCP tools 를 등록한다.
7. `README.md`, `.env.example`, tests 를 추가한다.
