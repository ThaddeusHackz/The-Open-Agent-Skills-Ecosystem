---
name: smithery-ai-cli
description: Install the smithery-ai-cli skill for your AI agent. Published on smithery.ai.
source: https://www.skills.sh/site/smithery.ai/smithery-ai-cli
---

<code class="language-bash code-highlight"><span class="code-line"><span class="token comment"># 1. Install</span>
</span><span class="code-line"><span class="token function">npm</span> <span class="token function">install</span> <span class="token parameter variable">-g</span> @smithery/cli
</span><span class="code-line">
</span><span class="code-line"><span class="token comment"># 2. Authenticate (requires human to confirm in browser)</span>
</span><span class="code-line">smithery auth login
</span><span class="code-line">
</span><span class="code-line"><span class="token comment"># 3. Search for MCP servers</span>
</span><span class="code-line">smithery mcp search <span class="token string">"github"</span>
</span></code>