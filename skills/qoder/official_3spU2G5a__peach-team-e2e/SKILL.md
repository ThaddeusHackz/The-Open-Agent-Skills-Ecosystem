---
name: peach-team-e2e
model: opus
description: |
  Spec 필수 + ui-proto 보조 기준으로 E2E 환경 세팅 + 단위 시나리오 자동 분할 + 통합 suite 생성 + 실행 + 부합 검증을 한 번에 처리하는 통합 팀 스킬.
  "e2e 검증해줘", "통합 검증", "전체 흐름 테스트", "팀 e2e", "스펙대로 동작하는지 확인",
  "ui-proto와 다른지 확인", "최종 검증", "릴리스 전 검증" 키워드로 트리거.
  peach-e2e-setup + peach-e2e-scenario + peach-e2e-suite 3개 스킬의 패턴을 공유하고,
  검증 기준은 본 프로젝트 Spec을 필수 기준으로 삼고, ui-proto는 화면/흐름 보조 기준으로 사용한다.
  peach-team-dev와 함께 하나의 개발-검증 납품 흐름을 이루되, 구현 컨텍스트와 검증 컨텍스트는 분리한다.
  팀 실행 방식은 E2E 범위와 런타임 도구 가용성을 분석해 single-agent / role-queue / agent-team 중 선택한다.
  단순 코드 동작 검증을 넘어, 기획 의도와 부합하는지 자동 검증하는 게 핵심 차별점.
---

# Peach Team E2E

본 프로젝트 Spec을 필수 검증 기준으로 삼고, ui-proto 화면 흐름은 보조 기준으로 사용해 E2E 시나리오를 자동 분할/조합/실행/검증/보완하는 통합 오케스트레이터.

## Overview

`peach-team-dev`로 본 개발이 끝난 시점에 호출한다. 요청이 Spec/proto 부합 검증, 통합 흐름, 릴리스 전 검증이면 먼저 E2E 범위 분석을 수행한다. 시나리오 분할, suite 구성, QA 독립성, 브라우저/데이터 준비 복잡도에 따라 `single-agent / role-queue / agent-team` 중 하나를 선택하고 다음을 한 번에 처리한다.

`peach-team-dev` 자동 chain으로 호출되고 handoff contract에 E2E preflight 결과가 있으면 같은 tab/context를 재사용한다. 이미 준비된 Chrome Beta/CDP/탭/세션은 다시 사용자에게 묻지 않는다. 단독 호출이거나 handoff가 없거나 무효하면 기존 강제 게이트와 자체 preflight를 수행한다.

1. (필요시) E2E 환경 세팅
2. 검증 기준 로드 (Spec 필수 + ui-proto 선택)
3. 단위 시나리오 자동 분할
4. 통합 suite 자동 생성
5. 실행 + 미스매치 분류
6. 자동 보완/자동 위임 루프 (랄프루프 5/10회)

일반 검증은 이 스킬만 사용한다. 기존 `peach-e2e-setup`, `peach-e2e-scenario`, `peach-e2e-suite`는 단일 시나리오 재실행, 실패 디버깅, 수동 세분화, 환경 점검이 필요한 단계별 단독 호출용 Tier 2로만 유지된다. 이 스킬은 그 3단계를 통합하면서 **검증 기준을 Spec으로 고정하고 ui-proto를 보조 기준으로 사용하는 것**이 핵심 차별점이다.
agent-team이 적절하지만 실제 팀 도구가 없으면 시작 전에 generic role-queue로 전환한다고 보고한다.

## 개발-검증 납품 흐름

`peach-team-e2e`는 `peach-team-dev` 이후 이어지는 납품 검증 단계다. 사용 경험상 두 스킬은 하나의 개발-검증 흐름이지만, 검증 독립성을 위해 역할과 컨텍스트를 분리한다.

```text
peach-team-dev 완료 산출
  - 구현 코드
  - TDD/lint/build 결과
  - API-Store Contract Gate 결과
  - TEST_ID 구현 상태 매핑
  - E2E handoff contract
  - E2E 잔여 리스크

peach-team-e2e 검증
  - handoff contract 재사용
  - 사용자 흐름 실행
  - ui-proto/Spec 부합 판정
  - 미스매치 분류
  - 시나리오 오류 자동 보완
  - TEST_ID 검증 상태 갱신
  - 명확한 코드 문제는 peach-team-dev로 위임
```

이 스킬은 본 프로젝트 코드를 직접 수정하지 않는다. Spec 또는 ui-proto 근거가 명확한 코드 문제만 `references/delegation-policy.md` 기준으로 `peach-team-dev`에 위임한다.

## TDD와 E2E의 책임 경계

team-e2e는 **사용자 경험 검증**만 담당한다. 로직 분기 검증은 backend/store TDD가 책임진다.

| 영역 | 책임 | 대상 |
|------|------|------|
| TDD (단위/통합) | 로직이 의도대로 동작하는가 | 분기 함수, DAO, 데이터 변환. `peach-gen-backend`/`peach-gen-store`의 TDD 게이트가 처리 |
| E2E (team-e2e) | 사용자가 보는 그대로 동작하는가 | UI 흐름, 인터랙션, 비즈니스 규칙의 외부 가시 결과 |

운영 규칙:

- 단위 시나리오 안에서 DB 직접 접근(읽기/쓰기 모두), 마이그레이션, 서버/앱 재시작을 발견하면 fixture/suite Step 또는 `peach-db-query`로 분리시킨 뒤 진행한다.
- ui-proto/Spec 모호 영역에서 "이건 TDD에서 검증해야 한다" 판단이 서면 보완 루프로 끌고 가지 말고, backend/store 측 TDD 추가를 권고한다.
- 미스매치 분류 시 "로직 버그"는 team-e2e가 직접 고치지 않고 `peach-team-dev`로 위임한다. Spec/proto 근거가 명확하고 안전 조건을 만족하면 사용자 확인 없이 자동 위임한다.
- Spec의 TEST_ID별 완료 기준에 맞춰 검증 근거와 잔여 리스크를 완료 보고에 남긴다.
- QA 판정 `APPROVED / CONDITIONAL / REJECTED`는 리뷰 판정이다.

TEST_ID 검증 보고 규칙:

| E2E 결과 | 보고 상태 | 기준 |
|----------|----------------|------|
| 미실행 | 검증전 | 아직 E2E 또는 동등 검증 전 |
| 일부 통과 | 일부검증 | 일부 시나리오만 통과하거나 범위 일부만 검증 |
| 전체 통과 | 검증완료 | 관련 TEST_ID의 E2E/QA 근거 확인 |
| 검증 불가 | 검증불가 | 환경/권한/데이터/Mock 한계로 검증 불가 |
| 차단 | 차단 | 기준 충돌, 실행 조건 부재, 반복 실패로 진행 차단 |

## 핵심 차별점 — 검증 기준의 외부화

기존 E2E는 "코드가 동작하는지"만 검증했다. 이 스킬은 **"기획 의도와 부합하는지"**를 검증한다.

| 검증 항목 | 1차 기준 | 2차 기준 |
|----------|---------|---------|
| 화면 레이아웃, 컴포넌트 배치 | ui-proto 화면 | (없으면 Spec) |
| 사용자 인터랙션 흐름 | ui-proto 화면 | Spec |
| 비즈니스 규칙 (검증, 권한, 분기) | Spec | (없으면 검증 불가 → 보고) |
| 데이터 정확성 (API 응답값) | Spec | (없으면 검증 불가 → 보고) |
| 에러/예외 처리 | Spec | - |

**핵심 원칙**: Spec은 필수 기준이다. ui-proto가 있으면 화면/흐름 보조 기준으로 사용하고, 기준이 모호하면 보고한다.
Spec에 없는 요구가 발견되면 코드 수정이 아니라 `DECISION_REQUIRED`로 분류한다.

> ui-proto는 본질적으로 Mock이라 100% 구현되지 않을 수 있다.
> 시각적 흐름 + 인터랙션 시퀀스만 ui-proto 기준, 데이터 정확성은 Spec 기준.

## Inputs

```bash
/peach-team-e2e spec=<경로> [proto=<경로>] [handoff=<경로>] [model=opus|sonnet|haiku] [team=force|off]

# 옵션
# spec=<경로>       본 프로젝트 Spec 파일 경로 (필수)
# proto=<경로>      ui-proto 태스크 폴더 절대 경로 (화면/흐름 기준)
# handoff=<경로>    team-dev 자동 chain 또는 수동 재개 시 전달된 handoff contract
# model=...         서브에이전트 모델 override (기본 sonnet)
# team=force|off    실제 agent-team 강제 시도 / 실제 agent-team 비활성화
```

| 인자 | 역할 |
|------|------|
| `spec` | 필수. 본 프로젝트 `docs/spec/...`의 Spec 파일 경로 |
| `proto` | 선택. ui-proto 저장소의 태스크 폴더 절대 경로 |
| `handoff` | 선택. `peach-team-dev`가 생성한 handoff contract. 자동 chain 호출에서는 입력 컨텍스트로 전달될 수 있음 |
| `model` | 선택. 서브에이전트 모델 override |
| `team` | 선택 override. 기본은 자동 분석이며, `team=force`는 실제 agent-team 생성을 강제 시도하고 `team=off`는 실제 agent-team을 금지 |

`proto` 인자가 없으면 본 프로젝트의 `docs/spec/...`만 검증 기준으로 사용한다.

Spec-only 모드는 신뢰도를 `중간`으로 표시한다. 비즈니스 규칙과 데이터 결과는 검증할 수 있지만, ui-proto가 없으므로 시각/레이아웃 부합 검증은 제한된다. Spec에 `화면 흐름 요약`이 있으면 이를 시나리오 분할 기준으로 사용한다.

## Preconditions

- `peach-team-dev`로 본 개발이 완료된 상태 (또는 동등한 코드 존재)
- 본 프로젝트의 `docs/spec/{년}/{월}/...`에 Spec 파일 존재
- E2E 환경이 미세팅이면 자동 세팅 진입 (e2e/ 폴더, Chrome Beta CDP 등)

## 강제 게이트

- `./e2e.sh status`로 탭 목록을 확인하고 사용자가 실행 탭을 지정하기 전에는 실행 명령(`./e2e.sh run`, `agent-browser eval`, 탭 전환)을 시작하지 않는다.
- 단, `peach-team-dev` 자동 chain으로 호출되고 handoff contract에 `e2e_tab`과 유효한 preflight 결과가 있으면 해당 값을 사용한다. 이 경우 Chrome Beta/CDP/탭/세션을 다시 사용자에게 묻지 않는다.
- Google 로그인, OAuth, 관리자 콘솔, 결제, 기존 Chrome Beta 프로필 세션 유지가 핵심인 작업은 시나리오 생성/분석까지만 진행하고, 실제 실행은 사용자 확인 후 시작한다.
- `agent-browser` 디버깅이 비정상이면 OS 레벨 브라우저 우회(`open -a`, 다른 브라우저, 다른 프로필 경로)를 하지 않는다.
- 로그인/2차 인증은 사용자가 Chrome Beta 고정 프로필에서 먼저 인증을 완료하도록 안내한다.

## 워크플로우

### Reference 선택

| 상황 | 읽을 reference |
|------|----------------|
| 팀 구성 자동 분석 | `references/runtime-team-selection.md` |
| Claude/Codex 실행 모드 선택 | `references/runtime-adapter.md` |
| E2E 환경 미세팅 | `references/e2e-setup-흡수.md` |
| team-dev 자동 chain/handoff 재사용 | `../peach-team-dev/references/dev-e2e-chain.md` |
| Spec/proto 검증 기준 로드 | `references/검증기준-로드.md` |
| 단위 시나리오 작성/검증 | `references/scenario-dev-agent.md`, `references/scenario-qa-agent.md` |
| 통합 suite 생성/실행 | `references/suite-dev-agent.md`, `references/suite-qa-agent.md` |
| 실패 원인 분류 | `references/미스매치-분류.md` |
| 코드 수정 위임 | `references/delegation-policy.md` |
| QA 판정/완료 보고 | `references/qa-policy.md` |

### 0. 입력 검증

#### 런타임 모드 선택

먼저 `references/runtime-team-selection.md`와 `references/runtime-adapter.md`를 읽고 팀 구성과 실행 모드를 정한다.

| 조건 | 모드 |
|------|------|
| Claude Code 팀 도구 사용 가능 | Claude team mode |
| Codex subagent 도구 사용 가능 | Codex subagent team mode |
| 서브에이전트 도구 없음 | generic role-queue |
| Claude Code지만 팀 기능 비활성 | team mode 활성화 안내 후 generic role-queue 가능 여부 확인 |

`skills.sh`는 설치 방식이며 Codex에서 에이전트 팀 사용 가능 여부를 결정하지 않는다. Codex 런타임에 `spawn_agent`, `wait_agent`, `send_input` 같은 서브에이전트 도구가 있으면 Codex subagent team mode를 사용할 수 있다. 서브에이전트 도구가 없을 때만 generic role-queue로 실행한다.

사용자가 `team-e2e`, `팀 e2e`, `최종 검증`을 명시하면 먼저 E2E 범위 분석을 수행한다. 시나리오 분할, suite 구성, QA 독립성, 브라우저/데이터 준비 복잡도에 따라 `single-agent / role-queue / agent-team` 중 하나를 선택한다. agent-team이 적절하지만 불가하면 시작 전에 generic role-queue 또는 single-agent 전환 사유를 보고한다.

#### 검증 기준 가용성 확인

```
spec 인자 있음 + proto 인자 있음 → 표준 검증 모드 (Spec + ui-proto)
spec 인자 있음 + proto 인자 없음 → Spec-only 검증 모드
spec 인자 없음 + 단일 시나리오 재실행/디버깅 요청 → Tier 2 스킬 안내
spec 인자 없음 + 통합/부합 검증 요청 → 검증 중단, peach-gen-spec 또는 Spec 보강 안내
```

Spec-only 검증 모드 진입 시 완료 보고에 다음을 남긴다.

- 검증 신뢰도: `중간`
- 강한 검증: 비즈니스 규칙, 데이터 정확성, 에러/예외
- 약한 검증: 화면 레이아웃, 컴포넌트 배치, 세부 인터랙션 흐름
- 보강 권고: 신규 복잡 화면이면 `peach-team-ui-proto` 작성 후 재검증

Spec이 없으면 자연어 기준이나 proto만으로 표준 E2E를 진행하지 않는다. 먼저 `/peach-gen-spec`으로 Spec을 만들거나 기존 Spec을 보강한 뒤 재진입한다.

#### Handoff contract 확인

`handoff` 인자 또는 자동 chain 입력 컨텍스트가 있으면 다음을 먼저 검증한다.

| 항목 | 처리 |
|------|------|
| `spec_path` | 현재 `spec` 인자와 다르면 기준 충돌로 보고 |
| `proto_path` | 현재 `proto` 인자와 다르면 사용자 확인 또는 Spec 기준 우선 |
| `base_url`, `api_url` | 현재 실행 대상과 다르면 재확인 |
| `e2e_tab` | 값이 있고 CDP 연결이 유효하면 탭 지정 게이트 재질문 생략 |
| `browser_context` | Chrome Beta/CDP/login_session이 `ready`면 preflight 재사용 |
| `created_data`, `test_scope` | 시나리오 fixture와 suite 검증 범위에 반영 |
| `dev_result` | TDD/lint/build/Contract Gate 결과를 실패 분류 근거로 사용 |

handoff contract가 없거나 무효하면 단독 호출로 간주하고 기존 강제 게이트를 수행한다.

#### Spec 없는 E2E 단독 재실행 요청

사용자가 이미 만들어진 E2E 시나리오나 suite를 **단독 재실행**해 달라고 요청하면, 이 스킬에 예외 모드를 추가하지 않는다. 다음 Tier 2 스킬로 안내한다.

| 요청 | 안내 스킬 | 목적 |
|------|-----------|------|
| 단위 시나리오 재실행/자동수정 | `peach-e2e-scenario` | 기존 시나리오 실행, 셀렉터/대기/문법 오류 확인 |
| 통합 suite 재실행 | `peach-e2e-suite` | 기존 suite md 실행, 실패 Step과 로그 확인 |
| 브라우저에서 실패 원인 확인 | `peach-e2e-browse` | 화면 상태, DOM, 콘솔, 네트워크 탐색 |
| E2E 환경 점검 | `peach-e2e-setup` | e2e 폴더, Chrome Beta, CDP 연결 확인 |

이 경로는 **기술적 실행 오류 확인**용이다. Spec 부합, 비즈니스 규칙, 권한/상태/데이터 정확성까지 판정하려면 `peach-team-e2e spec=<경로>`로 재진입한다.

### 1. E2E 환경 세팅 (필요시)

`e2e/`, `agent-browser`, Chrome Beta, CDP 연결을 확인한다. 도구는 자동 설치하지 않고 사용자에게 안내한다. 프로젝트 내부 E2E 인프라 배포와 CDP 연결 절차는 `references/e2e-setup-흡수.md`를 따른다.

handoff contract의 `browser_context`가 유효하면 이 단계는 재사용으로 처리하고 `preflight_reused: true`를 완료 보고에 남긴다.

### 2. 검증 기준 로드

표준 검증 모드는 본 프로젝트 Spec과 proto 화면 폴더를 함께 읽고 불일치를 확인한다. Spec-only 모드는 본 프로젝트 Spec만 기준으로 사용하되 시각 검증 한계와 신뢰도 `중간`을 보고한다. 상세 절차는 `references/검증기준-로드.md`를 따른다.

### 3. 팀 구성 다이어그램

```
e2e-scenario-dev ──→ e2e-scenario-qa
       │                    │
       └──→ e2e-suite-dev ──→ e2e-suite-qa
                              │
                              └──→ 실행 + 미스매치 분류
                                          │
                                          └──→ (분류 결과 기반 보완 루프)
```

| 역할 | 책임 | references |
|------|------|-----------|
| e2e-scenario-dev | 단위 시나리오 자동 분할 + 작성 | references/scenario-dev-agent.md |
| e2e-scenario-qa | 단위 시나리오 문법 + 단독 실행 검증 | references/scenario-qa-agent.md |
| e2e-suite-dev | 단위 시나리오 조합 + suite md 생성 | references/suite-dev-agent.md |
| e2e-suite-qa | suite 실행 + ui-proto/Spec 부합 검증 | references/suite-qa-agent.md |

오케스트레이터(이 스킬)가 각 역할의 결과를 받아 다음 단계로 분배한다.

### 4. 팀 생성 및 작업 등록

Claude team mode에서는 다음처럼 팀을 생성한다. Codex 환경에서도 team-by-analysis 결과 agent-team이 적절하고 `spawn_agent`, `wait_agent`, `send_input` 같은 서브에이전트 생성/대기/전달 수단이 있으면 e2e-scenario-dev, e2e-scenario-qa, e2e-suite-dev, e2e-suite-qa를 실제 별도 작업자로 분리한다.

단독 순차 실행은 분석상 소규모이거나, 도구 미가용이거나, 사용자가 `team=off`를 지정한 경우에 사용한다. generic role-queue는 실제 팀 도구 없이 같은 순서를 역할 체크리스트로 실행하는 모드다.

```
TeamCreate: team_name="[기능명]-e2e-team"

TaskCreate:
1. "단위 시나리오 분할 작성" (owner: e2e-scenario-dev)
2. "단위 시나리오 검증" (blockedBy: Task1, owner: e2e-scenario-qa)
3. "통합 suite 생성" (blockedBy: Task2, owner: e2e-suite-dev)
4. "통합 suite 실행 + 부합 검증" (blockedBy: Task3, owner: e2e-suite-qa)
```

### 5. 단위 시나리오 자동 분할

검증 기준에서 사용자 액션 단위로 시나리오를 분할한다. 단일 책임, 데이터 의존성 표시, 재사용성, 실패 격리를 기준으로 한다.

단위 시나리오 작성 원칙(단일 책임/시작 데이터 자체 준비/독립 실행/재활용 가능/실패 격리)의 SoT는 `peach-e2e-scenario/SKILL.md` "단위 시나리오 작성 원칙" 섹션이다. team-e2e는 분할 판단 시 이 원칙을 따른다. 분할 후 에이전트 워크플로우 상세는 `references/scenario-dev-agent.md`와 `references/scenario-qa-agent.md`를 따른다.

### 6. 통합 suite 자동 생성

단위 시나리오를 비즈니스 흐름 단위로 조합해 `docs/e2e-suite/{한글카테고리}/{NN}-{스위트명}.md`를 생성한다. 폴더/순번 규칙과 점진 이전 정책은 `peach-e2e-suite/references/suite-scenario-파일구조.md`를 SoT로 따른다.

suite 구성 시 단위 .js는 재활용 부품으로 다루며 suite에서 직접 수정하지 않는다. 단위 재활용 원칙의 SoT는 `peach-e2e-suite/SKILL.md` "단위 시나리오 재활용 원칙" 섹션이다. suite 구조와 검증 포인트 작성 에이전트 워크플로우는 `references/suite-dev-agent.md`와 `references/suite-qa-agent.md`를 따른다.

### 7. 실행 + 미스매치 분류

suite md를 순차 실행하면서 각 Step의 결과를 검증 기준과 대조한다.

실패 시 **5가지로 분류**한다.

| 분류 | 원인 | 처리 |
|------|------|------|
| **(a) Spec 비즈니스 규칙 위반** | 본 프로젝트 코드가 Spec과 다르게 동작 | 안전 조건 만족 시 handoff context와 함께 `peach-team-dev` 자동 위임 |
| **(b) ui-proto 화면 흐름과 다름** | 본 프로젝트 화면이 ui-proto와 다르게 구현됨 | 안전 조건 만족 시 handoff context와 함께 `peach-team-dev mode=ui` 자동 위임 |
| **(c) 시나리오 자체 오류** | 시나리오 코드의 셀렉터/로직 오류 | 시나리오 수정 (e2e-scenario 자동수정 패턴) |
| **(d) suite 구성 오류** | Step 순서, 데이터 전달, fixture, 검증 포인트 조합 오류 | suite md 수정 후 실패 지점부터 재실행 |
| **(e) 환경 문제** | 서버, 브라우저, 탭, 세션, 포트, 데이터 준비 문제 | `manual_retry_count`로 기록하고 필요 시 사용자 확인 |
| **(f) 기준 모호** | Spec/proto 근거 부족 또는 충돌 | 사용자 확인 또는 기준 보강 |

분류 판단:
- 검증 기준(ui-proto/Spec)에 명시된 동작과 다름 → (a) 또는 (b)
- 단위 시나리오 파일의 셀렉터/대기/문법/로직이 잘못됨 → (c)
- 단위 시나리오는 맞지만 suite의 Step 순서, 데이터 전달, fixture, 검증 포인트가 잘못됨 → (d)
- 브라우저/서버/세션/포트/fixture 준비 문제 → (e)
- 검증 기준이 부족하거나 충돌 → (f)

상세는 `references/미스매치-분류.md` 참조.

### 8. 보완 루프 (랄프루프 5/10회)

분류 결과에 따라 (a)/(b)는 안전 조건을 만족하면 handoff context와 함께 `peach-team-dev`로 자동 위임하고, (c)는 시나리오 자동수정을 수행한다. (d)는 suite md를 수정하고 실패 지점부터 재실행한다. (e)는 Manual Retry로 기록하고 환경 보정 후 재실행하거나 사용자 확인으로 올린다. (f)는 사용자 확인 또는 `peach-gen-spec` 보강으로 분기한다. Ralph Loop와 Manual Retry는 분리해 기록한다. QA REJECTED 후 산출물 수정 및 재검증은 Ralph Loop, 브라우저/서버/세션/포트 등 환경 보정 후 재실행은 Manual Retry로 기록한다. 자동 위임 조건은 `references/delegation-policy.md`, 반복 상한과 완료 보고 기준은 `references/qa-policy.md`를 따른다.

## QA 판정 처리

QA는 `APPROVED / CONDITIONAL / REJECTED` 3단계로 판정한다. 판정 의미, 보완 루프, 완료 보고 필드는 `references/qa-policy.md`를 따른다.

## Completion

모든 검증 통과 후 단위 시나리오 실행 결과, 통합 suite 경로, 미스매치 이력, 검증 기준 부합 결과를 수집한다.

```
SendMessage(shutdown_request) → 모든 팀원에게
TeamDelete → 팀 정리
```

generic role-queue에서는 위 팀 정리 단계 대신 실행 이력과 산출물 경로를 완료 보고에 남긴다.

## 완료 보고 형식

완료 보고는 `references/qa-policy.md`의 필드를 따른다. 자동 chain 호출이면 `chain_source`, `handoff_used`, `preflight_reused`, `e2e_result`, `failure_classification`을 반드시 포함한다. Spec-only 모드는 검증 한계와 사후 보강 권고를 반드시 포함한다.

## Examples

```bash
# === 표준 모드 (proto 사용) ===

# proto 경로로 검증 기준 자동 로드
/peach-team-e2e spec=docs/spec/2026/05/example.md proto=<PROTO_REPO>/src/modules-task/2604/260427-<initial>-goods

# opus 모델로 서브에이전트 실행
/peach-team-e2e spec=docs/spec/2026/05/example.md proto=<PROTO_REPO>/.../260427-<initial>-goods model=opus

# === Spec-only 모드 ===

# proto 없이 docs/spec/... 만 사용
/peach-team-e2e spec=docs/spec/2026/05/example.md
```

## 도구 역할 분담

| 용도 | 도구 |
|------|------|
| 단위 시나리오 실행 | `./e2e.sh run` |
| 검증 포인트 확인 | `agent-browser eval` |
| 코드 검증 | Read, Grep |
| DB 검증 | peach-db-query 또는 직접 SELECT |
| iframe 검증 | `./e2e/pwc.sh eval` (fallback) |

## 관련 스킬

- `peach-team-dev` — 본 개발 (이 스킬의 선행 단계)
- `peach-e2e-setup` — E2E 환경 단독 세팅 (Tier 2)
- `peach-e2e-scenario` — 단위 시나리오 단독 작성/실행/재실행/자동수정 (Tier 2)
- `peach-e2e-suite` — 통합 suite md 단독 생성/실행/재실행 (Tier 2)
- `peach-e2e-browse` — 브라우저 탐색/디버깅 (검증 중 보조)

> 이 스킬은 위 4개 e2e-* 스킬과 **같은 가이드 패턴을 공유한다**.
> 진짜 SoT는 시나리오 코드 패턴(`peach-e2e-scenario/references/`)과 e2e 인프라 코드(`peach-e2e-setup/references/`).
> Tier 2 스킬과 본 스킬은 같은 패턴을 두 가지 호출 방식으로 사용한다.
> `browse/scenario/suite`는 병합 대상이 아니라 연결 대상이다. 수명주기가 다르므로 Tier 2 단독 호출성을 유지한다.

| 스킬 | 수명주기 |
|------|----------|
| `peach-e2e-browse` | 일회성 탐색/디버깅 |
| `peach-e2e-scenario` | 반복 가능한 단위 회귀 검증 |
| `peach-e2e-suite` | 업무 흐름 단위 통합 검증 |
| `peach-team-e2e` | Spec/ui-proto 기준 최종 부합 검증 |

## 핵심 원칙

- 검증 기준은 **Spec 필수 + ui-proto 보조**로 외부화 (코드 동작 검증을 넘어 기획 의도 부합 검증)
- 비즈니스/데이터/권한/상태/예외는 Spec이 1차, 화면/흐름은 proto가 있으면 proto를 보조 기준으로 사용
- 미스매치는 **5가지로 분류** (Spec 위반 / proto 불일치 / 시나리오 오류 / suite 구성 오류 / 기준 모호)
- 코드 수정은 안전 조건을 만족하면 `peach-team-dev`로 자동 위임하고, 기준 모호만 사용자에게 보고
- 시나리오 수정은 **3회 자동수정** (peach-e2e-scenario 패턴)
- suite 구성 오류는 suite md를 수정하고 실패 지점부터 재실행
- 랄프루프 상한 5/10회 (변경 규모 기반)
- 검증 기준이 없거나 모호하면 **사용자에게 보고**, 강제 진행 금지
