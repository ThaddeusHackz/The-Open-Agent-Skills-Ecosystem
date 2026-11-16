---
name: linkedin-video-dl
description: 一个基于Go语言构建的工具，用于从公开的LinkedIn帖子中下载MP4视频。无需身份验证或API密钥，支持进度显示、断点续传保护及自动文件名生成。
---

SKILL.md

# linkedin-video-dl

Use linkedin-video-dl to download videos from LinkedIn posts. Takes a public post URL and saves the MP4 video to the current directory. No authentication required for public posts.

## Setup (once)

```bash
cd linkedin-video-dl && go build -o linkedin-video-dl .
```

Or install globally:

```bash
go install .
```

## Common commands

Download video:          `linkedin-video-dl "<post-url>"`

## Example

```bash
linkedin-video-dl "https://www.linkedin.com/posts/midudev_anthropic-ha-acusado-a-deepseek-activity-7432111870431449089-9evi"
```

## Notes

- Only works with **public** LinkedIn posts that contain video.
- No authentication or API keys needed.
- Zero external dependencies — built entirely with Go's standard library.
- Videos are downloaded from LinkedIn's CDN (`dms.licdn.com`) at the best available quality.
- Downloads use a temporary `.tmp` file and rename on completion — safe to interrupt without leaving corrupt files.
- Output filename is derived from the post URL slug (truncated to 80 chars).
- If a file with the same name already exists, the download is skipped to avoid overwriting.
- Progress bar is shown during download with percentage, downloaded size, and total size.
