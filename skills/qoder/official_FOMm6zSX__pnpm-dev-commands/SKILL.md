---
name: pnpm-dev-commands
description: Quick reference for pnpm development commands in File Manager API
tags: [pnpm, development, commands]
---

# pnpm Development Commands

## Build & Run

| Command | Description |
|---------|-------------|
| `pnpm install` | Install dependencies |
| `pnpm dev` | Dev server with hot-reload (port 3000) |
| `pnpm build` | Compile TypeScript to dist/ |
| `pnpm start:dev` | Run compiled app in dev env (port 3000) |
| `pnpm start:test` | Run compiled app in test env (port 3001) |
| `pnpm start:prod` | Run compiled app in prod env (port 3000) |

## Testing

| Command | Description |
|---------|-------------|
| `pnpm test` | Run all tests |
| `pnpm test:watch` | Run tests in watch mode |
| `pnpm test:coverage` | Run tests with coverage report |
| `pnpm test:integration` | Run integration tests only |
| `pnpm type-check` | TypeScript compiler check (no emit) |

## Utility Scripts

| Command | Description |
|---------|-------------|
| `pnpm test:azure` | Test Azure Blob Storage connectivity |
| `pnpm count:azure` | Count files in Azure Blob Storage |
| `pnpm test:db` | Test database connectivity |
| `pnpm explore:db` | Explore database schema |
| `pnpm list:users` | List users with their parent IDs |
| `pnpm list:parent-question` | List parent/question combinations with files |
| `pnpm check:files` | Check files by parent/question |
| `pnpm test:parent-access` | Test parent access authorization |

## Environment Variables

Set `APP_ENV` to switch environments: `dev`, `test`, `prod` (default: `dev`)
