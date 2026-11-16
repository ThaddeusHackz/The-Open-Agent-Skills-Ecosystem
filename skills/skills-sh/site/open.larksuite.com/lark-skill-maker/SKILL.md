---
name: lark-skill-maker
description: Install the lark-skill-maker skill for your AI agent. Published on open.larksuite.com.
source: https://www.skills.sh/site/open.larksuite.com/lark-skill-maker
---

<code class="language-bash code-highlight"><span class="code-line">lark-cli <span class="token operator"><</span>service<span class="token operator">></span> <span class="token operator"><</span>resource<span class="token operator">></span> <span class="token operator"><</span>method<span class="token operator">></span>          <span class="token comment"># 已注册 API</span>
</span><span class="code-line">lark-cli <span class="token operator"><</span>service<span class="token operator">></span> +<span class="token operator"><</span>verb<span class="token operator">></span>                      <span class="token comment"># Shortcut（高级封装）</span>
</span><span class="code-line">lark-cli api <span class="token operator"><</span>METHOD<span class="token operator">></span> <span class="token operator"><</span>path<span class="token operator">></span> <span class="token punctuation">[</span>--data/--params<span class="token punctuation">]</span>  <span class="token comment"># 任意飞书 OpenAPI</span>
</span><span class="code-line">lark-cli schema <span class="token operator"><</span>service.resource.method<span class="token operator">></span>       <span class="token comment"># 查参数定义</span>
</span></code>