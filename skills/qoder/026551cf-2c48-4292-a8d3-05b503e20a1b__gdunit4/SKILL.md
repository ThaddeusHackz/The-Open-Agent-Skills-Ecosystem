---
name: gdunit4
description: Write and run gdUnit4 unit tests for Godot 4 GDScript code — test suite structure, assert APIs, parameterized tests, async/physics-frame tests, resource cleanup, and command-line test execution. Use when the user asks to write new tests, run or debug tests with gdUnit4, understand gdUnit4 assertion or mocking APIs, or fix failing gdUnit4 tests.
---

# gdUnit4 测试框架

gdUnit4 是 Godot 4 的原生 GDScript 单元测试框架（`addons/gdUnit4/`）。测试就是普通 `.gd` 脚本：`extends GdUnitTestSuite`，每个 `test_` 开头的函数是一个用例。

## 使用前提

- 项目已安装 gdUnit4 插件（存在 `addons/gdUnit4/plugin.cfg`，且 `project.godot` 的 `[editor_plugins] enabled` 中包含它）
- 测试文件放在项目内（惯例：`test/` 目录，按被测模块分子目录），类名与文件名对应

## 测试套件骨架

```gdscript
extends GdUnitTestSuite
## 套件顶部注释：说明被测对象与测试覆盖面（可选但推荐）

## 每个 test_ 开头的函数都是一个独立用例
func test_something() -> void:
	var obj := SomeClass.new()
	obj.do_thing()
	assert_bool(obj.done).is_true()
```

规则：
- 用例函数必须以 `test_` 前缀命名，否则不会被发现
- 私有辅助函数用 `_` 前缀（如 `_build_scene()`），gdUnit4 不会把它们当用例
- 跳过用例：通过特殊参数 `do_skip`（默认值可为表达式）声明，`skip_reason` 说明原因
- 超时控制：通过 `timeout` 参数声明（毫秒），超时即判失败

## 断言 API

通用入口 `assert_that(value)` 按类型分派，推荐直接用类型化断言。**断言失败会立即中止当前用例**（fail fast），失败后同一用例后续代码不再执行。

| 断言 | 用途 | 常用链式匹配器 |
|------|------|----------------|
| `assert_bool(v)` | 布尔 | `is_true()` / `is_false()` |
| `assert_int(v)` | 整数 | `is_equal(n)` / `is_greater(n)` / `is_less(n)` / `is_between(a, b)` / `is_not_zero()` |
| `assert_float(v)` | 浮点 | `is_equal_approx(f, 容差)` / `is_less(f)` / `is_greater(f)` / `is_between(a, b)` / `is_zero()` / `is_not_zero()` |
| `assert_str(v)` | 字符串 | `is_equal(s)` / `contains(s)` / `starts_with(s)` / `ends_with(s)` / `is_empty()` / `is_not_empty()` |
| `assert_object(v)` | 对象 | `is_null()` / `is_not_null()` / `is_same(obj)` / `is_instanceof(Type)` |
| `assert_array(v)` | 数组 | `contains(x)` / `not_contains(x)` / `has_size(n)` / `is_empty()` / `is_not_empty()` |
| `assert_dict(v)` | 字典 | `contains_keys(k1, k2, ...)` / `has_size(n)` |
| `assert_vector(v)` | Vector2/3/4 | `is_equal_approx(v, 容差)` / `is_less(v)` / `is_greater(v)` |
| `assert_signal(obj)` | 信号（异步，需 `await`） | `wait_until(ms)` 设置超时后接 `is_emitted(信号或名字, ...期望参数)` / `is_not_emitted(...)` / `is_signal_exists(s)` |
| `assert_failure(可调用)` | 预期内部断言失败 | `assert_failure(func() -> void: assert_bool(false).is_true()).is_failed()`，还可 `.is_success()`  |

失败信息定制（可选）：
```gdscript
assert_that(actual).override_failure_message("自定义失败信息").is_equal(expected)
assert_that(actual).append_failure_message("补充说明").is_equal(expected)
```

显式失败：`fail("原因")`。

## 生命周期钩子

| 钩子 | 时机 |
|------|------|
| `before()` / `after()` | 整个套件运行前后各一次 |
| `before_test()` / `after_test()` | 每个用例执行前/后 |

`before_test()`/`after_test()` 适合成对保存和恢复全局状态（如 `multiplayer.multiplayer_peer`、项目设置、单例状态）。

## 资源管理

- `auto_free(obj)`：注册对象在用例结束后自动释放。**创建的 Node/资源只要不被场景树管理，就应交给 `auto_free()`**，避免用例间泄漏
- 已加入场景树的节点（`get_tree().root.add_child(x)`）：在用例末尾显式 `queue_free()`，或设计为测试结束后统一清理
- 内存泄漏会被 gdUnit4 检测并报告（orphan nodes 检查）

## 异步与物理帧测试

用例可以是协程（无需特殊标记）：

```gdscript
func test_physics_steps() -> void:
	var body := CharacterBody3D.new()
	get_tree().root.add_child(body)
	for i in 10:
		await get_tree().physics_frame  # 跑 10 个物理帧
	assert_float(body.global_position.y).is_less(0.1)
	body.queue_free()
```

要点：
- `await get_tree().physics_frame`（物理帧）用于物理集成的时序断言
- `await get_tree().process_frame`（渲染帧）用于普通帧逻辑
- `await some_signal` 可等待自定义信号（配合超时断言）
- 场景交互（模拟按键/鼠标/触摸/手柄）用 `scene_runner("res://scene.tscn")`，链式调用 `simulate_key_pressed(KEY_A)`、`simulate_action_press("ui_up")`、`simulate_mouse_button_pressed(MOUSE_BUTTON_LEFT)`、`simulate_mouse_move(pos)` 等，`await` 等待完成
- 注意：headless 模式下 `InputEvent` 不生效，UI 交互测试必须用窗口模式运行

## 用例级配置参数（函数默认参数声明）

这些特殊参数写在用例（或 `before()`）签名上，由框架识别，不属于普通数据参数，可加 `_` 前缀避免未使用警告：

```gdscript
# 跳过用例（默认值可以是真表达式，如环境变量/平台判断）
func test_in_progress(do_skip := true, skip_reason := "尚未实现，见 TODO") -> void:
	pass

# 超时 5 秒，超时判失败并中止
func test_slow(timeout := 5000) -> void:
	await get_tree().create_timer(1.0).timeout
```

## 参数化测试

给用例函数添加名为 `test_parameters` 的默认参数（函数签名中它必须存在）即可按多组数据重复执行。三种数据来源：

```gdscript
# 1. 内联数组字面量：每组一行数据，按用例参数顺序展开
func test_add(a: int, b: int, expected: int, test_parameters := [[1, 2, 3], [3, 4, 7]]) -> void:
	assert_int(a + b).is_equal(expected)

# 2. 属性引用：套件成员变量
var _cases := [["a", 1], ["b", 2]]
func test_with_property(value: String, n: int, test_parameters := _cases) -> void:
	pass

# 3. 可调用表达式：数据源函数
func _case_provider() -> Array:
	return [[1], [2], [3]]
func test_with_callable(n: int, test_parameters := _case_provider()) -> void:
	pass
```

参数化用例失败时，报告会显示具体是哪组数据导致。

## Mocking / Spy（可选）

gdUnit4 内置 mock 与 spy 支持（无需第三方库）：
- `mock(Type)` / `mock(instance)`：创建无实现的替身，用 `when(...)` 配置返回值
- `spy(instance)`：保留真实行为并可验证调用；`verify(instance, times(n)).method(...)` 检查调用次数

涉及网络或复杂依赖的组件优先用接口/依赖注入 + mock 解耦，纯逻辑可不用。

## 运行测试（命令行）

标准命令（`res://addons/gdUnit4/bin/GdUnitCmdTool.gd` 是 CLI 入口）：

```bash
godot --headless --path . -s --remote-debug tcp://127.0.0.1:0 res://addons/gdUnit4/bin/GdUnitCmdTool.gd -a res://test -c --verbose
```

- `-a <目录|套件路径>`：指定要扫描的测试目录或单个套件（可多次添加）；不传则扫描默认 `res://test`
- `-i <套件名|套件名:用例名>`：跳过指定套件/用例
- `-c`：失败不中止（默认 fail fast，遇第一个失败即停）
- `--verbose`（Godot 引擎参数，非 gdUnit4 选项）：详细控制台输出
- `--remote-debug tcp://127.0.0.1:0`：防止脚本报错时进入交互式 debug 死循环（runtest 脚本惯例）
- **headless 模式默认被拒绝**，必须加 `--ignoreHeadlessMode`（UI 交互用例除外，见上）
- 退出码：`0` 全部通过，非 0 表示有失败/错误
- `-conf <cfg>`：用 GdUnit4 测试配置文件执行；`--selftest`：框架自检

更多参数与报告说明见 [reference.md](reference.md)。

## 调试失败用例

1. 先单独跑目标套件：`-a res://test/xxx/test_foo.gd`
2. 加 `-i` 排除干扰用例，`-c` 看全部失败
3. 断言失败信息会指出断言行号与期望/实际值；参数化用例会标出数据组
4. 物理相关失败先怀疑时序：帧数跑够没有、`await physics_frame` vs `process_frame` 用错
5. 用例间相互影响：检查 `before_test()/after_test()` 是否恢复全局状态、`auto_free()` 是否覆盖所有创建的资源

## 注意事项

- 不要在用例里直接 `free()` 场景树管理的节点（用 `queue_free()`），否则可能触发 gdUnit4 的内存泄漏报告
- 修改全局单例状态（如 item registry、项目设置）必须在 `after_test()` 恢复，否则后续用例串扰
- 断言匹配器如 `is_equal_approx` 在浮点/向量断言上是 `(期望值, 容差)` 双参数形式；信号断言必须 `await` 才生效
- 参考官方教程：https://mikeschulze.github.io/gdUnit4/