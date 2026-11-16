---
name: onshape-featurescript
description">Generate Onshape FeatureScript code for custom CAD features and parametric parts. Specializes in dust collection fittings library (wyes, elbows, adapters, crosses). Use when user asks to: (1) create FS features (gears, fittings, brushes), (2) modify existing FS, (3) debug FS errors, (4) build libraries with consistent patterns (enums, shells, labels). Patterns for Z-axis fittings, wrapped labels, safe unions/shells. Triggers: 'Onshape FS for X', 'FeatureScript wye/elbow', 'dust fitting'.</description>
description: 为自定义 CAD 功能和参数化零件生成 Onshape FeatureScript 代码。专注于除尘配件库（三通、弯头、适配器、十字接头）。适用于用户请求：(1) 创建 FS 功能（齿轮、配件、刷子），(2) 修改现有 FS，(3) 调试 FS 错误，(4) 构建具有一致模式（枚举、抽壳、标签）的库。包含 Z 轴配件、包裹标签、安全联合/抽壳的模式。触发词：'Onshape FS for X'、'FeatureScript wye/elbow'、'dust fitting'。
---

# Onshape FeatureScript Generator

## Quick Start

Analyze request → Match pattern → Gen FS code → Validate logic.

**Core Workflow**:
1. **Precondition**: Enums/lengths/reals w/ bounds.
2. **Body**: Sketches → Extrudes → Booleans → Shell → Wrap/Thicken labels.
3. **Pitfalls**: qOwnedByBody(finalBody), if/else (no ternary lengths), cylinder(coordSystem).

## Key Patterns (Memorize)
- **Enum + Cond Param**:
  ```
  export enum AlignmentStyle { Centered, Tangent, Offset };
  if (definition.alignment == AlignmentStyle.Offset) { isLength(def.offsetDistance...); }
  ```
- **Safe Shell Caps**:
  ```
  var capFaces = qFacesParallelToDirection(qOwnedByBody(finalBody, EntityType.FACE), vector(0,1,0));
  ```
- **Union Primary First**:
  ```
  qUnion([qCreatedBy(id+"inlet", EntityType.BODY), ...]);
  ```
- **Wrapped Label**: skText → opWrap → opThicken.

## Dust Fittings Lib
Z-axis: Inlet Z=0 (-Z), Outlet Z=trans (+Z), Branch +X.
See [FITTINGS.md](references/fittings.md) for full spec/pitfalls.

## Resources
- **API Patterns**: [PATTERNS.md](references/patterns.md)
- **Fonts**: AllertaStencil-Regular.ttf for labels.
- **Validate**: Test mentally; no runtime here.

Gen code → User pastes to Onshape FS editor.
