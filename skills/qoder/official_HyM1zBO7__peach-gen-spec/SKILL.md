---
name: peach-gen-spec
description: |
  신규 기능 요구사항과 ui-proto를 분석하여 team-dev/team-e2e가 추가 기획 질문 없이 실행할 수 있는 확정 Spec을 생성하는 스킬.
  "Spec 만들어줘", "신규 기능 기획", "요구사항 정리" 키워드로 트리거.
  ui-proto가 있으면 proto=<경로>로 화면 기획안에서 Spec을 추출한다.
  기존 기능 분석이 필요하면 peach-doc-feature를 사용한다.
model: opus
---

# Spec 생성 스킬

신규 기능을 **Spec 주도 개발**로 진행하기 위해 단일 Spec 파일을 생성한다.

목표 흐름:

```text
peach-team-ui-proto
→ peach-gen-spec proto=<ui-proto 태스크 경로>
→ peach-gen-db spec=<생성된 Spec 경로>
→ peach-team-dev spec=<생성된 Spec 경로>
→ peach-team-e2e spec=<생성된 Spec 경로> [proto=<ui-proto 태스크 경로>]
```

## 핵심 원칙

- Spec은 구현 기준의 Source of Truth다.
- PRD는 고려하지 않는다. 입력 문서가 있더라도 원천 자료일 뿐이며, 구현 기준은 최종 Spec에 명시된 내용만 따른다.
- 표준 산출물은 **단일 `.md` 파일**이다.
- Spec은 `team-dev`와 `team-e2e`가 추가 기획 질문 없이 진행할 수 있을 만큼 확정한다.
- `team-*`가 알아서 처리할 테스트 코드, selector, fixture, suite 내부 구현은 Spec에 쓰지 않는다.
- 대신 TEST_ID별 요구사항, 완료 기준, Backend TDD 기준, Store/Contract 기준, UI 기준, E2E 시나리오를 충분히 구체화한다.
- 상태 코드는 운영 보고용으로 만들지 않는다. 사용자 보고는 평문(`확정`, `구현완료`, `검증완료`, `차단`)을 우선한다.
- 의무 매트릭스는 만들지 않는다. 권한/상태/오류/외부의존성은 산문 1차, 분기와 규칙이 많아 표가 더 명확할 때만 표로 확장한다.
- FK(Foreign Key)는 생성하지 않는다. 참조 무결성은 애플리케이션에서 처리한다.
- `test-data`는 복사 정답지가 아니라 기준 골격이다. 후속 `gen-*`/`team-*` 스킬은 Bounded Autonomy 안에서 도메인에 맞게 적응할 수 있다.
- Spec 분량 목표는 250~450줄이다. 작으면 200줄 내외도 허용하되, TDD/E2E 기준은 생략하지 않는다.
- 사용자가 **수정 전 토론**을 요청하면 문서를 바로 고치지 않고 `분석 → 권장안 → 사용자 확정 → 문서 반영` 순서로 진행한다. AI는 질문을 남발하지 않고 합리적 기본안을 먼저 제시하되, DB 구조·상태 전이·외부 연동·권한 흐름처럼 되돌리기 어려운 판단은 사용자 확정을 받는다.
- TDD/E2E 기준은 모든 요구사항에 빈칸 없이 채우지 않는다. team-dev/team-e2e가 자율 보완할 수 있도록 **핵심 비즈니스 전이, 저장 결과, 권한·소유 차단, 대표 실패 케이스**만 명시한다.
- E2E는 **핵심 사용자 흐름만** 적는다. 시작 데이터는 시나리오/suite가 직접 준비하고, 같은 흐름이 반복되면 **suite 조합**을 우선한다. 단위 시나리오 작성 규칙(단일 책임/재활용/독립 실행)은 `peach-e2e-scenario`, suite 통합 규칙은 `peach-e2e-suite`가 SoT다.
- 외부 연동·인증·결제·파일·알림·mock 데이터가 있으면 **환경별 동작**(local/dev mock 허용 여부, prod 금지 경로)을 §5 권한·상태·오류·외부의존성에서 산문으로 확정한다.
- Spec은 **검증 가능성**을 명시한다. 무엇을 자동 검증하고, 무엇이 검증 불가이며, 어디가 시스템 안전성에 위험한지를 §5.5/§6/§12.5에 분리해 둔다. 이 정의가 명확해야 team-dev/team-e2e가 자동 영역과 사용자 확인 영역을 분기할 수 있다.

## 파일 구조

```text
docs/spec/{년}/{월}/[개발자아이디]-[YYMMDD]-[한글기능명].md
```

예:

```text
docs/spec/2026/05/{개발자아이디}-260506-공지사항-게시판.md
```

개발자 아이디는 `whoami`를 우선 사용하고, 실패하면 `git config user.name`을 사용한다.

## 산출물 구조

### Part A: 한눈에 보기

사람이 기능의 본질을 빠르게 확인하는 섹션이다.

| 섹션 | 정책 |
|------|------|
| 요약 카드 | 의무. 무엇/누가/핵심 액션/신규·변경 테이블/검증 포인트 |
| 핵심 흐름 | 권장. 사용자 액션 1~3개의 sequence diagram |
| 데이터 모델 | 권장. 신규/변경 테이블만 erDiagram으로 표현 |
| 추가 다이어그램 | 선택. 상태 머신이나 특수 흐름이 있을 때만 |

폐기:
- 시스템 아키텍처 다이어그램: 피치 하네스 표준 구조라 정보 가치가 낮다.
- UI 흐름도 다이어그램: ui-proto가 1차 자료다. ui-proto가 없으면 Part B의 화면 기준 표로 대체한다.

### Part B: 확정 Spec

`team-dev`, `team-e2e`, `gen-db`가 우선 읽는 실행 기준이다.

| 섹션 | 정책 | 목적 |
|------|------|------|
| 메타 | 의무 | 모듈명, 기능명, UI 패턴, 참조 자료 |
| 1. 기능 범위 | 의무 | CRUD, 특수 액션, 파일/엑셀/외부 연동 |
| 2. 화면/액션 기준 | 의무 | ui-proto 기반 화면, 액션, 성공/오류 상태 |
| 3. DB 스키마 기준 | 의무 | gen-db가 마이그레이션을 만들 수 있는 컬럼/인덱스/참조 |
| 4. API 계약 | 의무 | Backend/Store/Contract가 맞출 요청·응답 기준 |
| 5. 권한·상태·오류·외부의존성 | 의무 | 구현 누락 방지 기준 (5.5 시스템 안전성 포함) |
| 6. TEST_ID 요구사항 | 의무 | 요구사항, 완료 기준, 검증 등급 |
| 7. Backend TDD 기준 | 의무 | 테스트 코드가 아니라 검증해야 할 동작 |
| 8. Store/Contract 기준 | 의무 | API 응답 키와 Store 상태 기준 |
| 9. UI 구현 기준 | 의무 | 화면 상태, 버튼, 토스트, 검증 메시지 |
| 10. E2E 시나리오 | 의무 | 사용자 흐름, 입력, 기대 결과 |
| 11. 파일/모듈 경계 | 의무 | 생성·수정 대상 디렉터리 |
| 12. 제외/금지 사항 | 선택 | 범위 밖 기능과 금지 구현 (12.5 검증 불가 영역 포함) |
| 13. 참조 | 의무 | ui-proto, schema, 기능 문서, 가이드 코드 |

## Spec에서 빠지는 것

| 항목 | 책임 |
|------|------|
| 테스트 코드, describe/it 상세 | `peach-team-dev` |
| selector, wait, fixture, suite 코드 | `peach-team-e2e` |
| 실행 이력, Ralph Loop 이력 | `docs/qa/`, `docs/e2e-suite/` |
| 4축 상태 매트릭스(S/U/I/V) | 사용하지 않음 |
| PRD 추적 표 | 사용하지 않음 |

## 필수: DB 종류 판별

스킬 실행 시 가장 먼저 대상 프로젝트의 env 파일을 읽어 DB 종류를 판별한다.

```bash
api/src/environments/env.local.yml
```

`DATABASE_URL` 기준:

| URL | 모드 |
|-----|------|
| `postgresql://...` | PostgreSQL |
| `mysql://...` | MySQL |

타입 기준:

| 용도 | PostgreSQL | MySQL |
|------|------------|-------|
| PK | serial4 | INT AUTO_INCREMENT |
| 정수 | int4 | INT |
| 큰 정수 | int8 | BIGINT |
| 날짜시간 | TIMESTAMP | DATETIME |
| 참조값 | int4 | INT |

> 타입 매핑 SoT는 `peach-gen-db/references/type-mapping.md`다. 변경 시 양쪽을 함께 갱신한다.

## 입력 시나리오

| 시나리오 | 입력 인자 | 설명 |
|----------|----------|------|
| ui-proto 기반 | `proto=<ui-proto 태스크 경로>` | 권장. 확정된 화면 기획안에서 Spec 추출 |
| 기존 개선 | `feature-docs=<경로>` 또는 컨텍스트 주입 | peach-doc-feature 산출물을 기준으로 변경 Spec 생성 |
| 자연어/대화 | 없음 | 작은 신규 기능을 대화로 수집 |
| DB 초안 보강 | `schema=<경로>` | 기존 schema/DDL/ERD 초안을 함께 읽어 DB 기준 보강 |
| 토론/확정 | 사용자가 "수정 전", "핵심만", "방향 확정 후 수정" 요청 | 문서를 바로 수정하지 않고 분석·권장안·확인 질문만 반환 |

실행 형태:

```bash
/peach-gen-spec proto=<ui-proto 태스크 경로>
/peach-gen-spec proto=<ui-proto 태스크 경로> schema=<schema 또는 DDL 경로>
/peach-gen-spec feature-docs=<기능별설명 폴더>
/peach-gen-spec
```

## 워크플로우

### 0단계: 입력 모드 분기

```text
proto=<경로> 있음        → ui-proto 기반 모드
feature-docs=<경로> 있음 → 기존 개선 모드
schema=<경로> 있음       → DB 초안 보강
인자 없음                → 자연어/대화 모드
사용자가 "수정 전/핵심만/방향 확정 후 수정" 요청
                         → 토론/확정 모드 (문서 수정 보류)
```

토론/확정 모드에서는 다음 순서로만 응답하고 파일을 수정하지 않는다.

```text
1. 현재 이해
2. 미확정 판단
3. 권장안
4. 사용자 확인 질문
5. 사용자 확정 후에만 문서 반영
```

### 1단계: 자료 수집

ui-proto/기능 문서 외에도 **현행 구현 확인**을 짧게 수행한다. 결과는 Spec에 길게 쓰지 않고 `현행 구조 기반 확장 / 신규 생성 / 제외` 정도로 압축한다.

- DB: 기존 테이블/컬럼/상태값/인덱스
- Backend: API, service, dao, transaction, approval/processing flow
- Frontend: 화면, store, contract, modal, route
- TDD: 기존 helper, fixture, cleanup 패턴
- E2E: 기존 scenario, suite, seed/data 준비 방식

이어서 ui-proto 기반이면 다음 자료를 읽는다.

```bash
# 메타
<PROTO_PATH>/_task-meta.ts

# 현업 검토용 설명/기획 개요
<PROTO_PATH>/overview/pages/overview.vue

# 화면 파일
<PROTO_PATH>/**/pages/*.vue

# Mock 데이터
<PROTO_PATH>/**/mock/*.mock.ts

# Mock Store
<PROTO_PATH>/**/store/*.store.ts

# 타입
<PROTO_PATH>/**/type/*.ts
```

기존 개선 모드이면 `feature-docs`의 개요 문서를 먼저 읽고 필요한 세부 문서만 추가로 읽는다.

schema 입력이 있으면 테이블/컬럼/인덱스/참조 관계를 읽고 Spec의 DB 스키마 기준에 반영한다.

### 2단계: 기본 정보 확정

- 모듈명: 영문 kebab-case
- 테이블명: snake_case
- 한글 기능명: 파일명용
- 한줄 설명
- UI 패턴: crud / two-depth / select-list / page / excel
- 파일 업로드: 없음 / 일반 파일 / 이미지 / 일반 파일 + 이미지
- 저장 방식: 없음 / Local / S3
- DB 종류: PostgreSQL / MySQL

### 3단계: 기능 범위 확정

기본 CRUD:

- 페이징 목록(`findPaging`)
- 키워드/선택 목록(`findList`)
- 상세 조회(`detailOne`)
- 등록(`insert`)
- 수정(`update`)
- 사용여부 변경(`updateUse`)
- 논리 삭제(`softDelete`)

특수 액션이 있으면 CRUD와 분리해서 명시한다.

예:
- 승인 / 반려
- 엑셀 업로드 / 다운로드 / 템플릿 다운로드
- 일괄 변경
- 파일 미리보기 / 다운로드
- 알림 발송
- 외부 API 동기화

### 4단계: 화면/액션 기준 확정

ui-proto에서 다음을 추출하고, 모호한 부분만 사용자에게 확인한다.

- 화면 목록: 목록, 상세, 등록, 수정, 모달, 탭, 일괄처리 등
- 주요 액션: 검색, 저장, 삭제, 승인, 반려, 업로드, 다운로드 등
- 입력 필드: 필수/선택, 타입, 길이, 선택값
- 목록 컬럼: 컬럼명, 정렬, 표시 조건
- 성공 상태: 토스트, 모달 닫힘, 목록 새로고침, 상세 이동, 상태 변경
- 오류 상태: 필수값 검증, 권한 실패, 서버 오류, 외부 연동 실패
- 빈 상태: 목록 0건, 검색 결과 없음, 파일 없음

### 5단계: DB 스키마 기준 확정

gen-db가 바로 마이그레이션을 만들 수 있도록 아래를 확정한다.

- 신규/변경 테이블
- 컬럼명, 타입, 필수 여부, 설명, 선택값, 기본값
- 인덱스 후보
- 논리적 참조 관계(FK 생성 없음)
- 공통 컬럼 적용 여부: `is_use`, `is_delete`, `insert_seq`, `insert_date`, `update_seq`, `update_date`
- DB 변경 후보와 확정 조건

DB 설계는 컬럼 목록만 쓰지 않는다. 다음 판단을 짧게 남긴다.

- 채택한 구조와 이유
- 제외한 구조와 이유
- unique 기준
- 히스토리 테이블 필요 여부
- soft delete / 공통 감사 컬럼 적용 또는 제외 여부 (단건 상태 테이블·로그성·외부 원장 테이블처럼 성격상 맞지 않으면 제외 가능, 제외 시 §12 제외/금지 사항에 명시)
- FK 금지 (참조 무결성은 애플리케이션에서 처리)

모호하면 `DB_DECISION_REQUIRED`로 남기되, 가능하면 Spec 생성 단계에서 사용자 확인 후 확정한다.

### 5.5단계: 시스템 안전성 확정

§5 권한·상태·오류·외부의존성 안에 **시스템 안전성** 소절을 명시한다. 카파시 인터뷰에서 짚은 "동작은 하지만 시스템적으로 위험한 결정"(예: 외부 이메일을 식별자로 사용해 결제와 로그인을 매칭) 부류를 Spec 단계에서 사전 차단한다.

다음 항목을 산문으로 확정한다. 해당 없으면 "해당 없음"으로 적되, "해당 없음"이 너무 많으면 §7.5 자가 점검에서 의심한다.

- 식별자 정책: 무엇이 PK인가, 외부 입력(이메일·전화)을 식별자로 사용하는가
- 데이터 소유 경계: 누구의 데이터를 누가 조회/수정 가능한가
- 교차 매칭 금지: 두 시스템 간 매칭에 사용 금지인 키
- 회귀 위험 표식: 이 기능이 인증/세션/공통 모듈을 건드리는가 (Y/N)

### 6단계: API 계약 확정

`team-dev`와 `team-e2e`가 같은 기준을 보도록 요청/응답을 명시한다.

- endpoint
- method
- query/path/body
- response shape
- error response
- 파일 업로드 multipart 여부
- pagination key: `list`, `totalRow`, `page`, `rowSize` 등 기존 패턴 우선

코드 구현 예제는 쓰지 않는다. 계약만 쓴다.

### 7단계: TEST_ID + TDD/E2E 기준 확정

TEST_ID는 요구사항당 하나를 기본으로 한다.

권장 형식:

```text
R-001, R-002 ...
```

도메인이 명확하면 접두어를 붙인다.

```text
NOTICE-001, NOTICE-002 ...
```

§6 TEST_ID 표는 모든 요구사항을 나열한다(요구사항 + 완료 기준 + 검증 등급).

#### 검증 등급 (4단계)

각 TEST_ID에 다음 중 하나를 부여한다. team-dev/team-e2e가 등급에 따라 자동 영역과 사용자 확인 영역을 분기한다.

| 등급 | 의미 | 처리 |
|------|------|------|
| 자동(높음) | 타입·테스트·계약 | team-dev/e2e 자동 |
| 자동(중간) | 비즈니스 규칙 | TEST_ID 매핑 후 자동 |
| 사람(중간) | 권한·교차 매칭·시스템 안전성 | 사용자 확인 필수 |
| 사람(낮음) | 미학·카피·실거래 정확성 | 자동 루프 금지, §12.5에 함께 명시 |


§7 Backend TDD, §10 E2E는 **TEST_ID 전부를 다루지 않는다**. 핵심 검증만 골라 작성한다.

#### Backend TDD 선별 기준 (다음 중 해당하는 것만 작성)

- 핵심 상태 전이 (예: 임시저장 → 승인요청 → 승인)
- 저장/갱신 결과 (필드값, 감사 컬럼, 이력 테이블)
- 권한 또는 소유 범위 차단
- 대표 실패 케이스 (외부 연동 실패, 동시 수정, 중복)
- 테스트 데이터 생성/정리 책임

> 단순 CRUD 기본 동작(필수값 검증, 정상 insert, 정상 update)은 team-dev가 표준 패턴으로 처리하므로 Spec에 적지 않는다.

#### E2E 시나리오 선별 기준

- 핵심 사용자 흐름만 단위 시나리오로 둔다.
- "기존 데이터가 있다고 가정"하지 않는다. 시작 데이터는 시나리오/suite가 직접 준비한다.
- 같은 흐름이 여러 TEST_ID에서 반복되면 **suite 조합**을 우선한다.
- selector, wait, fixture, suite 내부 코드는 쓰지 않는다.
- 단위 시나리오 작성 규칙(단일 책임/재활용/독립 실행)과 suite 통합 규칙은 `peach-e2e-scenario` / `peach-e2e-suite`가 SoT다. Spec에는 흐름 의도만 둔다.

예:

```text
TEST_ID: NOTICE-001 (등록 흐름 — 핵심)
Backend TDD: 등록자/등록일 저장 + 필수값 검증
E2E 단위: 빈 목록 → 등록 → 필수값 입력 → 저장 → 목록에 노출

TEST_ID: NOTICE-005 (승인 흐름 — 상태 전이)
Backend TDD: 승인요청 → 승인 상태 전이, 권한 차단
E2E 단위: 등록된 공지 → 승인요청 → 관리자 로그인 → 승인 → 상태 변경 확인

E2E suite: 공지 라이프사이클
  단위(등록) → 단위(승인) → 사용여부 변경 → 삭제
```

### 7.5단계: 검증성 자가 점검

8단계 파일 생성 전에 다음 5개 질문을 자체 점검한다. 하나라도 문제가 있으면 사용자에게 보고하고 보강 후 8단계로 넘어간다.

1. 모든 TEST_ID에 검증 등급이 매겨졌는가?
2. §5.5 시스템 안전성에서 "해당 없음"이 5개 이상인가? (있으면 의심하고 재검토)
3. 외부 입력(이메일·전화·외부 시스템 ID)을 식별자로 쓰는 곳이 있는가?
4. 인증/세션/_common 변경이 예상되는가? 있으면 §5.5 회귀 위험 표식에 Y로 명시한다.
5. §12.5 검증 불가 영역이 비어 있는가? 정말 없는지 미학·카피·실거래·외부 연동 안전성 관점에서 재확인한다.

이 점검은 카파시가 짚은 jagged intelligence 영역을 Spec 단계에서 분리하기 위한 것이다. 점검 결과는 완료 보고에 한 줄로 남긴다.

### 8단계: 사용자 확인 후 파일 생성

- 단일 `.md` 파일 한 개를 생성한다.
- `assets/spec-template.md`를 읽어 치환한다.
- 사용자 확인이 끝난 항목만 `확정`으로 쓴다.
- 미확정 항목은 `DECISION_REQUIRED` 또는 `DB_DECISION_REQUIRED`로 남기고 완료 보고에서 차단 항목으로 알린다.

## 템플릿

[spec-template.md](assets/spec-template.md)를 읽어 치환한다.

주요 플레이스홀더:

| 플레이스홀더 | 의미 |
|--------------|------|
| `FEATURE_NAME_KR` | 한글 기능명 |
| `DESCRIPTION` | 한줄 설명 |
| `MODULE_NAME` | 모듈명 |
| `TABLE_NAME` | 테이블명 |
| `DB_TYPE` | PostgreSQL/MySQL |
| `STATUS` | 초안/확정/차단 |
| `SOURCE_REFERENCES` | ui-proto/schema/기능 문서 경로 |
| `SUMMARY_*` | Part A 요약 카드 |
| `SEQUENCE_DIAGRAM_BODY` | 핵심 흐름 sequence body |
| `ER_DIAGRAM_BODY` | 데이터 모델 erDiagram body |
| `FUNCTION_SCOPE` | CRUD/특수 액션/파일 기능 |
| `SCREEN_ACTION_CRITERIA` | 화면/액션/성공/오류 기준 |
| `SCHEMA_COLUMNS` | DB 컬럼 표 본문 |
| `SCHEMA_INDEXES` | 인덱스 SQL |
| `REFERENCE_RELATIONS` | 논리 참조 관계 |
| `DB_CHANGE_CANDIDATES` | DB 변경 후보 |
| `API_CONTRACTS` | API 계약 |
| `RULES_PROSE` | 권한/상태/오류/외부의존성 |
| `SYSTEM_SAFETY` | 시스템 안전성 (식별자/소유 경계/교차 매칭 금지/회귀 위험) |
| `REQUIREMENT_MATRIX` | TEST_ID 요구사항 매트릭스 (검증 등급 포함) |
| `TDD_CRITERIA` | Backend TDD 기준 |
| `STORE_CONTRACT_CRITERIA` | Store/Contract 기준 |
| `UI_IMPLEMENTATION_CRITERIA` | UI 구현 기준 |
| `E2E_SCENARIOS` | E2E 단위 시나리오 |
| `E2E_SUITES` | E2E 통합 suite (선택) |
| `MODULE_BOUNDARIES` | 파일/모듈 경계 |
| `FORBIDDEN_ITEMS` | 제외/금지 사항 |
| `UNVERIFIABLE_AREAS` | 검증 불가 영역 (자동 검증 금지, 사용자 확인 영역) |
| `REFERENCE_INDEX` | 참조 인덱스 |

## 완료 조건

```text
□ DB 종류 판별 완료
□ ui-proto/기능 문서/schema 입력 자료 확인 완료
□ 기능 범위 확정
□ 화면/액션/성공/오류 기준 확정
□ DB 스키마 기준 확정 또는 DB_DECISION_REQUIRED 명시
□ API 계약 확정
□ §5.5 시스템 안전성 확정 (식별자/소유 경계/교차 매칭/회귀 위험)
□ TEST_ID 요구사항 매트릭스 확정 (검증 등급 포함)
□ Backend TDD 기준 확정
□ Store/Contract 기준 확정
□ UI 구현 기준 확정
□ E2E 시나리오 확정
□ §12.5 검증 불가 영역 명시 (없으면 "해당 없음")
□ §7.5 검증성 자가 점검 5개 질문 통과
□ 제외/금지 사항 확인
□ 단일 Spec 파일(.md) 생성 완료
□ team-dev/team-e2e가 추가 기획 질문 없이 실행 가능한지 자체 점검 완료
```

## 완료 후 안내

```text
Spec 생성이 완료되었습니다.

산출물: docs/spec/{년}/{월}/[개발자]-[YYMMDD]-[기능명].md

다음 단계:
1) DB 마이그레이션 생성
   /peach-gen-db spec=docs/spec/.../[기능명].md

2) 본 개발
   /peach-team-dev [모듈명] mode=fullstack spec=docs/spec/.../[기능명].md

3) E2E 검증
   /peach-team-e2e spec=docs/spec/.../[기능명].md [proto=<ui-proto 태스크 경로>]
```

사용자가 후속 구현을 별도 세션/worktree에서 이어가려면 다음 인계 정보를 함께 안내한다.

```text
- 대상 저장소
- 기준 브랜치 / feature branch 추천명
- Spec 문서 경로
- Spec 확정 커밋
- worktree 추천 경로 (peach-worktree 스킬 활용 가능)
- team-dev 실행 명령
- team-e2e 실행 명령
- commit/push 전 사용자 확인 원칙
```

## 예제

Spec 주도 개발 예제는 [examples.md](references/examples.md)를 필요한 경우에만 읽는다.

## 주의사항

1. PRD 추적 섹션을 만들지 않는다. 구현 기준은 Spec이다.
2. 질문은 단계별로 진행하되, 컨텍스트가 충분하면 단계 통합 가능하다.
3. 작은 단일 수정은 정식 Spec을 강제하지 않고 짧은 메모로 처리 가능하다.
4. 시스템 아키텍처 다이어그램을 반복 생성하지 않는다.
5. 4축 상태 매트릭스(S/U/I/V)를 만들지 않는다.
6. 권한/상태/오류/외부의존성은 산문 1차, 복잡할 때만 표로 확장한다.
7. TDD/E2E는 코드가 아니라 검증 기준과 시나리오로 확정한다.
8. Spec에 없는 요구는 `team-dev`와 `team-e2e`가 임의 구현하지 않는다.
9. 검증 가능성은 Spec이 책임진다. §5.5 시스템 안전성, §6 검증 등급, §12.5 검증 불가 영역을 비워 두지 않는다. 비워 두면 downstream이 jagged 영역을 자동으로 식별하지 못한다.
