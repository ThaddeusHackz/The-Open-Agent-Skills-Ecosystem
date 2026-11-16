---
name: story-orchestrate
description: Use when codex carries a ready type:story through story branch setup, task delegation, task PR aggregation, Pre-Final E2E scenario design, final review, final PR, and human handoff. Use story-breakdown before this when tasks are not implementation-ready.
---

# story-orchestrate

採用された 1 story を持ちきる Orchestra の手順。root `AGENTS.md` / `CLAUDE.md` には概要だけを置き、Story-level branch、Pre-Final review、Final review、hotfix 例外の詳細はこの skill を正とする。task 分解は `story-breakdown` skill を正とし、この skill では ready な story を最後まで運ぶ。

## いつ使うか

- `story-breakdown` 済み、または ready 状態の `type:story` Issue を Orchestra として開始するとき
- 進行中 story の task PR が merge されたあとの集約フェーズ
- E2E シナリオ設計 task を Pre-Final review で起動するとき
- final review → 人間 handoff まで進めるとき

## いつ使わないか

- `agent:opencode` 単発 task → `story-NN` を経由しない (`<trunk>` 直接 PR)
- `type:task` 単独で picked された場合 → story を作らず直接実装フローへ

## 担当判定

- Orchestra は **codex 専任**。claude-code は Orchestra を担わず、story 分解 / 委譲 / final review aggregation などの判断は codex が行う。
- codex で扱いきれない story（横断・設計判断主体で 1 PR に閉じない、Open Questions が残る、正本変更や高リスク領域に触れる）は実装委譲せず、人間判断へ戻す。

## フェーズ

### Phase 1: story の確認と branch 作成

1. story Issue を `github-read` で読み、Goal / Acceptance Criteria / Out of Scope を確定する
2. 進行中 story が他に無いことを確認する (同時 1 story の原則)
3. trunk を判定: `git symbolic-ref --short refs/remotes/origin/HEAD | sed 's@^origin/@@'`
   - 空なら `git remote set-head origin --auto` 後に再判定する。まだ空なら `TRUNK=<branch>` を人間判断で明示する
4. `git fetch origin` のうえ `story-<NN>` を `origin/<trunk>` 起点で作成 (NN は story Issue 番号)
   ```bash
   git fetch origin
   git switch -c story-<NN> origin/<trunk>
   git push -u origin story-<NN>
   ```
   最初の task PR は `story-<NN>` を base にするため、task 委託前に remote branch を作成しておく。

### Phase 2: task 確認と委託

1. `story-breakdown` の出力または story Issue 本文を読み、配下 task が implementation-ready であることを確認する
2. task が不足、粒度不適切、Open Questions 残りの場合は orchestration を止め、`story-breakdown` に戻す
3. E2E シナリオ設計 task が無い場合は `story-breakdown` に戻して起票する。起動は Pre-Final review まで待つ
4. 実装 agent へ委託する前に `implementation-contract` を使い、作業 branch / PR target / Scope / Out of Scope / Acceptance Criteria / Verification / Stop Conditions / 完了時に PR 作成まで求めるかを明示する
5. 委託先別の起動:
   - `agent:claude-code` → claude CLI を起動して委譲。Claude Code の Agent tool を使う場合は `isolation: worktree` と必要な `skills:` を明示する
   - `agent:opencode` → opencode CLI を起動。**ただし opencode 単発 task は `<trunk>` 直接消化なので story 配下には入れない**
6. task は default sequential。完全独立で conflict が出ない場合のみ Orchestra が明示的に並列許可する
7. codex は実装 CLI として自分自身を再委譲しない。実装は `agent:opencode` または `agent:claude-code` に委譲する

### Phase 3: task PR の集約

1. task PR は `story-<NN>` を base にして作成される (実装 agent が `github-write` 経由で作成)
2. 両 reviewer (codex / claude-code) の review PASS を待つ
3. 必須チェック通過、レビュー状態、対象 Issue、head commit、差分範囲を確認
4. 条件を満たしたら **merge 候補**として人間に報告。merge 実行は人間が行う (Orchestra は `gh pr merge` を実行しない)

### Phase 4: trunk 追従

`story-<NN>` が長期化すると drift が出る。Orchestra が定期的に `<trunk>` を取り込む:

```bash
git switch story-<NN>
git fetch origin
git merge origin/<trunk>     # conflict 解消は Orchestra が実施
git push
```

merge / cherry-pick / rebase の途中状態を残さない (`git status` で確認)。

### Phase 5: Pre-Final review

E2E シナリオ設計 task 以外の `story-NN` 配下 task PR がすべて merge されたら Pre-Final review に入る。final story PR の作成有無は Pre-Final review の開始条件にしない。

1. E2E シナリオ設計 task を `agent:claude-code` へ委託し、起動プロンプトで `e2e-scenario-design` skill の使用を明示する。Claude Code subagent を使う場合は `skills: [e2e-scenario-design, github-read, github-write]` と `isolation: worktree` を指定する
2. 出力は `specs/qa/<feature>.md` / `specs/manual/<feature>.md` と story Issue 本文 `Test Design`
3. spec から派生する QA Generator / Manual Generator / Manual 散文 task が必要なら起票し、実装・merge する
4. QA E2E / User Manual に影響が無い、または既存 spec / tests / Manual で追加・変更が不要と判断できる場合は、理由を `Test Design` に残して E2E シナリオ設計 task を close してよい
5. 派生 task が merge されるまで Final review へ進まない

### Phase 6: Final review

`story-<NN>` 配下の全 task PR が merge されたら final review に入る。

1. **Claude Code を reviewer として別 worktree / 別セッションで起動**し、`story-<NN>` の全体差分を再点検
   - 起動プロンプトには story Issue URL、base/head 範囲、使用 skill (`github-read`, `implementation-contract`) と root `CLAUDE.md` の review 指示を明示する
   - spec の frontmatter `story:` を起点に、QA spec から派生した実際の実装テストパスと、Manual spec から派生した実際の生成テスト / 出力パスのカバレッジを確認する。`tests/qa/` や Playwright 固定を仮定せず、repo の既存 test stack に合わせる
   - User Manual 差分が当該 story に紐付いた spec と reporter 出力に限定されているか監査する
   - 親 conversation の skill preload に依存せず、起動時に必要な skill と isolation を明示する
2. **Orchestra 自身も** `story-<NN>` 全体を再点検する (claude-code への二重チェック)
3. 両 review 結果を Orchestra が集約し、残存懸念を抽出
4. Go/No-Go 判断材料と懸念リストを人間に提示

### Phase 7: final PR と人間 handoff

1. `story-<NN>` から `<trunk>` への final PR を通常 PR として作成 (`github-write`)
   - 通常は最初の task PR が `story-<NN>` に merge された直後に作成し、以後は story 全体の進捗・差分確認の固定導線として扱う
   - title は story Issue タイトル
   - 本文の `Closes #<NN>` で auto close
   - 本文に final review 集約結果と Go/No-Go 推奨を含める
2. Go の場合、人間が merge 判断できる状態として final PR と判断材料を提示する
3. リリース承認は人間判断。Orchestra は `gh pr merge` しない
4. No-Go の場合は blocker を task として `story-<NN>` に追加し Phase 2 に戻る

## hotfix 例外

進行中 story がある状態で hotfix が必要になった場合はこの節に従う。

- 緊急性が低い: 進行中 story を pause、hotfix を新規 story として pick
- 即時必要: `<trunk>` 直接の単発 task として処理 (`story-NN` を経由しない)

## opencode 単発 task

`agent:opencode` の単発 task は、進行中 story の有無に関わらず `<trunk>` 直接の PR として消化する。story-level branch と final review は使わない。merge 可否判断は Orchestra が行い、merge 実行は人間に委ねる。

## 落とし穴

- task PR を **`<trunk>`** 向けに作らせない (`story-<NN>` が base)
- merge 候補と merge 実行を混ぜない (実行は人間)
- final review を Orchestra 単独で済ませない (claude-code holistic review が必須)
- Story の寿命が **1 週間**を超えたら強制再評価。分割か scope 縮小を判断する
- codex で扱いきれない story (横断・設計判断主体で 1 PR に閉じない、正本変更や高リスク領域に触れる) を Orchestra が無理に進めない (人間判断へ戻す)
