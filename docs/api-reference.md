# 청년정책 API 참고

Source: 온통청년 > 이용안내 > 오픈(OPEN) API 제공목록

## 현재 MCP 범위

| API | Method | URL |
| --- | --- | --- |
| 청년정책 | GET | `https://www.youthcenter.go.kr/go/ythip/getPlcy` |

기본계획중점과제, 기본계획정책방향, 청년콘텐츠, 기본계획과제, 청년센터 API는 이 MCP 범위에 포함하지 않는다. 각 API는 별도 인증/설정이 필요하므로 후속 작업에서 별도 MCP로 분리한다.

## 인증

- 청년정책 API 발급키 필요.
- 인증키 파라미터명: `apiKeyNm`
- 구현 환경변수명: `YOUTH_POLICY_API_KEY`
- MCP tool 입력으로 받은 `apiKeyNm`은 무시하고 서버 환경변수 값을 주입한다.

## 청년정책 요청 파라미터

| 이름 | 타입 | 필수 | 설명 |
| --- | --- | --- | --- |
| `apiKeyNm` | String | Y | 발급받은 인증키 |
| `pageNum` | Number | N | 페이지번호 |
| `pageSize` | Number | N | 페이지사이즈 |
| `pageType` | String | N | 화면유형: `1` 목록, `2` 상세 |
| `plcyNo` | String | N | 정책번호 |
| `rtnType` | String | N | 호출문서: `xml`, `json` |
| `plcyKywdNm` | String | N | 정책키워드명. 요청형식: `키워드1,키워드2,...` |
| `plcyExplnCn` | String | N | 정책설명 |
| `plcyNm` | String | N | 정책명 |
| `zipCd` | String | N | 법정시군구코드 5자리. 요청형식: `11000,11330,...` |
| `lclsfNm` | String | N | 정책대분류명. 요청형식: `대분류1,대분류2,...` |
| `mclsfNm` | String | N | 정책중분류명. 요청형식: `중분류1,중분류2,...` |

## MCP 입력 매핑

### `youth_policy_search`

| MCP 입력 | upstream 파라미터 |
| --- | --- |
| `page_num` | `pageNum` |
| `page_size` | `pageSize` |
| `return_type` | `rtnType` |
| 고정값 `1` | `pageType` |
| `keyword_names` | `plcyKywdNm` comma join |
| `description` | `plcyExplnCn` |
| `policy_name` | `plcyNm` |
| `region_codes` | `zipCd` comma join |
| `large_categories` | `lclsfNm` comma join |
| `medium_categories` | `mclsfNm` comma join |

### `youth_policy_get_detail`

| MCP 입력 | upstream 파라미터 |
| --- | --- |
| 고정값 `2` | `pageType` |
| `policy_no` | `plcyNo` |
| `return_type` | `rtnType` |

## 출력 필드

공식 문서에 노출된 `<youthPolicyList>` 하위 필드:

- `plcyNo`: 정책번호
- `bscPlanCycl`: 기본계획차수
- `bscPlanPlcyWayNo`: 기본계획정책방향번호
- `bscPlanFcsAsmtNo`: 기본계획중점과제번호
- `bscPlanAsmtNo`: 기본계획과제번호
- `pvsnInstGroupCd`: 제공기관그룹코드
- `plcyPvsnMthdCd`: 정책제공방법코드
- `plcyAprvSttsCd`: 정책승인상태코드
- `plcyNm`: 정책명
- `plcyKywdNm`: 정책키워드명
- `plcyExplnCn`: 정책설명내용
- `lclsfNm`: 정책대분류명
- `mclsfNm`: 정책중분류명
- `plcySprtCn`: 정책지원내용
- `sprvsnInstCd`: 주관기관코드
- `sprvsnInstCdNm`: 주관기관코드명
- `sprvsnInstPicNm`: 주관기관담당자명
- `operInstCd`: 운영기관코드
- `operInstCdNm`: 운영기관코드명
- `operInstPicNm`: 운영기관담당자명
- `sprtSclLmtYn`: 지원규모제한여부
- `aplyPrdSeCd`: 신청기간구분코드
- `bizPrdSeCd`: 사업기간구분코드
- `bizPrdBgngYmd`: 사업기간시작일자
- `bizPrdEndYmd`: 사업기간종료일자
- `bizPrdEtcCn`: 사업기간기타내용
- `plcyAplyMthdCn`: 정책신청방법내용
- `srngMthdCn`: 심사방법내용
- `aplyUrlAddr`: 신청URL주소
- `sbmsnDcmntCn`: 제출서류내용
- `etcMttrCn`: 기타사항내용
- `refUrlAddr1`: 참고URL주소
- `refUrlAddr2`: 참고URL주소
- `sprtSclCnt`: 지원규모수
- `sprtArvlSeqYn`: 지원도착순서여부
- `sprtTrgtMinAge`: 지원대상최소연령
- `sprtTrgtMaxAge`: 지원대상최대연령
- `sprtTrgtAgeLmtYn`: 지원대상연령제한여부
- `mrgSttsCd`: 결혼상태코드
- `earnCndSeCd`: 소득조건구분코드
- `earnMinAmt`: 소득최소금액
- `earnMaxAmt`: 소득최대금액
- `earnEtcCn`: 소득기타내용
- `addAplyQlfcCndCn`: 추가신청자격조건내용
- `ptcpPrpTrgtCn`: 참여제한대상내용
- `inqCnt`: 조회수
- `rgtrInstCd`: 등록자기관코드
- `rgtrInstCdNm`: 등록자기관코드명
- `rgtrUpInstCd`: 등록자상위기관코드
- `rgtrUpInstCdNm`: 등록자상위기관코드명
- `rgtrHghrkInstCd`: 등록자최상위기관코드
- `rgtrHghrkInstCdNm`: 등록자최상위기관코드명
- `zipCd`: 정책거주지역코드
- `plcyMajorCd`: 정책전공요건코드
- `jobCd`: 정책취업요건코드
- `schoolCd`: 정책학력요건코드
- `aplyYmd`: 신청기간
- `frstRegDt`: 최초등록일시
- `lastMdfcnDt`: 최종수정일시
- `sBizCd`: 정책특화요건코드

## 요청 예시

```text
https://www.youthcenter.go.kr/go/ythip/getPlcy?apiKeyNm=testKey&pageNum=1&pageSize=10&rtnType=json
```

## 아직 확인 필요

- JSON 실응답 최상위 구조
- 오류 payload 형식
- 호출 제한 수치
- `pageSize` 공식 최대값
- 다른 온통청년 API의 별도 인증/설정 방식
