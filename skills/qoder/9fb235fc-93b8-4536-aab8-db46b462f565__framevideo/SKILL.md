---
name: "framevideo-creator"
description: "Creates FrameVideo + Chanjing digital-human videos. Invoke when user mentions framevideo, 创作视频, 生成视频, or asks to create FrameVideo videos."
---

# FrameVideo Creator

当用户希望创建、修改或生成 FrameVideo 视频项目时，使用本 Skill。

触发词：

- `framevideo`
- `创作视频`
- `生成视频`
- `FrameVideo 视频`
- `蝉镜数字人视频`

这是执行型 Skill。信息齐全时，应实际完成环境检查、项目准备、蝉镜授权、数字人合成、composition 写入、校验、快照和渲染；不要只给用户步骤说明。

## 最高优先级规则

当用户输入包含 `framevideo`、`创作视频` 或 `生成视频` 时，必须立即启用本 Skill 的工作流。

本 Skill 只允许使用 FrameVideo CLI + 蝉镜数字人流程来创建视频。不得使用任何其他视频生成能力替代 FrameVideo。

必须先执行本 Skill 的 5 个前置条件；所有前置条件完成前，不允许创建、读取、修改或渲染任何视频内容，除非该动作是判断当前目录是否为 FrameVideo 项目所必需。

允许的 FrameVideo CLI 动作只包括本 Skill 明确列出的命令，例如：

- `npx --registry=https://registry.npmmirror.com @framevideo/cli doctor`
- `npx --registry=https://registry.npmmirror.com @framevideo/cli init <project-name> --example blank --skip-skills`
- 在 FrameVideo 项目目录中执行 `npx skills-cn add chanjing-ai/framevideo --all`
- 第 3 个前置条件或用户显式要求预览时的 `npx framevideo preview`
- `npx framevideo auth status`
- `npx framevideo auth login`
- 信息齐全后的 `npx framevideo lint / validate / inspect / snapshot / render`

特别禁止以下行为：

- 不要把“使用 framevideo 创建视频”转成“按文生视频默认路径生成短片”。
- 不要使用 `framevideo` 裸命令创建项目或渲染视频。
- 不要通过 `framevideo --help`、`framevideo -h`、`which framevideo` 探索通用 CLI 用法，除非本 Skill 明确要求的 `@framevideo/cli doctor` 失败后需要排查。
- 不要初始化“示例项目”“demo 项目”“默认项目”来满足用户的创建视频请求。

## 工作流总览

生成视频必须分为两个阶段：

1. 先完成所有前置条件。
2. 再按顺序采集生成视频所需信息。

禁止跳过前置条件直接创建视频。禁止在前置条件未完成前询问数字人、声音或脚本文案。

## 前置条件（严格约束）

必须严格按以下顺序完成 5 个前置条件。

### 1. 安装并检查 FrameVideo CLI

必须保证 FrameVideo CLI 可用。

实际执行：

```bash
node --version
ffmpeg -version
npx --registry=https://registry.npmmirror.com @framevideo/cli doctor
```

要求：

- Node.js 必须 `>=22`。
- FFmpeg 必须可用；检查阶段如果发现未安装，必须优先通过系统包管理器自动安装。
- Chrome/Chromium 必须可用；优先通过系统包管理器安装，必要时再使用 FrameVideo CLI 的 browser ensure 能力。
- 不要全局安装 `@framevideo/cli`。
- 如果 CLI 检查失败，先按可自动修复项处理；无法修复时报告错误并停止，不要继续创建视频。

FFmpeg 自动安装命令：

```bash
# macOS
brew install ffmpeg

# Ubuntu / Debian
sudo apt update
sudo apt install ffmpeg

# Windows
winget install Gyan.FFmpeg
```

自动安装后必须再次执行：

```bash
ffmpeg -version
npx --registry=https://registry.npmmirror.com @framevideo/cli doctor
```

### 2. 创建或确认 FrameVideo 项目

先判断当前目录是否已经是 FrameVideo 项目：

- 存在 `index.html` 且有 `data-composition-id`，或
- 存在 `framevideo.json`，或
- `package.json` 中包含 `@framevideo/cli`

如果当前已经在 FrameVideo 项目中，直接使用当前项目。

如果当前不处在 FrameVideo 项目路径下，必须使用 FrameVideo CLI 创建新项目：

```bash
npx --registry=https://registry.npmmirror.com @framevideo/cli init <project-name> --example blank --skip-skills
```

如果缺少项目名或项目路径，先询问用户：

```text
当前不在 FrameVideo 项目中。请提供项目创建路径和项目名称；如果不指定，我将使用当前目录下的 my-video。
```

严格禁止：

- 禁止手工创建 `index.html`、`package.json`、`framevideo.json`。
- 禁止自行拼装最小可运行 HTML 视频工程。
- 禁止在 CLI init 失败时改为手工 scaffold。

创建项目必须使用 `--example blank --skip-skills`，确保先创建空白项目，再在项目目录中单独安装 skills。只有 `@framevideo/cli init` 成功后，才算项目创建完成。

### 3. 打开并确认 FrameVideo 预览服务

规则：

- `@framevideo/cli init` 在真实交互式终端中可能会自动启动预览并打开浏览器；在 Codex、Trae Work 等 agent 的 non-TTY / CI 环境中可能不会自动打开。
- 如果 init 已经自动打开浏览器，必须从命令输出中记录本次项目的预览端口和完整 URL，不要再次打开同一个 URL。
- 如果 init 没有自动启动预览服务或没有打开当前项目预览 URL，必须进入第 2 步确认或创建成功的 FrameVideo 项目目录，只执行一次 `npx framevideo preview`。
- 从 `npx framevideo preview` 输出中记录端口和当前项目 URL，并打开该 URL 一次。
- 当前项目 URL 已打开后，不要再次执行 `npx framevideo preview`，避免重复启动进程或重复打开多个端口。
- 预览 URL 必须对应当前项目，不能复用其他项目的 localhost 页面。

### 4. 在 FrameVideo 项目目录中安装 `chanjing-ai/framevideo` 下的所有 skills

必须先进入第 2 步确认或创建成功的 FrameVideo 项目目录，再安装 `chanjing-ai/framevideo` 下的所有 skills：

```bash
cd <project-dir>
npx skills-cn add chanjing-ai/framevideo --all
```

要求：

- `npx skills-cn add chanjing-ai/framevideo --all` 必须在 `@framevideo/cli init <project-name>` 对应的项目目录下执行。
- 如果当前已经是 FrameVideo 项目，也必须在当前项目根目录执行。
- 不要在插件仓库根目录、用户工作区根目录或其他非 FrameVideo 项目目录安装这些 skills。
- 如果安装失败，报告错误并停止，不要继续进入授权或生成视频流程。
- 如果 skills 已安装，也应在项目目录中运行或确认该命令成功。

### 5. 检测蝉镜授权状态

进入 FrameVideo 项目目录后，检测蝉镜授权状态：

```bash
npx framevideo auth status
```

如果未登录或没有 token，必须强制登录蝉镜主站获取授权：

```bash
npx framevideo auth login
```

要求：

- 引导用户在蝉镜主站完成 OAuth 授权。
- 不要求用户复制 token。
- 不打印 access token / refresh token。
- 用户完成浏览器授权后，再次执行：

```bash
npx framevideo auth status
```

只有确认已登录后，才能进入生成视频流程。

## 生成视频流程

只有所有前置条件都满足后，才允许进入生成视频流程。

必须按以下顺序采集信息。

### 1. 数字人 ID

先从用户输入中解析 `person_id` / 数字人 ID。

如果用户输入不包含数字人 ID，必须主动询问用户是否需要数字人：

```text
是否需要使用数字人？
- 如果需要，请提供数字人 ID。
- 如果不需要，请明确回复“不使用数字人”。
```

规则：

- 用户提供数字人 ID 时，后续必须使用该 ID。
- 用户明确回复“不使用数字人”或“生成无数字人形象视频”时，才允许跳过数字人。
- 用户未明确确认前，不要默认生成无数字人视频。

### 2. 声音 ID

先从用户输入中解析 `voice_id` / 声音 ID。

如果用户输入不包含声音 ID，必须主动询问用户是否需要声音：

```text
是否需要使用声音？
- 如果需要，请提供声音 ID。
- 如果不需要，请明确回复“不使用声音”。
```

规则：

- 用户提供声音 ID 时，后续必须使用该 ID。
- 用户明确回复“不使用声音”时，才允许跳过声音。
- 用户未明确确认前，不要默认生成无声音视频。

### 3. 脚本文案

先从用户输入中解析脚本文案。

如果用户未提供视频文案，必须主动询问：

```text
请提供视频脚本文案。
```

脚本文案是生成视频的必需信息。没有脚本文案时，必须停止，不允许继续创建或修改视频内容。

## 信息缺失时必须停止

完成所有前置条件后，如果数字人、声音或脚本文案仍未确认，必须立即停止并向用户提问。

统一提问模板：

```text
我还需要以下信息才能继续创建视频：
1. 数字人：是否使用数字人？如果使用，请提供数字人 ID；如果不使用，请明确回复“不使用数字人”。
2. 声音：是否使用声音？如果使用，请提供声音 ID；如果不使用，请明确回复“不使用声音”。
3. 脚本文案：请提供视频脚本文案。
```

禁止行为：

- 不要创建“简短 FrameVideo 示例片”。
- 不要自行设定主题、时长、旁白、风格或示例文案。
- 不要生成占位视频、无数字人视频或默认产品宣传片。
- 不要调用子代理继续创作视频文件。
- 不要写入或修改 `index.html` 来绕过信息收集。
- 不要在用户未提供时虚构数字人、声音、脚本文案或背景音乐路径。
- 不要询问视频主题、视觉风格、风格偏好，或科技感、商务专业、活泼轻松、简约清新等选项。
- 不要询问背景音乐路径或输出文件名；只有用户主动提供时才使用。

## 合成前确认

进入合成前，必须确认：

- 数字人 ID，或用户明确确认不使用数字人。
- 声音 ID，或用户明确确认不使用声音。
- 脚本文案。
- 如果使用数字人和声音，必须确认已选定真实存在的 `figure_type`，并记录该形态的 `width` / `height`，用于决定蝉镜合成任务比例。

可选信息：

- `background_music`：背景音乐路径，仅当用户主动提供时使用。
- `output`：输出文件名，仅当用户主动提供时使用；否则使用默认值 `renders/output.mp4`。


## 生成蝉镜数字人口播素材

如果用户确认使用数字人和声音，优先使用 FrameVideo 的 Chanjing website-project flow：

- `projects/save`
- `videos/submit`
- `videos/status`
- 下载生成 MP4 到 `assets/digital-humans/`

关键规则：

- 用户提供的 `person_id` 和 `voice_id` 直接使用。
- 提交蝉镜合成任务前，必须查询并确认该数字人的真实记录，读取真实 `source`、`figures[].type`、`figures[].width`、`figures[].height`。
- 公共数字人常见 `source` 是 `common`。
- 自定义数字人常见 `source` 是 `custom`。
- `figure_type` 只能取自该数字人真实存在的 `figures[].type`。
- 禁止默认使用 `whole_body`。只有当 `figures` 列表中明确存在 `type: "whole_body"` 时，才允许使用 `whole_body`。
- 如果用户指定了形态，必须校验该形态存在于 `figures[].type`；不存在时必须停止并告知可用形态，不得自行回退到 `whole_body`。
- 如果用户未指定形态，必须从 `figures` 列表中选择第一个真实存在的形态，并使用该形态对应的 `width` / `height`。
- 如果无法获取 `figures` 或 `figures` 为空，必须停止，不允许提交蝉镜合成任务。
- 如果用错 `figure_type`，蝉镜可能在制作阶段返回 `status=40` 且 `msg` 为空。
- 合成素材应保持数字人原始比例，避免拉伸变形。
- 读取共享 OAuth 凭据，但不打印 token。
- 保存 request/response 到 `tmp/` 便于排查，但不要保存 token。
- 轮询 `videos/status`，直到 `status=30` 且存在 `video_url`。
- 失败状态 `40`、`41`、`50`、`1101`、`999` 应停止并报告。
- 下载 MP4 到 `assets/digital-humans/<name>.mp4`。

蝉镜合成任务比例规则：

- 提交 `projects/save` / `videos/submit` 前，必须根据所选 `figure_type` 对应的 `width` / `height` 决定合成项目比例。
- 如果 `height > width`，该数字人形态是竖版，必须提交 9:16 竖屏任务；禁止提交 16:9 横屏任务。
- 如果 `width > height`，该数字人形态是横版，必须提交 16:9 横屏任务。
- 蝉镜合成任务的画布比例必须与数字人形态比例一致或兼容，不得把 9:16 数字人放入 16:9 任务导致上下模糊、左右留白或主体异常缩放

如果用户明确不使用数字人或声音，跳过蝉镜数字人口播合成，改为创作无数字人/无声音的视频，并在最终回复中说明。


## 校验

```bash
npx framevideo lint
npx framevideo validate
npx framevideo inspect
```

根据结果修复所有 error。warning 可按影响判断，但交付前应尽量清理。

## 快照检查

```bash
npx framevideo snapshot . --at 2,8,16
```

检查 `snapshots/contact-sheet.jpg`：

- 数字人是否完整。
- 数字人是否未拉伸变形。
- 文字是否遮挡脸部或嘴型。
- 背景音乐不应覆盖口播。

## 渲染导出

```bash
npx framevideo render --output renders/output.mp4
```

完成后用 `ffprobe` 确认：

- 输出分辨率。
- 时长。
- 有视频轨道和音频轨道。

<!-- ## 用户显式要求预览时

只有用户显式要求预览时，才启动或复用 preview：

```bash
npx framevideo preview
``` -->


## 失败排查

- `auth status` 未登录：引导 `npx framevideo auth login`。
- 合成 `status=40` 且 `msg` 为空：优先检查 `source` 和 `figure_type` 是否真实存在，尤其确认没有默认使用不存在的 `whole_body`。
- 数字人变形：先检查蝉镜合成任务比例是否与所选形态 `width` / `height` 一致；竖版形态必须先生成 9:16 源视频，再检查是否把竖版素材强行放入 `16:9` 容器。
- 背景音乐不响：确认 audio clip 路径存在，`data-duration` 覆盖全片，`data-volume` 不为 0。
- 渲染失败：先跑 `lint -> validate -> inspect`，再检查素材路径和 Chrome/FFmpeg。

## 最终回复

最终回复用户时，给出：

- 成片 MP4 路径。
- 蝉镜数字人素材路径，如果有。
- contact sheet 路径。
- 已执行的校验命令结果摘要。
