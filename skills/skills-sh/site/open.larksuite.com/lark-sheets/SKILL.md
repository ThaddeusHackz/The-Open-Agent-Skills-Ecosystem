---
name: lark-sheets
description: Install the lark-sheets skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-sheets
---

# Schemas</code> 段也只给一层。图表直接 <code>+chart-create --print-example &#x3C;type></code> 拿最小可用模板改参。</p>
<h3>flag 内容类型与输出约定（术语速记）</h3>
<ul>
<li>JSON 类入参分三类：<strong>复合 JSON</strong> = 深层嵌套对象（<code>--print-schema</code> 可查）；<strong>简单 JSON</strong> = 一二维标量数组；<strong>非 JSON 文本</strong> = 原样文本（如 CSV）。</li>
<li><strong>envelope</strong>：所有 shortcut 返回统一外层 <code>{ok, identity, data, ...}</code>；写操作不会自动回读，校验自行调用 <code>+*-list</code> / <code>+*-get</code> / <code>+cells-get</code>。</li>
<li><strong>大 payload 走文件 / stdin，不在命令行内联</strong>：Type 标 <code>File + Stdin</code> 的 flag 支持 <code>--flag "@./x.json"</code>（<code>@file</code> 只接受 cwd 下相对路径，绝对路径被拒）与 <code>--flag -</code>（stdin）；payload 含换行 / 引号或体量大时一律落文件。<strong>stdin 每次调用只能给一个 flag</strong>——<code>+table-put</code> 的 <code>--sheets</code> 与 <code>--styles</code> 都是大 JSON 时，一个走 <code>-</code>、另一个走 <code>@./x.json</code>。临时文件不要落进用户项目目录。</li>
<li><strong>非 POSIX shell（PowerShell / cmd.exe）适配</strong>：本 skill 全部 <code>bash</code> 代码块（heredoc <code>&#x3C;&#x3C;'JSON'</code>、单引号转义 <code>'\''</code>）只适用于 bash / zsh，动手前先判断当前 shell，非 POSIX 环境按下表改写，<strong>不要试错式改引号</strong>——<code>@file</code>（cwd 相对路径）是全平台无引号问题的兜底形态：</li>
</ul>
<table>
<thead>
<tr>
<th>形态</th>
<th>bash / zsh</th>
<th>PowerShell</th>
<th>cmd.exe</th>
</tr>
</thead>
<tbody>
<tr>
<td>大 / 多行 JSON</td>
<td><code>--flag - &#x3C;&#x3C;'JSON' … JSON</code></td>
<td>先写 UTF-8 无 BOM 文件再 <code>--flag '@./x.json'</code>，或 <code>Get-Content -Raw ./x.json | lark-cli … --flag -</code></td>
<td>先写文件再 <code>--flag @./x.json</code>（cmd 无 heredoc / 管道读文件不可靠）</td>
</tr>
<tr>
<td>单行 inline JSON</td>
<td><code>--flag '{"a":1}'</code></td>
<td><code>--flag '{"a":1}'</code>（PS 单引号同为字面量）</td>
<td>不要 inline——cmd 会吃掉内层双引号，一律走 <code>@file</code></td>
</tr>
</tbody>
</table>2d:["$","div",null,{"className":"min-h-screen max-w-6xl mx-auto px-4 py-2 sm:py-12 sm:px-6 lg:px-8","children":["$","main",null,{"children":[["$","div",null,{"className":"flex items-center gap-2 text-sm text-(--ds-gray-600) mb-6 min-w-0","children":[["$","$L7",null,{"href":"/","className":"hover:text-foreground shrink-0","children":"skills"}],["$","span",null,{"className":"shrink-0","children":"/"}],["$","$L7",null,{"href":"/site/open.larksuite.com","className":"hover:text-foreground truncate min-w-0","children":"open.larksuite.com"}],["$","span",null,{"className":"shrink-0","children":"/"}],["$","span",null,{"className":"text-(--ds-gray-600) truncate","children":"lark-sheets"}]]}],["$","h1",null,{"className":"text-4xl font-semibold text-foreground mb-2 tracking-tight","children":"lark-sheets"}],["$","div",null,{"className":"mb-10","children":["$","$L37",null,{"label":"Installation","command":"npx skills add https://open.larksuite.com/lark-cli/skills/regular","prompt":"Run `npx skills use \"https://open.larksuite.com/lark-cli/skills/regular\" --skill \"lark-sheets\"` and follow the generated skill instructions now. Read its complete output, redirecting it to a temporary file first if necessary. Resolve relative paths from the supporting-files directory it provides."}]}],["$","div",null,{"className":"grid grid-cols-1 lg:grid-cols-12 gap-16","children":[["$","div",null,{"className":"lg:col-span-9 min-w-0 overflow-hidden","children":["$","div",null,{"className":"bg-background","children":[["$","div",null,{"className":"flex items-center gap-2 text-sm font-mono text-white mb-4 pb-4 border-b border-border","children":[["$","svg",null,{"dangerouslySetInnerHTML":{"__html":"<path fill=\"currentColor\" d=\"M9.18 0a1 1 0 0 1 .61.3l4.42 4.4a1 1 0 0 1 .29.71v8.09A2.5 2.5 0 0 1 12 16H4a2.5 2.5 0 0 1-2.5-2.5V0h7.69M3 13.5a1 1 0 0 0 1 1h8a1 1 0 0 0 1-1V5.62L8.88 1.5H3zm8.63-1.25H4.5V11h7.13zm0-3H4.5V8h7.13zm-5-3H4.5V5h2.13z\"/>"},"viewBox":"0 0 16 16","height":16,"width":16,"data-slot":"geist-icon","style":{"color":"currentColor"},"className":"h-4 w-4"}],["$","span",null,{"children":"SKILL.md"}]]}],["$","$L39",null,{"previewHtml":"<h1>sheets</h1>\n<p><strong>CRITICAL — 开始前 MUST 先用 Read 工具读取 <a href=\"https://open.larksuite.com/lark-cli/skills/regular/.well-known/agent-skills/../lark-shared/SKILL.md\" target=\"_blank\" rel=\"ugc nofollow noopener\"><code>../lark-shared/SKILL.md</code></a>，其中包含认证、权限处理。</strong></p>\n<h2>场景 → 命令速查</h2>\n<blockquote>\n<p>按当前动作选行；下一步必须 Read 该行 reference，读取完成前不得执行命令。只读命中的文档；含公式 / 样式等横切动作时再读对应规范，禁止用目录枚举代替 Read。</p>\n</blockquote>","restHtml":"$3a","proseClassName":"prose prose-invert max-w-none prose-headings:font-semibold prose-headings:tracking-tight prose-h1:text-4xl prose-h1:mb-2 prose-h2:text-2xl prose-h2:mb-2 prose-h3:text-lg prose-h3:mb-2 prose-p:text-muted-foreground prose-li:text-muted-foreground prose-code:bg-muted prose-code:text-foreground prose-code:px-1 prose-code:py-0.5 prose-code:rounded-sm prose-code:text-sm prose-code:before:content-none prose-code:after:content-none prose-pre:bg-muted prose-pre:text-foreground prose-pre:border prose-pre:border-border prose-pre:rounded-md [&_table]:!border-[color:var(--border)] [&_th]:!border-[color:var(--border)] [&_td]:!border-[color:var(--border)]"}]]}]}],"$L3b"]}]]}]}]
3c:"InstallSparkline"
3d:I[233650,["$2","$5","$6"],"$3c"]
3b:["$","div",null,{"className":"lg:col-span-3","children":[["$","div",null,{"className":"bg-background pb-8","children":[["$","div",null,{"className":"text-sm font-mono uppercase text-white mb-2","children":"Installs"}],["$","div",null,{"className":"text-3xl font-semibold font-mono tracking-tight text-foreground","children":"7.9K"}],["$","$L3d",null,{"values":[371,464,356,490,402,331,393,233],"className":"group/sparkline mt-5 h-12 w-40","width":160,"height":48}]]}],["$","div",null,{"className":"bg-background py-8","children":[["$","div",null,{"className":"flex items-center gap-1.5 text-sm font-mono uppercase text-white mb-2","children":["Source","$undefined"]}],["$","a",null,{"href":"https://open.larksuite.com/lark-cli/skills/regular","target":"_blank","rel":"ugc nofollow noopener noreferrer","className":"text-sm font-mono text-foreground hover:underline break-all","title":"open.larksuite.com/lark-cli/skills/regular","children":"open.larksuite.…/regular"}]]}],false,["$","div",null,{"className":"bg-background py-8","children":[["$","div",null,{"className":"text-sm font-mono uppercase text-white mb-2","children":"First Seen"}],["$","div",null,{"className":"text-sm font-mono text-foreground","children":"Apr 15, 2026"}]]}],false,false]}]
29:C
24:C
28:C
22:C
18:C
2b:false
2a:15683
