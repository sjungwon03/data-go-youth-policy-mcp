# 온통청년 OPEN API 참고

Source: 온통청년 > 이용안내 > 오픈(OPEN) API 제공목록

## 확인된 엔드포인트

| API | Method | URL |
| --- | --- | --- |
| 청년정책 | GET | `https://www.youthcenter.go.kr/go/ythip/getPlcy` |
| 기본계획중점과제 | GET | `https://www.youthcenter.go.kr/go/ythip/getBscPlanFcsAsmt` |
| 기본계획정책방향 | GET | `https://www.youthcenter.go.kr/go/ythip/getPolicyWay` |
| 청년콘텐츠 | GET | `https://www.youthcenter.go.kr/go/ythip/getContent` |
| 기본계획과제 | GET | `https://www.youthcenter.go.kr/go/ythip/getBscPlanAsm` |
| 청년센터 | GET | `https://www.youthcenter.go.kr/go/ythip/getSpace` |

기본계획과제는 문서의 URL 표에는 `getBscPlanAsm`, 요청 예시에는 `getBscPlanAsmt`로 표기되어 있다. 구현은 URL 표의 `getBscPlanAsm`을 사용한다.

## 인증

- 온통청년 OPEN API 발급키 필요.
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

### 추가 원시 조회 도구

| MCP tool | upstream endpoint | MCP 입력 | upstream 파라미터 |
| --- | --- | --- | --- |
| `ontong_basic_plan_focus_assessment_get_raw` | `getBscPlanFcsAsmt` | `return_type` | `rtnType` |
| `ontong_policy_way_get_raw` | `getPolicyWay` | `return_type` | `rtnType` |
| `ontong_basic_plan_assignment_get_raw` | `getBscPlanAsm` | `return_type` | `rtnType` |
| `ontong_content_get_raw` | `getContent` | `page_num` | `pageNum` |
| `ontong_content_get_raw` | `getContent` | `page_size` | `pageSize` |
| `ontong_content_get_raw` | `getContent` | `page_type` | `pageType` |
| `ontong_content_get_raw` | `getContent` | `post_sn` | `pstSn` |
| `ontong_content_get_raw` | `getContent` | `post_section_code` | `pstSeCd` |
| `ontong_content_get_raw` | `getContent` | `return_type` | `rtnType` |
| `ontong_space_get_raw` | `getSpace` | `page_num` | `pageNum` |
| `ontong_space_get_raw` | `getSpace` | `page_size` | `pageSize` |
| `ontong_space_get_raw` | `getSpace` | `page_type` | `pageType` |
| `ontong_space_get_raw` | `getSpace` | `city_code` | `ctpvCd` |
| `ontong_space_get_raw` | `getSpace` | `district_code` | `sggCd` |
| `ontong_space_get_raw` | `getSpace` | `place_sn` | `plcSn` |
| `ontong_space_get_raw` | `getSpace` | `place_type` | `plcType` |
| `ontong_space_get_raw` | `getSpace` | `return_type` | `rtnType` |

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

### 기본계획중점과제

- `bscPlanCycl`: 기본계획차수
- `bscPlanPlcyWayNo`: 기본계획정책방향번호
- `bscPlanFcsAsmtNo`: 기본계획중점과제번호
- `fcsAsmtNm`: 중점과제명

### 기본계획정책방향

- `bscPlanCycl`: 기본계획차수
- `bscPlanPlcyWayNo`: 기본계획정책방향번호
- `wayNm`: 정책방향명

### 청년콘텐츠

- `bbsSn`: 게시판일련번호
- `pstSn`: 게시물일련번호
- `pstSeSn`: 게시물구분일련번호
- `pstTtl`: 게시물제목
- `pstWholCn`: 게시물전체내용
- `pstUrlAddr`: 게시물URL주소
- `atchFile`: 첨부파일
- `thumnamilYn`: 썸네일여부
- `pstSeNm`: 게시물구분명
- `frstRgtrNm`: 최초등록자명
- `frstRegDt`: 최초등록일시
- `lastMdfrNm`: 최종수정자명
- `lastMdfcnDt`: 최종수정일시
- `pstInqCnt`: 게시물조회수

### 기본계획과제

- `bscPlanCycl`: 기본계획차수
- `bscPlanFcsAsmtNo`: 기본계획중점과제번호
- `asmtNm`: 과제명
- `bscPlanAsmtNo`: 기본계획과제번호

### 청년센터

- `cntrSn`: 센터일련번호
- `cntrNm`: 센터명
- `cntrTelno`: 센터전화번호
- `cntrAddr`: 센터주소
- `cntrDaddr`: 센터상세주소
- `cntrUrlAddr`: 센터URL주소
- `stdgCtpvCd`: 법정동시도코드
- `stdgCtpvCdNm`: 법정동시도코드명
- `stdgSggCd`: 법정동시군구코드
- `stdgSggCdNm`: 법정동시군구코드명

## 요청 예시

```text
https://www.youthcenter.go.kr/go/ythip/getPlcy?apiKeyNm=testKey&pageNum=1&pageSize=10&rtnType=json
```

## 아직 확인 필요

- JSON 실응답 최상위 구조
- 오류 payload 형식
- 호출 제한 수치
- `pageSize` 공식 최대값
- 기본계획과제 endpoint 표기 불일치: `getBscPlanAsm` vs `getBscPlanAsmt`
