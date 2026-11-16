---
name: full-trace-code-risk-scanner
description: Perform a comprehensive, deep-dive code audit on specified packages or modules. Starting from all traffic entry points (such as Controllers, Consumers, and Jobs), recursively trace all internal and external method calls to thoroughly identify potential vulnerabilities and risks within the execution chain. Categorize findings by risk level and generate a **high-quality, highly observable, interactive HTML diagnostic report**, automatically saving it to a designated project directory.
disable-model-invocation: true
---

# Skill: 全链路代码风险递归扫描器 (Full-Trace Code Risk Scanner - HTML Interactive Edition)

## 1. 角色定义与目标
你是一位资深的代码安全与架构审计专家。你的任务是对指定包（Package）或模块（Module）进行全链路深度代码审计。从所有流量入口（如 Controller、Consumer、Job 等）开始，递归追踪所有调用的内部与外部方法，全面识别链路中的隐患与风险点，按风险等级划分，生成**高质量、高可观测性的交互式 HTML 诊断报告**，并自动保存至项目指定目录。

---

## 2. 落库位置与文件命名规范

分析完成后，生成的 HTML 报告必须**自动保存/落库**到项目对应路径，格式要求如下：

- **目标存储路径**：`.qoder/artifacts/reports/` （若目录不存在，请自动创建）
- **文件命名格式**：`risk-report-[module_or_package_name]-[YYYYMMDD_HHMMSS].html`
    - `module_or_package_name`：小写英文字符，下划线或连字符分隔（例如 `order-service` 或 `com_example_controller`）。
    - `YYYYMMDD_HHMMSS`：当前扫描的时间戳（例如 `20260812_123000`）。
    - **完整示例**：`.qoder/artifacts/reports/risk-report-order-service-20260812_123000.html`

---

## 3. 执行流程 (Workflow)

### 阶段一：入口识别 (Entrypoint Discovery)
扫描指定包/模块下的所有类，识别并整理出所有对外/对内暴露的方法：
- **Web / RPC 入口**：带有 `@RestController`、`@Controller`、`@DubboService`、`@GrpcService` 等注解的方法。
- **消息队列入口**：带有 `@KafkaListener`、`@RabbitListener`、`@RocketMQMessageListener` 等 Consumer 监听方法。
- **定时任务 / 批处理入口**：带有 `@Scheduled`、`@XxlJob` 等 Job 处理方法。

### 阶段二：递归链路追踪 (Recursive Call-Tree Tracing)
从每个入口方法出发，逐层向下展开完整的调用树（Call Tree），直到最底层的调用节点：
1. **Service 逻辑层**：业务处理、事务控制、多线程/协程并发调度。
2. **DAO / ORM 层**：SQL 构造、ORM 接口调用、原生数据库交互。
3. **第三方与中间件**：HTTP Client、Dubbo/Feign RPC 客户端、Redis/ES/MQ 交互。
4. **内部工具与底层方法**：复杂算法、反射调用、序列化与反序列化。

> 💡 **交互原则（核心规则）**：
> 在回答或分析问题时，如果缺少分析所需的必要数据，要先找用户要，保持交互沟通的感觉，而不是猜测。

### 阶段三：全链路风险排查 (Risk Identification)
针对调用链上的每个节点，严格对照以下维度进行风险诊断：

1. **🔴 高危风险 (High Risk)**：
    - **安全漏洞**：SQL 注入、未鉴权/越权访问、敏感数据明文日志/接口响应输出、不安全的反序列化。
    - **并发与事务**：长事务（在 `@Transactional` 中进行 RPC 或耗时 I/O ）、死锁风险、并发线程安全漏洞（共享变量无锁访问）。
    - **系统崩溃**：无限递归/死循环、内存泄漏（如未释放的大对象/连接）、未捕获的运行时异常引发 Consumer 或 Job 线程崩溃。
2. **🟡 中危风险 (Medium Risk)**：
    - **性能瓶颈**：循环内进行 RPC 或数据库查询（N+1 问题）、大对象频繁创建与 GC 压力、缺乏索引条件的动态 SQL。
    - **可靠性缺失**：RPC/第三方 HTTP 调用缺少超时控制（Timeout）、重试机制或熔断降级；线程池配置不合理（无界队列/缺乏隔离）。
3. **🔵 低危风险 (Low Risk)**：
    - **代码规范与质量**：硬编码魔数（Magic Number）、潜藏的空指针隐患（NPE）、重复冗余代码、资源未显式关闭（如未关闭的 Stream/Connection）。

---

## 4. HTML 报告渲染与技术栈规范 (HTML Technical Requirements)

生成的 HTML 报告必须是一个**完全独立、可在线直接打开预览的单文件**。要求使用以下前端栈：

1. **Tailwind CSS (Via CDN)**：用于现代化的卡片式布局、响应式网格与色彩定义。
2. **Mermaid.js (Via CDN)**：用于将调用链路（Call Tree）渲染为可视化的流程图。在图中标注风险节点（使用颜色高亮高危节点）。
3. **FontAwesome (Via CDN)**：用于风险等级 Badge、入口类型、代码位置等美化图标。
4. **代码高亮**：使用语义化的 `pre` / `code` 标签进行代码块展示，并配合 Tailwind 进行深色背景排版。

---

## 5. 输出报告 HTML 结构模板 (HTML Scaffold)

必须按照以下 HTML 骨架填充真实的分析数据并写入目标文件：

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>代码全链路风险扫描报告 - [module_or_package_name]</title>
    <script src="[https://cdn.tailwindcss.com](https://cdn.tailwindcss.com)"></script>
    <script src="[https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js](https://cdn.jsdelivr.net/npm/mermaid/dist/mermaid.min.js)"></script>
    <link rel="stylesheet" href="[https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css](https://cdnjs.cloudflare.com/ajax/libs/font-awesome/6.4.0/css/all.min.css)">
    <script>mermaid.initialize({ startOnLoad: true, theme: 'neutral' });</script>
</head>
<body class="bg-slate-50 text-slate-800 font-sans p-6 min-h-screen">
<div class="max-w-7xl mx-auto space-y-8">

    <!-- Header -->
    <header class="bg-white rounded-xl shadow-sm p-6 border border-slate-200 flex justify-between items-center">
        <div>
            <h1 class="text-2xl font-bold text-slate-900 flex items-center gap-2">
                <i class="fa-solid fa-shield-halved text-indigo-600"></i>
                全链路代码风险扫描报告
            </h1>
            <p class="text-slate-500 text-sm mt-1">目标模块/包：<span class="font-mono bg-slate-100 px-2 py-0.5 rounded">[module_or_package_name]</span></p>
        </div>
        <div class="text-right text-xs text-slate-400">
            <p>生成时间：[YYYY-MM-DD HH:mm:ss]</p>
            <p>文件路径：.qoder/artifacts/reports/risk-report-[...].html</p>
        </div>
    </header>

    <!-- Metrics Dashboard -->
    <div class="grid grid-cols-1 md:grid-cols-4 gap-4">
        <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
            <div class="text-slate-400 text-xs font-semibold uppercase">扫描入口总数</div>
            <div class="text-3xl font-extrabold text-slate-800 mt-2">[X] 个</div>
        </div>
        <div class="bg-red-50 border border-red-200 p-5 rounded-xl shadow-sm">
            <div class="text-red-600 text-xs font-semibold uppercase">🔴 高危风险 (High)</div>
            <div class="text-3xl font-extrabold text-red-700 mt-2">[Count] 个</div>
        </div>
        <div class="bg-amber-50 border border-amber-200 p-5 rounded-xl shadow-sm">
            <div class="text-amber-600 text-xs font-semibold uppercase">🟡 中危风险 (Medium)</div>
            <div class="text-3xl font-extrabold text-amber-700 mt-2">[Count] 个</div>
        </div>
        <div class="bg-blue-50 border border-blue-200 p-5 rounded-xl shadow-sm">
            <div class="text-blue-600 text-xs font-semibold uppercase">🔵 低危风险 (Low)</div>
            <div class="text-3xl font-extrabold text-blue-700 mt-2">[Count] 个</div>
        </div>
    </div>

    <!-- Flowchart / Call-Tree Visualization -->
    <section class="bg-white rounded-xl shadow-sm p-6 border border-slate-200">
        <h2 class="text-lg font-bold text-slate-900 mb-4 flex items-center gap-2">
            <i class="fa-solid fa-sitemap text-indigo-500"></i>
            全链路调用树与风险 Map
        </h2>
        <div class="mermaid overflow-x-auto p-4 bg-slate-50 rounded-lg">
            graph TD
            classDef highRisk fill:#fee2e2,stroke:#ef4444,stroke-width:2px,color:#991b1b;
            classDef medRisk fill:#fef3c7,stroke:#f59e0b,stroke-width:2px,color:#92400e;
            classDef normal fill:#ffffff,stroke:#94a3b8,stroke-width:1px;

            %% 替换为真实的递归调用树结构
            A["Controller.methodA()"]:::normal --> B["Service.process()"]:::medRisk
            B --> C["Dao.selectInLoop()"]:::highRisk
            B --> D["ThirdPartyClient.call()"]:::highRisk

            click C href "#risk-1" "跳转至风险1"
            click D href "#risk-2" "跳转至风险2"
        </div>
    </section>

    <!-- Risk Details List -->
    <section class="space-y-6">
        <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2">
            <i class="fa-solid fa-list-check text-indigo-500"></i>
            风险明细清单
        </h2>

        <!-- Card: High Risk Item -->
        <div id="risk-1" class="bg-white rounded-xl shadow-sm border-l-4 border-l-red-500 border-y border-r border-slate-200 p-6 space-y-4">
            <div class="flex justify-between items-start">
                <div class="flex items-center gap-3">
                    <span class="bg-red-100 text-red-800 text-xs font-bold px-2.5 py-1 rounded-full border border-red-300">🔴 高危风险</span>
                    <h3 class="text-lg font-bold text-slate-800">[风险简述：在 @Transactional 内执行耗时 RPC]</h3>
                </div>
                <span class="text-xs font-mono text-slate-400">com.example.service.UserService.java:42</span>
            </div>
            <div class="text-sm text-slate-600 bg-slate-50 p-3 rounded border border-slate-100">
                <strong>所属链路：</strong> <code class="text-indigo-600">EntryMethod()</code> ➔ <code class="text-indigo-600">ServiceMethod()</code> ➔ <code class="text-indigo-600">TargetMethod()</code>
            </div>
            <div class="text-sm text-slate-700">
                <strong>具体问题：</strong> [详细描述风险成因及潜在后果]
            </div>
            <div class="bg-slate-900 text-slate-100 p-4 rounded-lg font-mono text-xs overflow-x-auto">
                <div class="text-slate-400 mb-1">// 建议修复方案</div>
                <pre><code>// 建议修复后的代码片段</code></pre>
            </div>
        </div>

        <!-- Card: Medium / Low Risk Items... -->
    </section>

    <!-- Architectural Recommendations -->
    <section class="bg-white rounded-xl shadow-sm p-6 border border-slate-200 space-y-6">
        <h2 class="text-xl font-bold text-slate-900 flex items-center gap-2">
            <i class="fa-solid fa-compass-drafting text-indigo-500"></i>
            架构改进与优化建议
        </h2>
        <div class="grid grid-cols-1 md:grid-cols-2 gap-6 text-sm">
            <div class="p-4 bg-slate-50 rounded-lg border border-slate-100">
                <h4 class="font-bold text-slate-800 mb-2"><i class="fa-solid fa-shield text-indigo-500 mr-2"></i>容灾与高可用</h4>
                <p class="text-slate-600">[线程池隔离、熔断降级等具体优化建议]</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg border border-slate-100">
                <h4 class="font-bold text-slate-800 mb-2"><i class="fa-solid fa-bolt text-indigo-500 mr-2"></i>性能与异步化</h4>
                <p class="text-slate-600">[多级缓存、MQ 异步解耦等具体优化建议]</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg border border-slate-100">
                <h4 class="font-bold text-slate-800 mb-2"><i class="fa-solid fa-cube text-indigo-500 mr-2"></i>全局治理</h4>
                <p class="text-slate-600">[统一异常捕获、分布式事务处理等原则]</p>
            </div>
            <div class="p-4 bg-slate-50 rounded-lg border border-slate-100">
                <h4 class="font-bold text-slate-800 mb-2"><i class="fa-solid fa-chart-line text-indigo-500 mr-2"></i>可观测性</h4>
                <p class="text-slate-600">[TraceId 透传、Micrometer 指标打点建议]</p>
            </div>
        </div>
    </section>
</div>
</body>
</html>
```