---
name: github-read
description: GitHub から Issue / PR / コメント / レビュー / ラベルを読み取るときに使う共通 skill。gh CLI を一次源とし、横断的な Issue / PR 棚卸しも gh の JSON / GraphQL 出力で扱う。
---

# github-read

GitHub の状態を読むときの取り口。書き込み (起票・コメント・resolve) は `github-write` に委ねる。

## いつ使うか

- 着手前に対象 Issue / PR の本文・コメント・review を確認する
- Story Orchestra が配下 task の状態 (open / closed / merged / labels) をまとめて取る
- nightly sweep で全 Issue を棚卸しする

## 一次源と分岐

| 用途 | コマンド |
|---|---|
| 単一 Issue / PR の本文 + コメント + review | `gh issue view` / `gh pr view --comments` |
| ラベル一覧 / 残タスク数の即時確認 | `gh issue list -L 200 --json number,title,labels,state,updatedAt` |
| 全 Issue / PR をまとめて棚卸し | `gh issue list -L <N> --json ...` / `gh pr list -L <N> --json ...` |
| review thread の構造 (resolve 用 thread ID 含む) | `gh api graphql` |

`gh` を一次源にする。repo-local に棚卸し用 cache script が存在する場合だけ、その repo の説明に従って使ってよい。

## 単一 Issue / PR

```bash
gh issue view <NN> --json number,title,state,body,labels,comments,assignees,milestone
gh pr view <NN> --json number,title,state,body,labels,reviews,comments,headRefName,baseRefName,mergeable,statusCheckRollup
gh pr view <NN> --comments
```

## Review thread (resolve 判定用)

review コメントへ返信したり resolve するには thread の `id` が要る。`pr-comment-resolve` skill から呼ばれる典型クエリ:

```bash
gh api graphql -f query='
query($owner:String!,$repo:String!,$number:Int!){
  repository(owner:$owner,name:$repo){
    pullRequest(number:$number){
      reviewThreads(first:100){
        nodes{
          id
          isResolved
          comments(first:50){
            nodes{ id databaseId author{login} body url path line }
          }
        }
      }
    }
  }
}' -F owner=<OWNER> -F repo=<REPO> -F number=<NN>
```

`databaseId` が `gh pr review` / `gh api .../comments` で出てくる数値 ID。`id` (Node ID) が GraphQL で resolve するのに必要。

## 横断棚卸し

Issue / PR を横断するときは、まず `gh` の JSON 出力を使う。

```bash
gh issue list -L 200 --state open --json number,title,labels,state,updatedAt,assignees
gh pr list -L 200 --state open --json number,title,labels,state,updatedAt,headRefName,baseRefName
gh pr list -L 200 --state all --json number,title,state,labels,updatedAt,mergedAt,headRefName,baseRefName
```

- `-L` は必要件数に合わせて明示する
- 出力は JSON。`jq` で絞り込む
- Open PR の即時確認は `--state open`、nightly sweep など merged PR の review thread まで見る棚卸しは `--state all` または `--state merged` を使う
- review thread や `closingIssuesReferences` は GraphQL を使う
- repo-local に cache script が存在しない場合、存在しない `scripts/*cache*` を仮定しない

## 落とし穴

- `gh issue list` の default ページサイズは 30。`-L` を必ず指定する
- `gh pr view --json comments` は **issue コメント**のみ返す。**review コメント / review thread** は別経路 (`reviews` / GraphQL `reviewThreads`)
- review thread を resolve したいなら GraphQL の `id` を取る。`databaseId` では resolve できない
- PR の `closingIssuesReferences` (auto close 連携) は GraphQL でしか取れない。本文の `Closes #NN` から推測しない
