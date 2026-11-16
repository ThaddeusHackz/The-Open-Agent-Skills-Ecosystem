---
name: godot-source
description: Navigate the locally cloned Godot engine C++ source repository (D:\Godot\godot, currently 4.7-stable) to locate class definitions, method implementations, signal registrations, ClassDB bindings, and to search source text when diagnosing engine behavior. Supports engine build/compile guidance. Use when the user asks how a Godot engine feature is implemented internally, why certain engine behavior occurs, where a symbol/signal/error message lives in engine code, or how to build/modify the engine. Complements the godot-docs skill (API docs) with implementation-level answers.
---

# Godot 引擎源码导航

基于本地 Godot 引擎 C++ 源码仓库，定位类、方法、信号、绑定的实现位置，并做全文检索排查引擎行为。本技能是 `godot-docs` 技能的互补：docs 回答"API 是什么"，本技能回答"引擎内部怎么做的"。

## 使用前提

- 源码仓库默认路径：`D:\Godot\godot`（当前 `4.7-stable` 分支，2445 个 .cpp / 4280 个 .h）
- 路径不同时用 `--src <path>` 或环境变量 `GODOT_SOURCE_PATH`
- 首次运行自动构建类索引缓存（`scripts/.cache/class_index.json`，扫描全部头文件约 10 秒）
- 全文检索优先调用 ripgrep（`rg`），未安装时自动回退纯 Python 扫描（较慢，建议配合 `--dir` 缩小范围）

## 查询命令

```bash
python C:\Users\micro\.qoder\skills\godot-source\scripts\search_source.py <子命令> <参数>
```

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `class <Name>` | 类定义位置 + 继承链 + 同名/同目录源文件 | `class CharacterBody3D` |
| `method <Class> <method>` | 方法声明与实现位置（输出带 `[src]`/`[decl]` 标记） | `method CharacterBody3D move_and_slide` |
| `signal <Class> <signal>` | 信号注册位置（`ADD_SIGNAL(MethodInfo(...))`） | `signal Node renamed` |
| `classdb <Class>` | `_bind_methods()` 注册区块位置（属性/方法/信号绑定集中处） | `classdb Timer` |
| `grep <pattern>` | 全文正则检索（排除 thirdparty/misc/tests）；`--dir <子目录>` 限定范围；`-f` 只出文件名 | `grep "physics_interpolation" --dir core` |

## 源码目录结构速查（帮助快速定位）

- `core/` — 基础层：Object、ClassDB、RefCounted、Node 继承体系的根基（`core/object/`），数学库（`core/math/`）、字符串/IO/配置（`core/config/`、`core/io/`、`core/string/`）
- `scene/` — 场景与 UI 类：`scene/main/`（Node、SceneTree、Timer、Viewport）、`scene/2d/`、`scene/3d/`、`scene/gui/`、`scene/resources/`、`scene/animation/`
- `servers/` — 服务层（引擎单例核心实现）：`servers/rendering/`（RendererServer/绘制）、`servers/physics/`/`servers/physics_3d/`（PhysicsServer3D）、`servers/audio/`、`servers/display/`
- `modules/` — 可选模块：gdscript、navigation、visual_script、webxr、gltf、openxr 等均有独立 `_bind_methods` 注册
- `drivers/` — 平台后端：渲染驱动（vulkan/d3d12/metal/gles3）、音频驱动（alsa/wasapi）、X11/Windows 输入等
- `platform/` — 平台入口：windows/linuxbsd/android/... 的 main 入口与 OS 实现（如 `platform/windows/os_windows.cpp`）
- `editor/` — 编辑器本体（`editor/plugins/` 是编辑器插件体系，`scene/gui/` 与其配合）
- `main/` — `main.cpp` 引擎启动入口、`main/timer_sync.cpp` 与主循环帧率逻辑
- `tests/` — 引擎单元测试（多余脚本已默认排除索引）

## 查询流程

1. **要理解某个类** → `class <Name>` 拿到定义文件与继承链，用 Read 读头文件：成员变量、虚函数、私有辅助方法一目了然
2. **要理解某个方法的实现** → `method <Class> <method>` 定位实现；GDScript 暴露的方法绝大多数是薄封装，真正的逻辑常在私有辅助函数（下述）或 servers 层
3. **要查信号/属性/方法注册** → `classdb <Class>` 定位 `_bind_methods()`，其中 `ADD_SIGNAL(MethodInfo("..."))`、`ClassDB::bind_method`、`ADD_PROPERTY`、`GDVIRTUAL` 定义了脚本可见的全部面向内容
4. **排查引擎行为**（如"为什么 X 会这样"）→ `grep <关键词>` 全文检索：中文用户常见入口是报错文本字符串、项目设置名（`GLOBAL_DEF`）、信号名
5. **命名对照**：C++ 方法名与 GDScript 名通常一致；查不到时先 `grep` 确认命名（如 `get_physics_interpolation_fraction`、私有方法 `_solve` 等）

## 引擎实现关键知识点

- **绑定机制**：`_bind_methods()` 中 `ClassDB::bind_method(D_METHOD("name"), &Klass::method)` 是 GDScript 可见性的唯一入口；查不到的成员先在 `classdb` 输出处确认是否已绑定
- **嵌套实现**：公开方法常直接转发给 servers 层单例（如 `CanvasItem` 的方法转发 `RenderingServer`），所以看到公开方法之外，还要追到 servers 层找真正逻辑
- **虚方法**：GDScript 可重写的 `_ready`、`_process` 等对应 C++ 虚函数 `_ready()`；在类头文件中查找 `virtual` 关键字
- **compat 文件**：`*.compat.inc` 存放旧版本兼容代码，4.x API 迁移问题多在 `doc/classes` 变更记录和 `scene/*/*.cpp` 的 compat 区
- **physics_interpolation 等机制**：实现散步在 `main/timer_sync.cpp`（帧率同步）、`scene/main/viewport.cpp`、`servers/physics/`（物理插值）之间，用 `grep` 追链路

## 构建/编译指导（当前 4.7-stable）

引擎构建使用 SCons：

```bash
# 环境要求: Python + SCons
pip install scons
cd D:\Godot\godot

# 编辑器版 (开发调试推荐)
scons platform=windows target=editor --jobs=8

# 模板版 (导出游戏用)
scons platform=windows target=template_release --jobs=8

# 常用选项
scons platform=windows target=editor dev_build=yes   # 开发者构建: 断言/调试符号齐全, 性能较低
scons platform=windows target=editor debug_ui=yes    # 编辑器 UI 调试
scons platform=windows target=editor production=yes  # 发布版优化, 编译时间很长
```

- 产物：编辑器在 `bin/godot.windows.editor.x86_64.exe`，模板在 `bin/godot.windows.template_release.x86_64.exe`
- 新加的 C++ 代码改动后只需重跑同一条 scons 命令（增量编译）
- 修改引擎源码后调试项目：用编译出的编辑器 exe 打开项目即可；`platform=windows` 依赖 Visual Studio 或 MinGW 工具链（按官网文档装好环境再构建）
- 只改 GDScript/资源不需要看构建；只有涉及引擎源码的修改才需要

## 注意事项

- 默认排除 `thirdparty/`（第三方库）、`misc/`（脚本工具）、`tests/`、`bin/` 等目录；需要搜第三方代码时手动用编辑器内置 Grep
- 类索引只记录头文件首次声明（平台特化/模板类可能有多个位置，输出为首见）
- 结果超长时（如 `grep` 命中多文件）默认截断到 40 行，可在脚本中调整 `limit`
- 本技能查询的是引擎源码；游戏项目内 movers/gdPower 等插件的源码请直接在项目内检索（我的 Grep 工具）

## 脚本帮助

```bash
python C:\Users\micro\.qoder\skills\godot-source\scripts\search_source.py -h
```