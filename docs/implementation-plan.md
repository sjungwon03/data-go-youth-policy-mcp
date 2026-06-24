# data-go-youth-policy-mcp 작업 계획

## 목표

온통청년 OPEN API를 읽기 전용 MCP 서버로 제공한다.

현재 범위:

- 청년정책 목록 검색
- 청년정책 상세 조회
- 청년정책 raw 조회
- 기본계획중점과제 raw 조회
- 기본계획정책방향 raw 조회
- 청년콘텐츠 raw 조회
- 기본계획과제 raw 조회
- 청년센터 raw 조회
- 페이지네이션
- 공식 문서에 있는 주요 필터 전달
- 응답 정규화는 실 API 응답 구조 확인 후 진행

## 안 할 것

- 쓰기/수정/삭제 도구 없음.
- API 문서에 없는 파라미터 추측 구현 없음.
- 새 프레임워크 도입 없음.
- 호출 제한/캐시/복잡한 재시도는 실제 제한 확인 전까지 보류.
- caller가 전달한 `apiKeyNm`으로 서버 소유 API key를 덮어쓰지 않음.

## 제안 도구 설계

### `youth_policy_search`

청년정책 목록을 검색한다.

입력과 내부 매핑은 `docs/api-reference.md`를 기준으로 한다. 핵심 매핑:

- `page_num` → `pageNum`
- `page_size` → `pageSize`
- `return_type` → `rtnType`
- env `YOUTH_POLICY_API_KEY` → `apiKeyNm`
- 목록 조회 고정값 `pageType=1`
- 상세 조회 고정값 `pageType=2`, `policy_no` → `plcyNo`

### `youth_policy_get_raw`

문서/실응답 확인용 raw 호출 도구.

입력:

- `params: Record<string, string | number | boolean>`

제약:

- `apiKeyNm` 직접 입력 금지. 서버가 환경변수에서 주입.
- 읽기 전용 GET만 허용.

### 추가 raw 조회 도구

- `ontong_basic_plan_focus_assessment_get_raw` → `getBscPlanFcsAsmt`
- `ontong_policy_way_get_raw` → `getPolicyWay`
- `ontong_content_get_raw` → `getContent`
- `ontong_basic_plan_assignment_get_raw` → `getBscPlanAsm`
- `ontong_space_get_raw` → `getSpace`

기본계획과제는 공식 문서 URL 표와 요청 예시의 endpoint 표기가 다르다. 현재 구현은 URL 표의 `getBscPlanAsm`을 따른다.

## 파일 구조

```text
README.md
pyproject.toml
.env.example
src/data_go_youth_policy_mcp/
  __init__.py
  api_client.py
  models.py
  server.py
tests/
  test_api_client.py
  test_server.py
docs/
  api-reference.md
  reference-repo-notes.md
  implementation-plan.md
```

현재 repo 는 단일 MCP 서버 repo 이므로, 참고 repo 의 `src/<api-name>/` 다중 패키지 구조를 그대로 복사하지 않고 단일 패키지 구조로 단순화한다.

## 구현 단계

1. 프로젝트 스캐폴딩
   - `pyproject.toml`
   - `.env.example`
   - Python package 디렉터리
   - console script entrypoint

2. API client
   - `YOUTH_POLICY_API_KEY` 로드
   - `httpx.AsyncClient` context manager
   - `getPlcy` GET wrapper
   - HTTP/API 오류 메시지 정리

3. 모델
   - 검색 입력 모델
   - raw response 모델은 우선 dict 기반
   - 실응답 확인 후 정책 요약 모델 정규화

4. MCP server
   - `FastMCP`
   - `youth_policy_search`
   - `youth_policy_get_detail`
   - `youth_policy_get_raw`
   - 추가 OPEN API raw 조회 tools
   - `stdio` 실행

5. 테스트
   - 인증키 누락 테스트
   - 파라미터 매핑 테스트
   - `httpx.MockTransport` 기반 성공/오류 테스트
   - MCP tool 함수 smoke test

6. 문서
   - 설치
   - 환경변수
   - Claude/OpenCode MCP 설정 예시
   - 도구 설명/예시

7. 실 API 확인
   - 발급키로 샘플 호출
   - JSON/XML 응답 차이 확인
   - 응답 필드명 반영
   - 필요 시 `youth_policy_get_detail` 추가

## 이슈 분해안

### Issue 1 — 프로젝트 스캐폴딩

- `pyproject.toml`, `.env.example`, package skeleton 작성
- 실행 entrypoint 추가
- README 기본 설치/실행 문서 작성

### Issue 2 — 온통청년 API client 구현

- 인증키 로드
- `getPlcy` 호출
- 파라미터 매핑
- HTTP 오류 처리
- 단위 테스트

### Issue 3 — MCP tools 구현

- `FastMCP` 서버 구성
- `youth_policy_search` 구현
- `youth_policy_get_detail` 구현
- `youth_policy_get_raw` 구현
- 추가 OPEN API raw 조회 tools 구현
- tool smoke test

### Issue 4 — 실 API 응답 검증 및 출력 정규화

- 발급키로 실제 호출
- JSON/XML 응답 확인
- 응답 필드 모델 정리
- README 예시 업데이트

## 진행 전 필요한 것

- 온통청년 API 인증키.
- GitHub issue 생성 권한 확인.
