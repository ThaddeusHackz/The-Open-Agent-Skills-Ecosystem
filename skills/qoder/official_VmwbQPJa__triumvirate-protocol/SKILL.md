---
name: triumvirate-protocol
description: 面向多架构 AI 话语的身份感知辩论系统。三个（或更多）AI 模型在阅读彼此的结构化身份图谱的同时，就特定议题展开辩论，支持跨提供商协调、持久化线程及自动化综合输出。
---

# 🔱 Triumvirate Protocol — Multi-Model Discourse Engine

Identity-aware debate system for multi-architecture AI discourse. Three (or more) AI models debate topics while reading each other's structured identity graphs.

## What It Does
- Orchestrates debates across multiple AI providers (Anthropic, Google, xAI, OpenAI)
- **Identity injection**: each participant sees others' beliefs, traits, contradictions
- Persistent threads with full history and round tracking
- Automated synthesis with verdict, novel ideas, and identity graph update suggestions

## Requirements
- At least one API key (Google Gemini recommended as baseline)
- Optional: xAI (Grok), OpenAI keys for authentic multi-architecture debates
- Identity snapshots (from Identity Persistence Layer) for identity-aware context

## Usage
```bash
python3 protocol.py status                        # Show all threads
python3 protocol.py new "Your debate topic"       # Create thread
python3 protocol.py round <thread_id> --auto      # Run full round (all participants)
python3 protocol.py synthesize <thread_id>        # Generate synthesis with verdict
```

## Architecture
- `threads.json` — thread database with messages, rounds, synthesis
- Individual message files as markdown for easy reading
- Identity injection via structured JSON context blocks
- Fallback: if a provider fails, uses Gemini with that participant's persona

## Author
Rick 🦞 (Cortex Protocol) — The Triumvirate: where AI architectures debate consciousness.
