---
name: qoder-skin
description: 给 Qoder IDE 换肤。用户提供一张背景图片，自动通过 CDP 本地注入将图片设为 Qoder 全窗口背景，不改安装包，可一键恢复。触发词：/qoder-skin、换肤、换背景、皮肤。
---

# Qoder Skin — Qoder IDE 换肤工具

## 触发条件

当用户说以下任意一种时触发：
- `/qoder-skin`
- "帮我换个皮肤"、"换个背景"、"换肤"
- "给 Qoder 换张背景图"
- 用户提供了一张图片并要求设为背景/皮肤

## 前置条件

- macOS 系统
- Qoder.app 正在运行（`/Applications/Qoder.app`）
- Node.js 可用（`node` 或 `/opt/homebrew/bin/node`）

## 执行步骤

### Step 1: 确认图片

用户必须提供一张图片文件路径。如果用户没有提供，主动询问：

> 请提供一张你想用作背景的图片路径（支持 PNG / JPEG / WebP，建议 16:9 比例，推荐 2560x1440）。

验证图片存在且大小合理（1 ~ 16 MB）。

### Step 2: 执行换肤

运行：

```bash
bash ~/.qoder/skills/qoder-skin/scripts/start.sh --image "<用户图片的绝对路径>"
```

脚本会自动：
1. 通过 `lsof` 检测 Qoder Electron 主进程的 CDP 端口（Qoder 默认自带，无需重启）
2. 验证 CDP 端点可用
3. 通过 CDP 注入 CSS + 背景图到所有渲染窗口
4. 进入 watch 模式，页面重载时自动重新注入

**无需重启 Qoder。** 换肤即时生效。

### Step 3: 告知用户结果

换肤成功后告知用户：

> Qoder Skin 已生效！当前背景图：`<图片路径>`
>
> - 停止注入器（皮肤保留到下次重启）：`bash ~/.qoder/skills/qoder-skin/scripts/stop.sh`
> - 恢复原始外观：`bash ~/.qoder/skills/qoder-skin/scripts/restore.sh`
> - 换一张图：再给我一张图片就行

## 技术原理（供排查用）

CDP 本地回环注入，无需重启 Qoder：

1. Qoder（Electron 应用）默认启用 CDP 调试端口（随机分配）
2. 通过 `ps + grep` 定位 Electron 主进程 PID，再用 `lsof -i -P -n` 找到监听的 127.0.0.1 端口
3. 通过 WebSocket 连接 `ws://127.0.0.1:{port}/devtools/page/{id}`
4. 筛选 `vscode-file://` 且包含 `.monaco-workbench` 的页面目标
5. `Runtime.evaluate` 注入 CSS（透明化原生面板 + backdrop-filter 模糊）+ 背景 DOM 层
6. 将 `qoder-skin` class 添加到 `.monaco-workbench` 元素上，激活所有皮肤选择器
7. Canvas 分析图片亮度，自动调整面板透明度（暗图 → 轻透明，亮图 → 重透明）
8. MutationObserver + Page.frameNavigated 监听，保证页面重载后自动恢复

### 已知坑点

- **CSS 选择器**：`.qoder-skin.monaco-workbench`（同元素双 class，无空格）而非 `.qoder-skin .monaco-workbench`（父子关系，有空格），因为 class 加在同一个 DOM 元素上
- **pgrep 不可靠**：Qoder 主进程会修改自身进程名，`pgrep -f` 可能匹配不到，需用 `ps aux | grep` 替代
- **Electron 直接启动 Segfault**：macOS 上不能直接执行 `.app/Contents/MacOS/Electron` 二进制（会 Segmentation fault），必须通过 `open -a` 启动
- **`open -a --args` 不透传 CDP 参数**：macOS LaunchServices 不会把 `--remote-debugging-port` 等参数传给 Electron，但幸运的是 Qoder 默认就启用了 CDP
- **`already-active` 问题（已修复）**：旧版 inject.js 在检测到皮肤已激活时直接返回 `already-active` 跳过注入，导致换图不生效。现在改为先清理旧皮肤再重新注入，无需手动 restore

## 恢复 / 卸载

```bash
# 移除皮肤，恢复 Qoder 原生外观
bash ~/.qoder/skills/qoder-skin/scripts/restore.sh

# 卸载 skill
rm -rf ~/.qoder/skills/qoder-skin
```

## 核心视觉默认值

| UI 区域 | 默认值 |
|---|---|
| 编辑区（空状态） | `opacity 0.30`，`blur 3px` — 背景图清晰可见 |
| 编辑区（打开文件） | `opacity 0.88` — 代码可读性优先 |
| 侧边栏 | `opacity 0.42`，`blur 2px`，`saturate 140%` |
| 标题栏 | `opacity 0.35`，`blur 2px` |
| 状态栏 | `opacity 0.45`，`blur 2px` |
| 底部面板 | `opacity 0.42`，`blur 2px` |
| Widget（悬浮/搜索） | `opacity 0.90`，`blur 3px` |
| 暗图自动适配 | `brightness < 0.45` → 面板透明度降低（更透明） |
| 亮图自动适配 | `brightness >= 0.45` → 面板透明度提高（更遮挡） |

## 注意事项

- **无需重启** Qoder，换肤即时生效
- CDP 仅绑定 127.0.0.1，不暴露到网络
- 不修改 Qoder 官方安装包和代码签名
- 重启 Qoder 后皮肤会消失，需要重新运行脚本
- 图片数据仅在本地处理，不上传任何外部服务

## 文件结构

```
qoder-skin/
  SKILL.md              # 本文件
  scripts/
    start.sh            # 检测 CDP 端口 + 注入（v2，无需重启）
    stop.sh             # 停止注入器
    restore.sh          # 移除皮肤恢复原生
    inject.mjs          # Node.js CDP 注入器
  assets/
    qoder-skin.css      # Qoder DOM 适配 CSS
    inject.js           # 渲染进程注入脚本模板
  themes/
    default/
      theme.json        # 默认主题配置
```
