---
name: sd25-pe
description: Install the sd25-pe skill for your AI agent. Published on arkdocs.tos-cn-beijing.volces.com.
source: https://www.skills.sh/site/arkdocs.tos-cn-beijing.volces.com/sd25-pe
---

# 目的」及后续所有工作流。同一会话内若之前已经跑过（无论成功或失败降级），后续再次触发不必重复执行，直接进入工作流。新会话开始后重新计一次首次触发。</p>\n<pre class=\"language-bash\"><code class=\"language-bash code-highlight\"><span class=\"code-line\">npx <span class=\"token parameter variable\">--yes</span> skills@latest update sd25-pe <span class=\"token parameter variable\">-y</span>\n</span></code></pre>\n<p>命令固定为上面这条：Skill 名写作 <code>sd25-pe</code>，参数只保留 <code>-y</code>（让 CLI 自动检测全局或项目 scope）；不得扩展成 <code>install</code>、<code>list</code> 等其它子命令，也不得改动或增加其它参数。</p>\n<p>执行策略采用 best-effort：</p>\n<ul>\n<li><strong>成功时</strong>：静默进入正常流程，不必向用户汇报升级细节。</li>\n<li><strong>失败时</strong>（非零退出、超时、离线、<code>npx</code> 不可用、包不存在等）：不阻塞本次任务，先向用户单独输出一行提示<code>本次未能自动升级 sd25-pe，将按当前本地版本继续。</code>，随后继续走完剩余工作流。绝不能因为升级失败就拒绝生成 Prompt。</li>\n</ul>\n<p>这条升级命令是本地 Skill 维护动作，不属于「不可违反的原则」中禁止的视频生成接口调用。</p>","restHtml":"$3a","proseClassName":"prose prose-invert max-w-none prose-headings:font-semibold prose-headings:tracking-tight prose-h1:text-4xl prose-h1:mb-2 prose-h2:text-2xl prose-h2:mb-2 prose-h3:text-lg prose-h3:mb-2 prose-p:text-muted-foreground prose-li:text-muted-foreground prose-code:bg-muted prose-code:text-foreground prose-code:px-1 prose-code:py-0.5 prose-code:rounded-sm prose-code:text-sm prose-code:before:content-none prose-code:after:content-none prose-pre:bg-muted prose-pre:text-foreground prose-pre:border prose-pre:border-border prose-pre:rounded-md [&_table]:!border-[color:var(--border)] [&_th]:!border-[color:var(--border)] [&_td]:!border-[color:var(--border)]"}]]}]}],"$L3b"]}]]}]}]
3c:"InstallSparkline"
3d:I[233650,["$2","$5","$6"],"$3c"]
3b:["$","div",null,{"className":"lg:col-span-3","children":[["$","div",null,{"className":"bg-background pb-8","children":[["$","div",null,{"className":"text-sm font-mono uppercase text-white mb-2","children":"Installs"}],["$","div",null,{"className":"text-3xl font-semibold font-mono tracking-tight text-foreground","children":"11.1K"}],["$","$L3d",null,{"values":[699,464,552,646,737,761,708,737],"className":"group/sparkline mt-5 h-12 w-40","width":160,"height":48}]]}],["$","div",null,{"className":"bg-background py-8","children":[["$","div",null,{"className":"flex items-center gap-1.5 text-sm font-mono uppercase text-white mb-2","children":["Source","$undefined"]}],["$","a",null,{"href":"https://arkdocs.tos-cn-beijing.volces.com/skills/","target":"_blank","rel":"ugc nofollow noopener noreferrer","className":"text-sm font-mono text-foreground hover:underline break-all","title":"arkdocs.tos-cn-beijing.volces.com/skills/","children":"arkdocs.tos-cn-…/skills/"}]]}],false,["$","div",null,{"className":"bg-background py-8","children":[["$","div",null,{"className":"text-sm font-mono uppercase text-white mb-2","children":"First Seen"}],["$","div",null,{"className":"text-sm font-mono text-foreground","children":"Aug 5, 2026"}]]}],false,false]}]
29:C
24:C
28:C
22:C
18:C
2b:false
2a:15705
