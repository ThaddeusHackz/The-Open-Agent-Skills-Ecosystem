---
name: peach-team-dev
model: opus
description: |
  PeachSolution 신규 모듈 개발을 조율하는 통합 팀 스킬.
  준비된 DB 스키마와 Spec, ui-proto 기반 표준 모드 + Spec만 모드 + 자연어 prompt 모드를 지원.
  "팀으로 만들어줘", "풀스택 개발", "팀 개발", "백엔드+UI 전체 생성",
  "버그 수정해줘", "이 화면에 X 추가해줘", "API와 화면 같이 만들어줘",
  "백엔드만 만들어줘", "API만 만들어줘", "UI만 추가" 키워드로 트리거.
  mode=backend(API+Store) | ui(UI만) | fullstack(전체) 지원하며,
  mode/proto 없이 자연어 입력만으로도 즉흥적 버그 수정·기능 추가 가능.
  대규모 작업은 기능 큐와 Contract Gate로 1차 완성도를 높이는 방향을 따른다.
  peach-team-e2e와 함께 하나의 개발-검증 납품 흐름을 이루되, E2E 검증 독립성은 유지한다.
  팀 실행 방식은 요청 범위와 런타임 도구 가용성을 분석해 single-agent / role-queue / agent-team 중 선택한다.
  기존 팀 개발 스킬의 개발 조율 역할을 대체하며, DB 생성은 peach-gen-db 선행 단계로 분리한다.
---

# Peach Team Dev

PeachSolution 개발을 조율하는 통합 오케스트레이터다. 신규 기능, 기존 기능 수정, prompt 기반 즉흥 작업을 처리하되 구현 기준은 항상 외부 산출물과 기존 코드 증거에서 가져온다.

## 핵심 책임

- 구현과 코드 수준 검증을 수행한다: TDD, lint, build, API-Store Contract Gate.
- 사용자 흐름과 기획 부합 검증은 `peach-team-e2e`로 넘긴다.
- DB 마이그레이션 생성과 적용은 직접 하지 않는다. `mode=backend|fullstack`은 `peach-gen-db`로 생성된 `api/db/schema/...`가 준비된 뒤 실행한다.
- Spec, schema, ui-proto가 충돌하거나 기준이 없으면 추측 구현하지 않고 `DECISION_REQUIRED`, `DB_DECISION_REQUIRED`, `DB_CHANGE_REQUIRED`로 차단한다.
- 요청 범위와 런타임 도구 가용성에 따라 `single-agent`, `role-queue`, `agent-team` 중 하나를 선택한다.

## 입력 모드

| 모드 | 입력 | 검증 기준 | 적합 케이스 |
|------|------|---------|-----------|
| 표준 | `mode` + `spec` + `proto` | Spec + ui-proto 화면 | 신규 기능 표준 경로 |
| Spec만 | `mode` + `spec` | `docs/spec/...` Spec | 백엔드 중심, 기존 화면 수정, 단순 CRUD |
| prompt | 자연어 입력 | prompt 텍스트 + 기존 코드 | 버그 수정, 즉흥적 변경, 핫픽스 |
| queue | `queue=<기능큐.md>` | 기능별 Spec/schema/proto | 큰 작업의 기능별 상태 관리 |

prompt 모드는 검증 기준이 약하므로 작은 변경은 경량 처리하고, 중규모는 자동 팀 모드로 전환한다. 기준이 부족한 큰 변경은 `peach-gen-spec`으로 Spec 작성을 권고하고 중단한다.

## Modes

| mode | 용도 | 포함 역할 |
|------|------|----------|
| `backend` | 준비된 DB 스키마 기준 API + Store 연결 | backend-dev, backend-qa, store-dev, frontend-qa |
| `ui` | Store 기반 UI만 구현 | ui-dev, frontend-qa |
| `fullstack` | 준비된 DB 스키마 기준 API + Store + UI 생성 | backend-dev, backend-qa, store-dev, ui-dev, frontend-qa |

## Preconditions

### 표준 모드

- `docs/spec/{년}/{월}/`의 Spec 파일이 존재해야 한다.
- ui-proto 저장소의 태스크 폴더가 존재해야 한다.
- DB 스키마가 필요한 모드에서는 `api/db/schema/[도메인]/[테이블].sql`이 존재해야 한다.

### Spec만 모드

- DB 스키마가 필요한 모드에서는 `api/db/schema/[도메인]/[테이블].sql`이 존재해야 한다.
- `ui` 모드에서는 `front/src/modules/[모듈명]/store/[모듈명].store.ts`가 존재해야 한다.
- Store가 없으면 먼저 `peach-gen-store`, UI가 없으면 `peach-gen-ui` 기준으로 생성한다.
- 기존 기능 수정이면 `docs/기능별설명/{카테고리명}/{기능명}/`가 있을 때 개요, 로직, 명세, TDD 순으로 먼저 읽는다.
- Spec의 화면 흐름 요약이 있으면 UI 흐름의 최소 기준으로 사용한다.
- 신규 복잡 화면인데 Spec에 화면 흐름 요약이 없으면 `peach-team-ui-proto` 또는 Spec 보강을 권고하고, 강행 시 완료 보고에 검증 한계를 남긴다.

### prompt 모드

- 사전 조건은 자연어 입력이다.
- 변경 규모 추정 후 DB/권한/상태/API 계약 기준이 부족하면 Spec 작성으로 돌린다.

## Inputs

```bash
# 표준 모드
/peach-team-dev [모듈명] mode=backend|ui|fullstack spec=<경로> proto=<경로> [옵션]

# 대규모 기능 큐 모드
/peach-team-dev [작업명] queue=<기능큐.md> [proto=<경로>] [옵션]

# Spec만 모드
/peach-team-dev [모듈명] mode=backend|ui|fullstack spec=<경로> [옵션]

# prompt 모드
/peach-team-dev "버그/개선 사항 자연어 설명" [옵션]
```

| 인자 | 역할 |
|------|------|
| `[모듈명]` | 표준/Spec만 모드에서 권장. prompt 모드에서는 후보 제안 후 확정 |
| `mode` | 표준/Spec만 모드에서 필수 |
| `spec` | 본 프로젝트 `docs/spec/...`의 Spec 파일 경로 |
| `queue` | 큰 작업용 기능 큐 문서. 지정 시 기능별 mode/input/status를 기준으로 반복 실행 |
| `proto` | ui-proto 저장소의 태스크 폴더 절대 경로 |
| `model` | 선택. 서브에이전트 모델 override. 미지정 기본값은 `sonnet`, 허용 값은 `sonnet|opus|haiku` |
| `team` | 선택. `force`는 agent-team 강제 시도, `off`는 실제 agent-team 금지 |
| `e2e` | 선택. `auto`는 개발 전 E2E preflight 후 완료 시 `peach-team-e2e` 자동 실행, `off`는 자동 체인 비활성 |
| `figma`, `ui`, `file`, `excel`, `storeTdd` | 선택. 역할별 reference의 옵션 처리 기준을 따른다 |

E2E chain 해석:

```text
team-dev만 요청 → E2E 미실행
team-dev + team-e2e 함께 요청 → e2e=auto
사용자가 E2E 제외 명시 또는 e2e=off → e2e=off
```

## 구현 기준 우선순위

### Spec / schema / proto 충돌 처리

| 상황 | 처리 |
|------|------|
| Spec과 schema가 일치 | Spec/schema 기준으로 구현 |
| Spec에 없는 요구 발견 | 임의 구현하지 않고 `DECISION_REQUIRED`로 기록 |
| Spec과 schema가 충돌 (의사결정 필요) | `DB_DECISION_REQUIRED`로 분리하고 사용자 결정 요청 |
| Spec과 schema가 충돌 (변경 필요 확정) | `DB_CHANGE_REQUIRED`로 분리하고 `peach-gen-db` 후속 |
| ui-proto와 Spec이 충돌 | 비즈니스/데이터는 Spec 우선, 화면/흐름은 ui-proto 우선. 자동 병합하지 않는다 |

ui-proto는 Mock 산출물이므로 team-dev는 코드 구조와 이벤트 구현 참고로 사용한다. 실제 사용자 흐름 부합은 `peach-team-e2e`가 판정한다.

### 항목별 team-dev 기준 vs 최종 검증

ui-proto는 본질적으로 Mock이라 100% 구현되지 않을 수 있다. team-dev는 다음 기준으로 구현/TDD 범위를 잡고, 실제 브라우저 흐름 부합 검증은 `peach-team-e2e`로 넘긴다.

| 항목 | team-dev 기준 | 최종 검증 |
|------|---------------|-----------|
| 화면 레이아웃, 컴포넌트 배치 | ui-proto 화면을 구현 참고 자료로 사용 | `peach-team-e2e` |
| 사용자 인터랙션 흐름 | ui-proto/Spec을 기준으로 코드 구조와 이벤트를 구현 | `peach-team-e2e` |
| 비즈니스 규칙 (검증, 권한, 분기) | Spec 기준으로 API/Store/UI 코드와 TDD 작성 | TDD + `peach-team-e2e` |
| 데이터 정확성 (API 응답값) | Spec 기준으로 타입/API/TDD 검증 | TDD |
| 에러/예외 처리 | Spec 기준으로 코드와 테스트 작성 | TDD + 필요 시 E2E |

핵심 원칙: team-dev는 구현과 코드 수준 검증까지 책임진다. 화면 흐름이 실제 사용자 관점에서 기획 의도와 맞는지는 `peach-team-e2e`가 판정한다. 두 팀 사이의 책임 경계와 자세한 운영 규칙은 `references/dev-e2e-chain.md`를 따른다.

## Reference 선택

필요한 상세 문서만 읽는다. `SKILL.md`는 실행 라우터이고, 세부 절차와 역할 정의는 아래 reference가 Source of Truth다.

| 상황 | 읽을 reference |
|------|----------------|
| 팀 구성 자동 분석 | `references/runtime-team-selection.md` |
| Claude/Codex 실행 모드 선택 | `references/runtime-adapter.md` |
| 전체 입력 판정, 환경 확인, 도메인 분석, 작업 등록 | `references/orchestration-workflow.md` |
| proto 인자 처리 | `references/proto-sync.md` |
| prompt 모드 | `references/prompt-mode.md` |
| 대규모 기능 큐 | `references/queue-workflow.md` |
| team-dev + team-e2e 자동 chain | `references/dev-e2e-chain.md` |
| fullstack 병렬 개발 | `references/fullstack-workflow.md` |
| Mock Store → 실제 Store 연결 | `references/connect-workflow.md` |
| Figma 입력 | `references/figma-workflow.md` |
| API-Store-UI 연결 검증 | `references/contract-gate.md` |
| 결정 차단, DB 변경 차단 템플릿 | `references/blockers.md` |
| QA 판정과 완료 보고 | `references/qa-policy.md` |
| 역할별 dev/qa 지시 | `references/*-agent.md` |

## 실행 순서

1. `references/runtime-team-selection.md`와 `references/runtime-adapter.md`를 읽고 `single-agent`, `role-queue`, `agent-team` 중 실행 방식을 정한다.
2. 입력 형태를 판정한다: `queue` → 기능 큐, 자연어 단독 → prompt, `mode+proto` → 표준, `mode`만 → Spec만.
3. `e2e=auto` 또는 team-dev/team-e2e 동시 요청이면 개발 시작 전에 `references/dev-e2e-chain.md`의 preflight를 수행한다.
4. 환경, schema, 기존 모듈 구조, gen-* reference 경로를 확인한다. 상세 명령은 `references/orchestration-workflow.md`를 따른다.
5. Spec, schema, proto 또는 prompt를 읽고 도메인 특성을 분석해 역할별 프롬프트에 주입한다.
6. mode와 분석 결과에 맞춰 역할을 실행한다. 실제 agent-team을 쓸 수 없으면 같은 순서를 role-queue로 실행한다.
7. 각 dev 역할은 요청 범위 구현과 자체 검증을 수행하고, QA 역할은 독립적으로 검증한다.
8. `mode=backend|fullstack` 또는 연결 변경이 있으면 `references/contract-gate.md`를 기준으로 API-Store Contract Gate를 수행한다.
9. QA가 `REJECTED`면 `references/qa-policy.md`의 반복 상한 안에서 dev 역할로 되돌린다.
10. 완료 보고에 TDD/lint/build/Contract Gate, TEST_ID 구현 상태, 차단 항목, E2E 인계 정보를 남긴다.

## 역할 구성

| 역할 | 참조 파일 | 핵심 책임 |
|------|----------|----------|
| backend-dev | `references/backend-dev-agent.md` | API 코드 생성, TDD/lint/build |
| backend-qa | `references/backend-qa-agent.md` | Backend 구조, TDD, lint, build, Spec 기반 검증 |
| store-dev | `references/store-dev-agent.md` | Backend 타입 기반 Pinia Store 생성과 타입 검증 |
| ui-dev | `references/ui-dev-agent.md` | Store 기반 UI 생성, 디자인 시스템/Figma/proto 반영 |
| frontend-qa | `references/frontend-qa-agent.md` | Store/UI 구조, 타입, lint, build, AI Slop, Spec/proto 반영 검증 |

진짜 SoT는 대상 프로젝트의 `test-data/` 가이드 코드와 gen-* 스킬 reference다. team-dev는 같은 패턴을 팀 실행 방식으로 조율한다.

## QA와 완료

QA 에이전트는 `APPROVED / CONDITIONAL / REJECTED`로 판정한다. `APPROVED` 후에는 `/peach-qa-gate`를 실행하고, `REJECTED`는 Ralph Loop로 dev 에이전트 수정 후 재검증한다.

완료 보고에는 최소한 다음을 포함한다.

- 변경 요약과 파일 경로
- 실행한 TDD/lint/build 명령과 결과
- Contract Gate 결과: 통과/실패/스킵
- TEST_ID별 구현 상태: 구현전/구현중/일부구현/구현완료/차단
- `DECISION_REQUIRED`, `DB_DECISION_REQUIRED`, `DB_CHANGE_REQUIRED` 항목
- `e2e_chain` 상태와 `peach-team-e2e` handoff contract 또는 후속 권장

상세 판정 규칙과 보고 필드는 `references/qa-policy.md`, 기능 큐 상태는 `references/queue-workflow.md`, E2E 인계는 `references/dev-e2e-chain.md`를 따른다.

## Examples

```bash
# 표준 fullstack
/peach-team-dev product-manage mode=fullstack spec=docs/spec/2026/05/example.md proto=<PROTO_REPO>/src/modules-task/2604/260427-<initial>-goods

# Spec만 backend
/peach-team-dev notice-board mode=backend spec=docs/spec/2026/05/example.md

# 개발 후 team-e2e까지 자동 체인
/peach-team-dev product-manage mode=fullstack spec=docs/spec/2026/05/example.md e2e=auto

# prompt 모드
/peach-team-dev "list.vue 검색 후 페이지네이션 클릭 시 검색어 초기화되는 문제 수정"
```

## 관련 스킬

- `peach-gen-spec` — Spec 단독 생성
- `peach-team-ui-proto` — 기획 검토용 ui-proto 팀 생성/검증
- `peach-gen-db` — DB 스키마/마이그레이션 생성
- `peach-gen-backend`, `peach-gen-store`, `peach-gen-ui` — 단계별 단독 호출
- `peach-team-e2e` — E2E 검증
- `peach-team-3a` — 작은 단일 기능
- `peach-doc-feature` — 기존 기능 As-Is 분석
