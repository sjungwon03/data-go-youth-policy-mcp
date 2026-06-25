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
- `sbizCd`: 정책특화요건코드

## 실 API 응답 구조 확인 결과

2026-06-25에 발급키를 환경변수 `YOUTH_POLICY_API_KEY`로만 주입해 live 호출을 검증했다. 인증키는 파일, 로그, 이슈 본문에 저장하지 않았다.

### 목록 조회

`pageNum=1`, `pageSize=1`, `rtnType=json`, `pageType=1` 기준으로 `youth_policy_search`가 성공했다.

최상위 JSON 구조:

```text
resultCode
resultMessage
result
```

`result` 하위 구조:

```text
pagging
youthPolicyList
```

`pagging` 하위 필드:

```text
pageNum
pageSize
totCount
```

### 상세 조회

목록 조회에서 얻은 `plcyNo`로 `pageType=2` 상세 조회를 호출했고 `youth_policy_get_detail`이 성공했다.

최상위 JSON 구조:

```text
resultCode
resultMessage
result
```

`result` 하위 구조:

```text
youthPolicyList
```

상세 응답의 `youthPolicyList` 첫 항목에서 확인한 필드명:

```text
addAplyQlfcCndCn
aplyPrdSeCd
aplyUrlAddr
aplyYmd
bizPrdBgngYmd
bizPrdEndYmd
bizPrdEtcCn
bizPrdSeCd
bscPlanAsmtNo
bscPlanCycl
bscPlanFcsAsmtNo
bscPlanPlcyWayNo
earnCndSeCd
earnEtcCn
earnMaxAmt
earnMinAmt
etcMttrCn
frstRegDt
inqCnt
jobCd
lastMdfcnDt
lclsfNm
mclsfNm
mrgSttsCd
operInstCd
operInstCdNm
operInstPicNm
plcyAplyMthdCn
plcyAprvSttsCd
plcyExplnCn
plcyKywdNm
plcyMajorCd
plcyNm
plcyNo
plcyPvsnMthdCd
plcySprtCn
ptcpPrpTrgtCn
pvsnInstGroupCd
refUrlAddr1
refUrlAddr2
rgtrHghrkInstCd
rgtrHghrkInstCdNm
rgtrInstCd
rgtrInstCdNm
rgtrUpInstCd
rgtrUpInstCdNm
sbizCd
sbmsnDcmntCn
schoolCd
sprtArvlSeqYn
sprtSclCnt
sprtSclLmtYn
sprtTrgtAgeLmtYn
sprtTrgtMaxAge
sprtTrgtMinAge
sprvsnInstCd
sprvsnInstCdNm
sprvsnInstPicNm
srngMthdCn
zipCd
```

## 코드값 참고

공식 문서와 제공된 코드표 기준의 주요 코드값이다. 이 MCP는 현재 응답을 정규화하지 않으므로, 코드 해석이 필요한 클라이언트는 아래 표를 참고해 표시명을 매핑한다.

### 기관/제공/승인/기간/조건 코드

#### `pvsnInstGroupCd` 제공기관그룹코드

| 코드 | 코드내용 |
| --- | --- |
| `0054001` | 중앙부처 |
| `0054002` | 지자체 |

#### `plcyPvsnMthdCd` 정책제공방법코드

| 코드 | 코드내용 |
| --- | --- |
| `0042001` | 인프라 구축 |
| `0042002` | 프로그램 |
| `0042003` | 직접대출 |
| `0042004` | 공공기관 |
| `0042005` | 계약(위탁운영) |
| `0042006` | 보조금 |
| `0042007` | 대출보증 |
| `0042008` | 공적보험 |
| `0042009` | 조세지출 |
| `0042010` | 바우처 |
| `0042011` | 정보제공 |
| `0042012` | 경제적 규제 |
| `0042013` | 기타 |

#### `plcyAprvSttsCd` 정책승인상태코드

| 코드 | 코드내용 |
| --- | --- |
| `0044001` | 신청 |
| `0044002` | 승인 |
| `0044003` | 반려 |
| `0044004` | 임시저장 |

#### `aplyPrdSeCd` 신청기간구분코드

| 코드 | 코드내용 |
| --- | --- |
| `0057001` | 특정기간 |
| `0057002` | 상시 |
| `0057003` | 마감 |

#### `bizPrdSeCd` 사업기간구분코드

| 코드 | 코드내용 |
| --- | --- |
| `0056001` | 특정기간 |
| `0056002` | 기타 |

#### `mrgSttsCd` 결혼상태코드

| 코드 | 코드내용 |
| --- | --- |
| `0055001` | 기혼 |
| `0055002` | 미혼 |
| `0055003` | 제한없음 |

#### `earnCndSeCd` 소득조건구분코드

| 코드 | 코드내용 |
| --- | --- |
| `0043001` | 무관 |
| `0043002` | 연소득 |
| `0043003` | 기타 |

### 대상 요건 코드

#### `plcyMajorCd` 정책전공요건코드

| 코드 | 코드내용 |
| --- | --- |
| `0011001` | 인문계열 |
| `0011002` | 사회계열 |
| `0011003` | 상경계열 |
| `0011004` | 이학계열 |
| `0011005` | 공학계열 |
| `0011006` | 예체능계열 |
| `0011007` | 농산업계열 |
| `0011008` | 기타 |
| `0011009` | 제한없음 |

#### `jobCd` 정책취업요건코드

| 코드 | 코드내용 |
| --- | --- |
| `0013001` | 재직자 |
| `0013002` | 자영업자 |
| `0013003` | 미취업자 |
| `0013004` | 프리랜서 |
| `0013005` | 일용근로자 |
| `0013006` | (예비)창업자 |
| `0013007` | 단기근로자 |
| `0013008` | 영농종사자 |
| `0013009` | 기타 |
| `0013010` | 제한없음 |

#### `schoolCd` 정책학력요건코드

| 코드 | 코드내용 |
| --- | --- |
| `0049001` | 고졸 미만 |
| `0049002` | 고교 재학 |
| `0049003` | 고졸 예정 |
| `0049004` | 고교 졸업 |
| `0049005` | 대학 재학 |
| `0049006` | 대학 예정 |
| `0049007` | 대학 졸업 |
| `0049008` | 석·박사 |
| `0049009` | 기타 |
| `0049010` | 제한없음 |

#### `sbizCd` 정책특화요건코드

| 코드 | 코드내용 |
| --- | --- |
| `0014001` | 중소기업 |
| `0014002` | 여성 |
| `0014003` | 기초생활수급자 |
| `0014004` | 한부모가정 |
| `0014005` | 장애인 |
| `0014006` | 농업인 |
| `0014007` | 군인 |
| `0014008` | 지역인재 |
| `0014009` | 기타 |
| `0014010` | 제한없음 |

### 정책 분류명

#### `lclsfNm` 정책대분류명

| 번호 | 정책대분류명 |
| --- | --- |
| 1 | 일자리 |
| 2 | 주거 |
| 3 | 교육 |
| 4 | 복지문화 |
| 5 | 참여권리 |

#### `mclsfNm` 정책중분류명

| 번호 | 정책중분류명 |
| --- | --- |
| 1 | 취업 |
| 2 | 재직자 |
| 3 | 창업 |
| 4 | 주택 및 거주지 |
| 5 | 기숙사 |
| 6 | 전월세 및 주거급여 지원 |
| 7 | 미래역량강화 |
| 8 | 교육비지원 |
| 9 | 온라인교육 |
| 10 | 취약계층 및 금융지원 |
| 11 | 건강 |
| 12 | 예술인지원 |
| 13 | 문화활동 |
| 14 | 청년참여 |
| 15 | 정책인프라구축 |
| 16 | 청년국제교류 |
| 17 | 권익보호 |

#### `plcyKywdNm` 정책키워드명

| 번호 | 정책키워드명 |
| --- | --- |
| 1 | 대출 |
| 2 | 보조금 |
| 3 | 바우처 |
| 4 | 금리혜택 |
| 5 | 교육지원 |
| 6 | 맞춤형상담서비스 |
| 7 | 인턴 |
| 8 | 배달 |
| 9 | 중소기업 |
| 10 | 청년가장 |
| 11 | 장기미취업청년 |
| 12 | 공공임대주택 |
| 13 | 신용회복 |
| 14 | 육아 |
| 15 | 출산 |
| 16 | 해외진출 |
| 17 | 주거지원 |

## 요청 예시

```text
https://www.youthcenter.go.kr/go/ythip/getPlcy?apiKeyNm=testKey&pageNum=1&pageSize=10&rtnType=json
```

## 아직 확인 필요

- 호출 제한 수치
- `pageSize` 공식 최대값
- 다른 온통청년 API의 별도 인증/설정 방식
