from __future__ import annotations

from dataclasses import dataclass
from typing import Final, TypedDict

from data_go_youth_policy_mcp.models import ErrorPayload, ErrorResponse, JsonObject, SuccessResponse


class CodeGroupPayload(TypedDict):
    label: str
    codes: dict[str, str]


class CodeReferencePayload(TypedDict):
    groups: dict[str, CodeGroupPayload]


class CodeGroupLookupPayload(TypedDict):
    group: str
    label: str
    codes: dict[str, str]


class CodeLookupPayload(TypedDict):
    group: str
    label: str
    code: str
    name: str


@dataclass(frozen=True, slots=True)
class CodeGroup:
    label: str
    codes: dict[str, str]


YOUTH_POLICY_CODE_REFERENCE: Final[dict[str, CodeGroup]] = {
    "pvsnInstGroupCd": CodeGroup(
        label="제공기관그룹코드",
        codes={"0054001": "중앙부처", "0054002": "지자체"},
    ),
    "plcyPvsnMthdCd": CodeGroup(
        label="정책제공방법코드",
        codes={
            "0042001": "인프라 구축",
            "0042002": "프로그램",
            "0042003": "직접대출",
            "0042004": "공공기관",
            "0042005": "계약(위탁운영)",
            "0042006": "보조금",
            "0042007": "대출보증",
            "0042008": "공적보험",
            "0042009": "조세지출",
            "0042010": "바우처",
            "0042011": "정보제공",
            "0042012": "경제적 규제",
            "0042013": "기타",
        },
    ),
    "plcyAprvSttsCd": CodeGroup(
        label="정책승인상태코드",
        codes={"0044001": "신청", "0044002": "승인", "0044003": "반려", "0044004": "임시저장"},
    ),
    "aplyPrdSeCd": CodeGroup(
        label="신청기간구분코드",
        codes={"0057001": "특정기간", "0057002": "상시", "0057003": "마감"},
    ),
    "bizPrdSeCd": CodeGroup(
        label="사업기간구분코드",
        codes={"0056001": "특정기간", "0056002": "기타"},
    ),
    "mrgSttsCd": CodeGroup(
        label="결혼상태코드",
        codes={"0055001": "기혼", "0055002": "미혼", "0055003": "제한없음"},
    ),
    "earnCndSeCd": CodeGroup(
        label="소득조건구분코드",
        codes={"0043001": "무관", "0043002": "연소득", "0043003": "기타"},
    ),
    "plcyMajorCd": CodeGroup(
        label="정책전공요건코드",
        codes={
            "0011001": "인문계열",
            "0011002": "사회계열",
            "0011003": "상경계열",
            "0011004": "이학계열",
            "0011005": "공학계열",
            "0011006": "예체능계열",
            "0011007": "농산업계열",
            "0011008": "기타",
            "0011009": "제한없음",
        },
    ),
    "jobCd": CodeGroup(
        label="정책취업요건코드",
        codes={
            "0013001": "재직자",
            "0013002": "자영업자",
            "0013003": "미취업자",
            "0013004": "프리랜서",
            "0013005": "일용근로자",
            "0013006": "(예비)창업자",
            "0013007": "단기근로자",
            "0013008": "영농종사자",
            "0013009": "기타",
            "0013010": "제한없음",
        },
    ),
    "schoolCd": CodeGroup(
        label="정책학력요건코드",
        codes={
            "0049001": "고졸 미만",
            "0049002": "고교 재학",
            "0049003": "고졸 예정",
            "0049004": "고교 졸업",
            "0049005": "대학 재학",
            "0049006": "대학 예정",
            "0049007": "대학 졸업",
            "0049008": "석·박사",
            "0049009": "기타",
            "0049010": "제한없음",
        },
    ),
    "sbizCd": CodeGroup(
        label="정책특화요건코드",
        codes={
            "0014001": "중소기업",
            "0014002": "여성",
            "0014003": "기초생활수급자",
            "0014004": "한부모가정",
            "0014005": "장애인",
            "0014006": "농업인",
            "0014007": "군인",
            "0014008": "지역인재",
            "0014009": "기타",
            "0014010": "제한없음",
        },
    ),
    "lclsfNm": CodeGroup(
        label="정책대분류명",
        codes={"1": "일자리", "2": "주거", "3": "교육", "4": "복지문화", "5": "참여권리"},
    ),
    "mclsfNm": CodeGroup(
        label="정책중분류명",
        codes={
            "1": "취업",
            "2": "재직자",
            "3": "창업",
            "4": "주택 및 거주지",
            "5": "기숙사",
            "6": "전월세 및 주거급여 지원",
            "7": "미래역량강화",
            "8": "교육비지원",
            "9": "온라인교육",
            "10": "취약계층 및 금융지원",
            "11": "건강",
            "12": "예술인지원",
            "13": "문화활동",
            "14": "청년참여",
            "15": "정책인프라구축",
            "16": "청년국제교류",
            "17": "권익보호",
        },
    ),
    "plcyKywdNm": CodeGroup(
        label="정책키워드명",
        codes={
            "1": "대출",
            "2": "보조금",
            "3": "바우처",
            "4": "금리혜택",
            "5": "교육지원",
            "6": "맞춤형상담서비스",
            "7": "인턴",
            "8": "배달",
            "9": "중소기업",
            "10": "청년가장",
            "11": "장기미취업청년",
            "12": "공공임대주택",
            "13": "신용회복",
            "14": "육아",
            "15": "출산",
            "16": "해외진출",
            "17": "주거지원",
        },
    ),
}


def get_code_reference(group: str | None = None, code: str | None = None) -> JsonObject:
    if group is None:
        payload: CodeReferencePayload = {
            "groups": {
                group_name: {"label": code_group.label, "codes": code_group.codes}
                for group_name, code_group in YOUTH_POLICY_CODE_REFERENCE.items()
            }
        }
        return SuccessResponse(data=payload).model_dump()

    code_group = YOUTH_POLICY_CODE_REFERENCE.get(group)
    if code_group is None:
        return ErrorResponse(
            error=ErrorPayload(
                code="unknown_code_group",
                message="Unknown youth policy code group.",
                details={"group": group, "available_groups": list(YOUTH_POLICY_CODE_REFERENCE)},
            )
        ).model_dump()

    if code is None:
        group_payload: CodeGroupLookupPayload = {
            "group": group,
            "label": code_group.label,
            "codes": code_group.codes,
        }
        return SuccessResponse(data=group_payload).model_dump()

    code_name = code_group.codes.get(code)
    if code_name is None:
        return ErrorResponse(
            error=ErrorPayload(
                code="unknown_code",
                message="Unknown youth policy code in the requested group.",
                details={"group": group, "code": code, "available_codes": list(code_group.codes)},
            )
        ).model_dump()

    code_payload: CodeLookupPayload = {
        "group": group,
        "label": code_group.label,
        "code": code,
        "name": code_name,
    }
    return SuccessResponse(data=code_payload).model_dump()
