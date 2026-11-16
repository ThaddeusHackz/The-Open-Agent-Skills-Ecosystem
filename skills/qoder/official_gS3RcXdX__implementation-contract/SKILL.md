---
name: implementation-contract
description: Use when codex Orchestra delegates an implementation task to opencode or claude-code, or when an implementation agent needs to validate task boundaries, completion requirements, branch/PR targets, stop conditions, and handoff details.
---

# implementation-contract

実装 task の作業契約を明文化するための skill。root `AGENTS.md` / `CLAUDE.md` は恒久ガードに留め、task 固有の完了条件は Issue 本文または委譲プロンプトを正とする。

## いつ使うか

- codex Orchestra が `agent:opencode` / `agent:claude-code` に task を委譲するとき
- 実装 agent が着手前に Issue が implementation-ready か確認するとき
- 作業途中で Scope 外変更、仕様判断、正本変更が必要になったとき
- 完了報告前に commit / push / PR 作成 / clean 確認の要否を確認するとき

## 委譲時に必ず渡す契約

Orchestra は委譲プロンプトまたは Issue 本文に次を明記する。

- 対象 Issue / Story
- 作業 branch と PR target
- Goal
- Scope
- Out of Scope
- Acceptance Criteria
- Verification
- Stop Conditions
- Source of Truth
- Generated Artifacts
- 完了時に commit / push / PR 作成 / clean working tree 確認まで求めるか

明示が無い場合、実装 agent は commit / push / PR 作成まで行い、PR merge / Issue close / cleanup は人間に残す。

## Stop Conditions

最低限、次を含める。

- Scope 外ファイル / Scope 外領域の変更が必要になった場合
- 仕様、優先度、対象ユーザー、期待挙動の判断が必要になった場合
- セキュリティ / プライバシー / コストに影響する判断が必要になった場合
- Acceptance Criteria の変更が必要になった場合
- 1 PR で閉じないと分かった場合
- DB スキーマ、データモデル、API contract、認可モデル、課金モデル、イベント仕様、外部連携 mapping などの正本変更が必要になった場合

Stop Condition に当たったら実装を広げない。状況、必要な判断、影響範囲、提案する後続 Issue を親 Issue または完了報告に残す。

## Agent 別の完了条件

### agent:opencode

- story 外の単発 PR として扱い、起点 / PR target は repo の `<trunk>` に揃える
- 単一ファイル / 単一関数、10 行未満、近傍コード参照不要の超小粒 task に限る
- テスト追加・修正は原則しない
- 期待 diff が文章 1 行で書けること

### agent:claude-code

- opencode で扱えない実装、テスト設計、技術調査、横断変更を担当する
- 委譲された Issue の Goal / Scope / Acceptance Criteria / Out of Scope / Stop Conditions を作業契約として扱う
- Story / Epic / 要件整理を実装 task として進めない
- task branch は、story 配下なら `story-NN` 起点かつ PR target も `story-NN`
- story 外の hotfix / 単発 task は `origin/<trunk>` 起点かつ PR target も `<trunk>`
- `<trunk>` は `git symbolic-ref --short refs/remotes/origin/HEAD | sed 's@^origin/@@'` で解決する。空なら `git remote set-head origin --auto` 後に再判定し、まだ空なら人間判断へ戻す

## codex の扱い

codex は story 分解、orchestration、PR review、Issue / PR 整理に専念する。実装 task の担当 agent として `agent:codex` を付けない。

## Agent ラベル契約

- `agent:*` は 1 Issue につき 1 個だけ付ける
- `agent:codex` は PO 整理、story 分解、orchestration、PR review、needs-refinement の再整理に限る
- implementation-ready な task にする時点で、`agent:codex` は `agent:claude-code` または `agent:opencode` に置き換える
- `agent:*` を付け替えるときは、変更前に想定される既存 `agent:*` を同時に外し、重複状態を残さない
- story 配下 task は `agent:claude-code` に統一し、`agent:opencode` は story 外の単発 PR lane だけに使う

## 完了報告

完了報告には次を含める。

- 対象 Issue
- 作業 branch
- PR URL
- 変更ファイル
- 実行した検証
- 残した後続課題
- ローカル差分の有無

「確認済み」と書けるのは実際に実行した検証だけ。実行できない場合は「未検証」と理由を書く。

## 落とし穴

- root `CLAUDE.md` に task 固有の完了条件を固定しない
- 調査 task と実装 task を混ぜない
- 非 Blocker の別課題を同じ PR に混ぜない
- PR の merge / Issue 更新 / cleanup は人間の手動作業として残す
