---
name: voxel-selfie-avatar
description: >-
  Converts a selfie or a text character description into a high-saturation 3D
  voxel chibi via RunningHub (accio1 static from photo or accio1 text-to-image,
  then accio2 action), then locally cuts out and composes a circular gradient
  transparent PNG avatar. Use when the user uploads a selfie, provides a
  character text prompt, or asks for 像素小人, 体素小人, 抠图, 圆形头像,
  RunningHub, accio, MagicaVoxel, or this blocky toy avatar style.
---

# 自拍或文字 → 无动作静态 → 选图 → accio2 动作 → 圆形透明头像

## 何时使用

- 用户上传自拍，要做体素小人圆形头像
- 用户上传文字描述，要做体素小人圆形头像
- 只要跑 RunningHub 某一段，或只要本地抠图进圆

## 启动时必须先确认输入

用户说「运行 skill」但**既没有自拍、也没有角色文字**时：不要立刻调 RunningHub。只发下面这段引导，不要附加工作流名称、缺项默认或实现说明。

请选一种输入：

1. 上传照片
2. 上传文字

文字模板：性别/人种/发型/发色/眉毛色/是否有胡子/服饰穿搭类型……。

内部路由（不要写给用户）：自拍 → `workflows.static`；文字 → `workflows.staticText`。

## 文字缺项默认（写入节点前补全，不要写进引导）

- 如果用户的输入文字不包含任何的裤子，那么默认黑色、灰色、白色三种颜色其中一种与其他一种纯色的拼色长裤或者七分裤
- 如果识别不到任何的鞋子，那么默认黑色、灰色、白色三种颜色其中一种与其他一种纯色的拼色运动鞋
- 如果识别不到任何的衣服，那么黑色、灰色、白色三种颜色其中一种与其他一种纯色的拼色卫衣或者短袖或者夹克
- 如果识别不到任何的发色眉毛色，那么默认黑色

脚本 `text_prompt.py` / `pipeline.py --prompt` 会自动补这些默认；Agent 也可先补全再传入。

## 端到端流程（必须按序）

1. **确认配置**：读 [config.local.json](config.local.json)（或 `config.example.json` 复制后填写）。需要：
   - `apiKey`
   - `workflows.static.workflowId`（accio1+无动作，自拍）
   - `workflows.staticText.workflowId`（accio1+无动作+文字生图）
   - `workflows.action.workflowId`（accio2+有动作）  
   `workflowId` 来自网页地址栏 `/#/workflow/<数字>`。API 说明见 [runninghub.md](runninghub.md)。
2. **stage1 · 无动作**：
   - 自拍 → 节点「用户上传图片」(`nodeId=40`)，跑 accio1
   - 文字 → 节点「用户上传文字」(`nodeId=11`, `fieldName=text`)，跑文字生图  
   下载全部输出（通常 2～3 张）。
3. **用户挑选**：把候选图展示给用户，问选哪一张（或 `--pick-index`）。**必须先弹出预览，再问选哪张。**
4. **stage2 · 有动作**：把选中图交给节点「用户上传图片」(`nodeId=11`)，跑 accio2，得到 1 张动作白底图。
5. **本地合成**：`compose_circle.py` 抠白底 + 随机/指定渐变 + 圆形蒙版，圆外透明。
6. **交付**：只交最终 `*_circle.png`；附带用了哪条渐变 id。同样必须弹出预览。

```bash
python3 .cursor/skills/voxel-selfie-avatar/scripts/pipeline.py stage1 \
  --selfie /path/selfie.jpg --out-dir ./voxel_out

python3 .cursor/skills/voxel-selfie-avatar/scripts/pipeline.py stage1 \
  --prompt '女/亚洲/短发/黑发/黑眉/无胡子/休闲卫衣' --out-dir ./voxel_out

python3 .cursor/skills/voxel-selfie-avatar/scripts/pipeline.py stage2 \
  --out-dir ./voxel_out --pick-index 1
```

Agent 在对话里：跑完 stage1 后必须停下来让用户选图，再跑 stage2。

## 图片预览（必须，不可跳过）

所有产出共用**同一个**固定汇总预览页：`voxel_out/preview.html`（近期最多 50 张，最新在前；归档在 `voxel_out/history/`）。  
禁止按对话/批次生成不同预览网址；禁止只报路径、禁止等用户问「预览呢」。

1. `pipeline.py` / `compose_circle.py` 每次出图后更新并打开该固定页（缩略图、点击大图、保存）。
2. Agent 仍须立刻对**每一张**新图做完下面三件事，再开口问用户：
   - 调用 `open_resource`，URI 为 `file://` + 绝对路径（空格写成 `%20`）；也可打开固定的 `preview.html`
   - `Read` 该图片，让对话里出现内嵌预览
   - 回复里用 markdown：`![候选N](相对路径)`
3. **每次图片产出后的回复末尾必须附带同一条可点击预览链接**（汇总近期最多 50 张），格式固定：
   - `[打开图片预览（近期最多50张）](file:///绝对路径/voxel_out/preview.html)`
   - 路径中的空格写成 `%20`；以脚本打印的 `[preview] markdown:` 行为准
4. 时机：
   - stage1：全部候选图（通常 2～3 张）
   - stage2：动作图 + 最终 `*_circle.png`
   - 仅本地抠图进圆：最终 `*_circle.png`

## 固定参数

见 [layout.json](layout.json)、[gradients.json](gradients.json)。

| 项 | 值 |
|----|----|
| 动作图期望 | 2048×2048 白底 |
| 输出头像 | 1000×1000，圆外透明 |
| 裁切（相对动作图） | 顶 80 / 左 524 / 右 524 / 底 968，直径 1000 |
| 渐变 | `g01`…`g12`，冷暖各 6 条；默认按色系均匀随机，并避开上一次的冷/暖 |

## 仅本地抠图进圆（跳过 RunningHub）

```bash
python3 .cursor/skills/voxel-selfie-avatar/scripts/compose_circle.py action.png -o out_circle.png
```

## 提示词备份

工作流内已含提示时，以网页工作流为准。本地备份：

- [prompt-static.md](prompt-static.md)
- [prompt-action.md](prompt-action.md)
- [workflows/accio1-static-text.json](workflows/accio1-static-text.json)（文字生图工作流）

硬约束：高饱和、四指手、四方耳、头身比 1:1.5、下颌左右各 3 块转折。

## 依赖

```bash
python3 -m pip install -r .cursor/skills/voxel-selfie-avatar/requirements.txt
```

## 安全

- 密钥只放本机 `config.local.json` 或环境变量 `RUNNINGHUB_API_KEY`，不要写进公开仓库、不要打进提交包
- 提交前用 `./pack.sh` 打包（会排除 `config.local.json`、`.DS_Store`、`__MACOSX/`、`voxel_out/`）
- 当前环境若拦 `runninghub.cn`，请在用户本机终端跑 `pipeline.py`
