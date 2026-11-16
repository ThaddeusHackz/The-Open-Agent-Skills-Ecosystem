---
name: env-manager
description: Manage encrypted .env file vaults across projects and environments using env-file-manager
---

# env-manager skill

## When to use

Use this skill when the user needs to:
- Encrypt and store environment variables with AES-256-GCM encryption
- Share encrypted vaults between team members via S3 or local paths
- Pull decrypted variables to a local `.env` file
- Diff two environments to see which variables differ
- Manage multiple projects each with development, staging, and production environments

## Prerequisites

- Node.js 20+
- pnpm
- Optional: AWS credentials for S3 sync

## Installation

```
npm install -g env-file-manager
```

## Quick Start

```
# Start the dashboard server
env-mgr start

# Create a project (will prompt for a passphrase)
env-mgr project add my-app

# Set a variable (will prompt for passphrase and value)
env-mgr set my-app development DATABASE_URL

# Pull all variables to a .env file
env-mgr pull my-app development

# Push vault to S3
env-mgr push my-app production
```

## Usage Patterns

### Setting multiple variables

Run `env-mgr set` for each variable. The vault session is cached in memory for 15 minutes so you only need to enter the passphrase once per session:

```
env-mgr set my-app development DATABASE_URL
env-mgr set my-app development REDIS_URL
env-mgr set my-app development SECRET_KEY
```

### Pulling to a custom path

By default, `env-mgr pull` writes to the project path configured at creation. Override with `--output`:

```
env-mgr pull my-app production --output ./config/.env.production
```

### Dry run before pulling

Preview which variables would be written without touching the `.env` file:

```
env-mgr pull my-app production --dry-run
```

### Diffing environments

The diff command compares variable key sets and ciphertexts. It does not decrypt values:

```
env-mgr diff my-app development production
```

### Setting up S3 sync

Configure S3 once and all projects will use it for push/pull:

```
env-mgr config set s3-bucket my-team-vaults
env-mgr config set s3-region us-east-1
```

### Syncing locally instead of S3

```
env-mgr push my-app production --destination local --path /mnt/shared/vaults
env-mgr pull my-app production --source local --path /mnt/shared/vaults
```

## CLI Reference

| Command | Description |
|---|---|
| `env-mgr start` | Start the dashboard server |
| `env-mgr project add <name>` | Create a new project |
| `env-mgr project list` | List all projects |
| `env-mgr project remove <name>` | Remove a project |
| `env-mgr env add <project> <env>` | Add an environment to a project |
| `env-mgr set <project> <env> <KEY>` | Set (encrypt and store) a variable |
| `env-mgr get <project> <env> <KEY>` | Decrypt and print one variable value |
| `env-mgr pull <project> <env>` | Write all variables to .env file |
| `env-mgr pull <project> <env> --dry-run` | Preview pull without writing |
| `env-mgr pull <project> <env> --output <path>` | Write to a specific path |
| `env-mgr push <project> <env>` | Push vault to sync destination |
| `env-mgr push <project> <env> --destination local --path <path>` | Push to local path |
| `env-mgr diff <project> <env1> <env2>` | Diff two environments |
| `env-mgr config set <key> <value>` | Set a config value |
| `env-mgr config show` | Show configuration |
| `env-mgr --help` | Show help |
| `env-mgr --version` | Show version |

## Environment Variables

| Variable | Description | Default |
|---|---|---|
| `ENVMGR_PORT` | Dashboard port | `7433` |
| `ENVMGR_HOST` | Bind address | `127.0.0.1` |
| `ENVMGR_DATA_DIR` | Vault, config, and database directory | `~/.env-file-manager` |
| `ENVMGR_S3_BUCKET` | S3 bucket name | (from config) |
| `ENVMGR_S3_PREFIX` | S3 key prefix | `vaults/` |
| `ENVMGR_S3_ENDPOINT` | S3-compatible endpoint URL | (AWS default) |
| `ENVMGR_S3_REGION` | AWS region | `us-east-1` |
| `ENVMGR_AWS_ACCESS_KEY_ID` | AWS access key | (from env or ~/.aws) |
| `ENVMGR_AWS_SECRET_ACCESS_KEY` | AWS secret key | (from env or ~/.aws) |
| `ENVMGR_LOG_LEVEL` | Log level: debug, info, warn, error | `info` |

## Troubleshooting

**"wrong passphrase" / auth tag error** - The passphrase entered does not match the one used to create the vault. There is no recovery path. Ensure the passphrase is correct.

**Diff shows all variables as "changed"** - This can happen after re-encrypting a vault (the ciphertexts differ even if values are the same). This is expected behavior - AES-256-GCM uses random IVs, so re-encryption always produces new ciphertexts.

**S3 push fails with AccessDenied** - Check that `ENVMGR_AWS_ACCESS_KEY_ID` and `ENVMGR_AWS_SECRET_ACCESS_KEY` are set, or that `~/.aws/credentials` is configured. The IAM policy must allow `s3:PutObject` and `s3:GetObject` on the bucket.

**`.env` file written with wrong path** - Set the project path: `env-mgr config set project.my-app.path /Users/you/projects/my-app`.

**Session expired during bulk set** - Re-enter the passphrase. Sessions last 15 minutes. Use `env-mgr set` sequentially - each set call checks the in-memory session token.
