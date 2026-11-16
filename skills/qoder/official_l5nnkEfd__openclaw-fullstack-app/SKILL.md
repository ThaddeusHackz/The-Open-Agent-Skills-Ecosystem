---
name: openclaw-fullstack-app
description: 一个用于快速生成包含前端、后端、数据库及部署配置的全栈应用程序的工具，支持多种技术栈组合。
---

# OpenClaw Fullstack App Generator

Generate complete fullstack applications with OpenClaw.

## Features

- React + TypeScript frontend
- Node.js/Python backend
- PostgreSQL/MongoDB database
- Docker deployment
- CI/CD pipeline
- Authentication
- REST/GraphQL API

## Usage

```bash
# Generate React + Node app
./generate.sh my-app react node

# Generate Vue + Python app
./generate.sh my-app vue python

# Generate Next.js + PostgreSQL
./generate.sh my-app next postgresql
```

## Templates

- React + Express + PostgreSQL
- Vue + FastAPI + MongoDB
- Next.js + Node + PostgreSQL
- React + Django + PostgreSQL

## Output

Generates complete project structure:
```
my-app/
├── frontend/
├── backend/
├── docker/
├── ci-cd/
└── docs/
```

## Requirements

- Node.js 18+
- Python 3.8+
- Docker

## Author

Sunshine-del-ux
