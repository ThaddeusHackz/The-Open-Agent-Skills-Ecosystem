---
name: godot-docs
description: Query the locally cloned Godot official documentation (RST source at D:\Godot\godot-docs) for precise API class references, method/property/signal signatures, official tutorials and best practices. Use when the user asks about Godot API usage, class members, engine behavior, official tutorials, or when code needs verification against official docs instead of web search. Trigger scenarios: GDScript API questions, Godot class/method lookups, tutorial-style guidance like physics, shaders, networking.
---

# Godot 本地文档查询

基于本地克隆的 Godot 官方文档仓库（RST 源码），提供比网络搜索更精准、更新及时的 API 参考查询。

## 使用前提

- 文档仓库默认路径：`D:\Godot\godot-docs`
- 若路径不同，用 `--docs <path>` 参数或设置环境变量 `GODOT_DOCS_PATH` 指定
- 需要 Python 3 运行脚本

## 快速开始

所有查询通过脚本完成：

```bash
python C:\Users\micro\.qoder\skills\godot-docs\scripts\search_docs.py <子命令> <参数>
```

首次运行会自动建立类索引缓存（`scripts/.cache/class_index.json`，1079 个类约几秒）。

## 查询命令

| 子命令 | 用途 | 示例 |
|--------|------|------|
| `classes <query>` | 按名称搜索类，支持部分匹配、忽略大小写 | `classes characterbody` |
| `class <Name>` | 查看类的完整参考头部（继承链、属性、方法、信号一览） | `class CharacterBody3D` |
| `class <Name> --section <节>` | 只输出某个章节 | `class Node --section Signals` |
| `member <Class> <member>` | 精确查找类成员（方法/属性/信号/常量/注解）及完整描述 | `member Timer timeout` |
| `tutorial <query>` | 按标题搜索教程页面；`-k` 在标题无匹配时转全文搜索 | `tutorial physics_interpolation` |

## 查询流程与决策规则

1. **用户问题涉及某个类** → 先用 `classes <关键词>` 定位类名（输出含继承信息，可帮助判断类层次）
2. **需要某个方法/属性/信号的签名和语义** → 用 `member <Class> <member>` 获取签名 + 官方描述 + 成员类型
   - 注意：`member` 是精确匹配（忽略大小写），先在类中确认成员确实存在
3. **需要整体的 API 概况**（哪些方法可用、有哪些信号）→ 用 `class <Name>` 查看头部，或 `--section Methods/Properties/Signals` 查看对应章节
4. **需要"怎么做某事"的官方教程** → 用 `tutorial <主题>`；标题无结果时加 `-k` 全文搜索
5. **输出优先级**：把脚本输出中的关键信息翻译成准确的中文回答用户，RST 标记
   （`:ref:`、`\ (\ )`、`**`）可在转述时处理，但签名中的准确类型、默认值、参数顺序必须原样保留

## 输出中的 RST 标记速记

- `:ref:\`ClassX<class_ClassX>\`` — 指向其他类的引用，代表类型名
- `\ (\ )` — 空参数列表；`\ (\ up_direction\: ...\ )` 带参数
- `|void|` — 无返回值；`|const|` — const 方法
- `` ``默认值`` `` — 参数或属性的默认值

## 注意事项

- `classes/` 目录中的类文件是引擎自动生成的，永远是当前仓库版本对应的准确内容
- 教程目录（`tutorials/`、`getting_started/` 等）为人工编写，跟随最新主分支
- 属性/方法描述有时很长，`member` 命令只输出到下一个成员为止的完整描述，无需截断
- 若查询的成员在类中找不到，优先怀疑：继承自父类（用 `classes <父类>` + `member` 或直接查父类）或 `@GlobalScope`/`@GDScript` 等特殊类
- 枚举成员在类的 `--section Enumerations` 中；注解（如 `@export`）在 `class @GDScript` 中
- 脚本输出为 UTF-8；在旧版 Windows 终端若中文乱码，先执行 `chcp 65001`

## 脚本帮助

```bash
python C:\Users\micro\.qoder\skills\godot-docs\scripts\search_docs.py -h
```