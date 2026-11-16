---
name: github-write
description: GitHub に書き込むときに使う共通 skill。Issue 起票・更新・コメント、PR 作成・コメント・review コメント返信・review thread resolve、ラベル整合を gh CLI と GraphQL でまとめて扱う。読み取りは github-read を使う。
---

# github-write

GitHub の状態を変える操作の取り口。読み取りは `github-read`、PR コメント返信のフローは `pr-comment-resolve` を参照。

## いつ使うか

- 新規 Issue を起票する (codex の PO 整理 / 後続 Issue 切り出し)
- 既存 Issue / PR にコメント、ラベル付け替え、close
- PR を作成する (task PR / final PR / hotfix)
- review コメントへ返信 / review thread を resolve する

## 起こさない操作

- `gh pr merge` は実行しない。merge は人間判断
- `gh pr merge --auto` も実行しない
- remote branch の削除は実行しない

実行前提は root `AGENTS.md` / root `CLAUDE.md` の managed block と managed block 外の local rule を見る。PR merge は人間判断で、AI agent は `gh pr merge` / `gh pr merge --auto` を実行しない。

## Issue 起票

```bash
gh issue create \
  --title "<日本語タイトル>" \
  --label "type:task,agent:claude-code" \
  --body-file <(cat <<'MD'
## 概要
...
## Acceptance Criteria
- [ ] ...
MD
)
```

- ラベルは Issue テンプレート (`.github/ISSUE_TEMPLATE/`) と整合させる。`agent:*` は 1 個のみ
- 起票直後に URL とラベルをユーザーに報告する
- `Refs #<親>` / `Split off to #<親>` を本文に書いて親子関係を残す (codex の起票規約)

implementation-ready な Issue 本体は、Goal / Scope / Acceptance Criteria / Out of Scope / Verification / Stop Conditions / Source of Truth / Generated Artifacts を含める。作業契約は `implementation-contract` skill に合わせる。

## Issue 更新

```bash
gh issue comment <NN> --body "..."
gh issue edit <NN> --add-label agent:claude-code --remove-label "agent:codex,agent:opencode"
gh issue edit <NN> --add-assignee <user>
gh issue close <NN> --reason completed
```

ラベル付け替え時は `implementation-contract` の Agent ラベル契約に従う。既存の `agent:*` を外し、重複を残さない (1 Issue = 1 担当 agent)。

## PR 作成

```bash
gh pr create \
  --base <story-NN | <trunk>> \
  --head <task-branch> \
  --title "<Issue タイトル>" \
  --body-file <(cat <<'MD'
## 変更内容
...

## 確認
- [ ] ...

## 関連 Issue
Closes #<NN>
MD
)
```

- target は `story-orchestrate` skill の branch / PR target 契約に従う (task PR → `story-NN`, final PR → `<trunk>`, opencode 単発 → `<trunk>`)
- title は原則 Issue タイトルそのまま。Issue が無い場合だけ短い日本語タイトル
- 本文は日本語、見出しは `変更内容` / `確認` / `関連 Issue`
- `Closes #NN` だけは英語 keyword (auto close に必要)

## PR コメント / review reply / resolve

### 通常の PR コメント (会話タブ)

```bash
gh pr comment <NN> --body "..."
```

### Review thread への返信

```bash
gh api repos/<OWNER>/<REPO>/pulls/<NN>/comments \
  -f body="..." \
  -F in_reply_to=<comment_database_id>
```

`in_reply_to` には review コメントの **数値 ID** (`databaseId`) を渡す。Node ID ではない。`github-read` の GraphQL クエリで取れる。

### Review thread を resolve

```bash
gh api graphql -f query='
mutation($id:ID!){ resolveReviewThread(input:{threadId:$id}){ thread{ isResolved } } }
' -F id=<thread_node_id>
```

`threadId` は **Node ID** (例: `PRRT_xxx`)。`databaseId` では resolve できない。読み取りは `github-read` の `reviewThreads` クエリで `id` を取る。

resolve は「議論済みかつ反映済み」のときだけ行う。指摘を後続 Issue に切り出した場合は、Issue URL を返信に書いてから resolve する。

## ラベル整合

ラベルはこのリポジトリ自身が正本。新しいラベルを定義した、または既存ラベルの description を変えた場合は `gh label create` / `gh label edit` で default branch 側に反映する。

```bash
gh label list --limit 100 --json name,description,color
gh label edit "agent:codex" --description "Codex lane (PO, Story Breakdown, Story Orchestra, and PR review; not implementation)"
gh label create "agent:claude-code" --description "..." --color BFD4F2
```

ラベル変更は **元の正本ファイルを更新する PR** とセットで行う。description だけを CLI で書き換えて差分を残さない。

## 落とし穴

- `--label` は **既存ラベルだけ**を許す。未定義ラベルを渡すと失敗する。先に `gh label list` で確認
- `gh pr create --base` の指定漏れで default branch 向けに作ると story 配下 task PR の集約先を誤る
- `gh issue close` は Issue 本文を変えない。完了報告 / リンクを残したい場合は先に `gh issue comment`
- `in_reply_to` のないコメント API は新規 thread を作る。会話の続きにしたい場合は必ず `in_reply_to` を渡す
- resolve は不可逆ではない (`unresolveReviewThread`) が、議論を打ち切る効果が強いので、相手返信前の resolve は避ける
