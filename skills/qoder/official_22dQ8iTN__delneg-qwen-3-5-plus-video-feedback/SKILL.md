---
name: qwen-3-5-plus-video-feedback
description: 'Analyze and reason about a video using Qwen 3.5 Plus via OpenRouter. Use for video feedback, quality assessment, prompt-adherence evaluation, and content description. Accepts public video URLs or local files (uploaded to S3-compatible storage).'
metadata:
  emoji: 🎬
  requires:
    bins:
      - uv
    env:
      - OPENROUTER_API_KEY
  primaryEnv: OPENROUTER_API_KEY
---


# Qwen 3.5 Plus Video Feedback

## Overview

Analyze videos with OpenRouter using the `qwen/qwen3.5-plus-02-15` model. Designed as the feedback loop for Veo 3.1 video generation — pass a generated video and a prompt to get structured analysis and quality feedback.

### Analyze a public video URL

```
uv run {baseDir}/scripts/analyze_video.py \
  --video-url "https://example.com/generated.mp4" \
  --prompt "Does this video match the description: a cat jumping over a fence? Rate quality 1-10."
```

### Analyze a local video file (auto-uploaded to S3)

```
uv run {baseDir}/scripts/analyze_video.py \
  --video-file /path/to/video.mp4 \
  --prompt "Describe what is happening in this video and assess its overall visual quality."
```

### Save analysis to a file

```
uv run {baseDir}/scripts/analyze_video.py \
  --video-url "https://example.com/clip.mp4" \
  --prompt "Evaluate prompt adherence and suggest improvements." \
  --output feedback.txt
```

## Arguments

| Argument | Required | Description |
|----------|----------|-------------|
| `--prompt` | Yes | Question or instruction for the model |
| `--video-url` | One of these | Public or presigned URL to the video |
| `--video-file` | One of these | Path to a local video file (uploaded to S3, then analyzed via presigned URL) |
| `--output` | No | File path to save the analysis text |

`--video-url` and `--video-file` are mutually exclusive.

## S3 Configuration (required for `--video-file`)

Local files are uploaded to an S3-compatible bucket and accessed via a presigned URL (valid 1 hour). Set these environment variables:

| Variable | Required | Description |
|----------|----------|-------------|
| `S3_ENDPOINT_URL` | Yes | e.g. `https://s3.us-east-1.amazonaws.com` or `https://nyc3.digitaloceanspaces.com` |
| `S3_ACCESS_KEY_ID` | Yes | Access key ID |
| `S3_SECRET_ACCESS_KEY` | Yes | Secret access key |
| `S3_BUCKET` | Yes | Bucket name |
| `S3_REGION` | No | Region (default: `us-east-1`) |
| `S3_KEY_PREFIX` | No | Key prefix for uploads (default: `video-analysis/`) |

The bucket does **not** need to be public — presigned URLs are used.

## Supported video formats

`video/mp4`, `video/mpeg`, `video/mov`, `video/webm`

## System prompt customization

The skill reads an optional system prompt from `assets/SYSTEM_TEMPLATE`. Edit it to tune the model's feedback style (scoring rubric, artifact checklist, output format).

## Behavior

- When `--video-file` is used: uploads the file to S3, generates a presigned URL, passes it to the model. Upload progress is printed to stderr.
- Prints the full analysis to stdout.
- If `--output` is provided, also writes the text to that file and prints `Analysis saved to: <path>`.

## Chaining with veo3-1

```bash
VIDEO_URL=$(uv run veo3-1/scripts/generate_video.py --prompt "..." --url-only | grep '^VIDEO_URL:' | cut -d' ' -f2)
uv run {baseDir}/scripts/analyze_video.py \
  --video-url "$VIDEO_URL" \
  --prompt "Evaluate prompt adherence, list artifacts, rate 1-10."
```

## Troubleshooting

| Symptom | Resolution |
|---------|------------|
| `OPENROUTER_API_KEY is not set` | `export OPENROUTER_API_KEY="sk-or-..."` |
| `S3_ENDPOINT_URL is not set` | Set S3 env vars (see S3 Configuration above) |
| `Video file not found` | Check the path passed to `--video-file` |
| `AuthenticationError` / HTTP 401 | Key invalid or out of credits. Check <https://openrouter.ai/settings/keys>. |
| `Missing Content-Length` / upstream error | The provider doesn't support base64 data URLs — use `--video-file` (S3 upload) or `--video-url` with a direct HTTP URL. |
| `uv: command not found` | macOS/Linux: `curl -LsSf https://astral.sh/uv/install.sh \| sh`. Restart terminal. |

For transient errors (HTTP 429, network timeouts), retry once after 30 seconds. Do not retry the same error more than twice — surface it to the user instead.
