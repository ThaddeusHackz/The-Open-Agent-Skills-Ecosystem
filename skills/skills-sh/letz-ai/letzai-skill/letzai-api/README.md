# LetzAI API Skill for Claude

An agent skill that teaches Claude how to use the [LetzAI API](https://www.letz.ai) for AI
image and video generation.

## What is This?

With this skill active, Claude can help you:

- **Generate images** with Nano Banana Pro, Seedream 5, Flux 2, GPT Image 2 and more
- **Generate videos** with Veo 3.1, Kling V3, Seedance 2.0 and Gemini Omni Flash — from an image or from text alone
- **Edit images** with context editing and multi-reference composition
- **Upscale** images up to 4K
- **Upload your own files** and use them as sources
- **Train and use custom models** via the `@modelname` syntax

## Repository Structure

```
letzai-skill/
├── SKILL.md                        # Main skill file
├── api_reference.md                # Detailed API reference
├── examples/
│   ├── image_generation.js         # Images, editing, upscaling, trained models
│   ├── video_generation.py         # Text-to-video, image-to-video, multi-shot
│   ├── uploads_and_training.md     # /user-assets uploads + POST /models training
│   └── polling_pattern.md          # Async polling guide
├── LICENSE.txt
└── README.md
```

## Quick Start

1. Get an API key at [letz.ai/subscription](https://letz.ai/subscription)
2. Export it as `LETZAI_API_KEY`
3. Authenticate with `Authorization: Bearer YOUR_API_KEY`

### Installation

**Skills CLI (recommended)** — via [skills.sh](https://skills.sh):

```bash
npx skills add Letz-AI/letzai-skill
```

**Claude Code** — place the skill in `.claude/skills/letzai-api/`.

**Claude.ai** — Settings → Features → Add custom skill (Pro/Max/Team/Enterprise).

**Claude API** — upload through the Skills API.

## Usage Examples

- *"Generate an image of a sunset over the ocean using LetzAI"*
- *"Create a video from this image with the camera slowly panning"*
- *"Edit this photo to change the background to a beach"*
- *"List my trained models and generate an image with @john_doe"*
- *"Upscale this image to 4K"*
- *"Train a new object model from these 20 product photos"*

## API Overview

Base URL: `https://api.letz.ai` · Swagger: [api.letz.ai/doc](https://api.letz.ai/doc)

| Endpoint | Purpose |
|---|---|
| `POST /images` | Generate images |
| `POST /videos` | Generate videos (image-to-video or text-to-video) |
| `POST /image-edits` | Edit existing images |
| `POST /upscale` | Upscale images |
| `POST /user-assets` | Upload your own images, video or audio |
| `GET /models` | List custom trained models |
| `POST /models` | Train a new model |

All generation is asynchronous — poll the matching `GET` until `status` is `ready`, or pass
a `webhookUrl`.

> **Public API vs private API.** `api.letz.ai` is the public developer API.
> `private-api.letz.ai` powers the letz.ai web app and uses different route names
> (`/upscales`, `/image_completions`, `/video-edits`). Those paths 404 here — note in
> particular that the public upscale route is the singular **`/upscale`**.

## Available Models

### Image generation

| Model | `baseModel` | `mode` (resolution) | Credits |
|---|---|---|---|
| Nano Banana Pro | `gemini-3-pro-image` | `default` · `2k` · `4k` | 80 / 160 / 240 |
| Nano Banana 2 | `nbf-inferencesh` | `default` · `2k` · `4k` | 40 / 80 / 160 |
| Nano Banana 2 Lite | `nano-banana-2-lite` | `default` | 20 |
| Seedream 5 Pro | `seedream-5-0-pro` | `2k` · `4k` | 80 / 160 |
| Seedream 4.5 | `seedream-4-5-251128` | `2k` · `4k` | 80 / 160 |
| Flux 2 | `flux2` | `1k` · `hd` | 60 / 120 |
| GPT Image 2 | `gpt-image-2` | `1k` · `hd` · `4k` | 160 / 240 / 480 |
| WAN 2.7 Image Pro | `wan-2-7-image-pro` | `1k` · `2k` | 10 |

### Video generation

Set the model through `settings.mode`, using the `video-` prefixed key.

| Model | `settings.mode` | Duration | Credits |
|---|---|---|---|
| Google Veo 3.1 | `video-veo31` | 8 s | 1500 (×2 audio, ×2 at 1080p) |
| Kling V3 | `video-kling3` | 3–15 s | 150 (300 with audio) |
| Kling V2.6 | `video-kling26` | 5 or 10 s | 150 (×2 audio, ×2 at 1080p) |
| WAN 2.5 | `video-wan25` | 5 or 10 s | 110 (×2 at 1080p) |
| Seedance 2.0 | `video-seedance2` | 4–15 s | 105–1000 per second by resolution |
| Seedance 2.0 Enterprise | `video-seedance2-enterprise` | 4–15 s | as above; needs `organizationId` |
| Gemini Omni Flash | `video-gemini-omni` | 3–10 s | 100 per second |

The live catalogue, including models added after this README, is published at
[letz.ai/docs/models.json](https://letz.ai/docs/models.json).

## Custom Trained Models

Train models on persons, objects or styles and reference them in prompts:

```
@john_doe on the beach at sunset
A product photo featuring @my_product
Portrait in @vintage_style aesthetic
```

Train through the [web interface](https://letz.ai) or via `POST /models` — see
[examples/uploads_and_training.md](examples/uploads_and_training.md).

## Resources

- **Website:** [www.letz.ai](https://www.letz.ai)
- **Swagger / OpenAPI:** [api.letz.ai/doc](https://api.letz.ai/doc) · [`/doc-json`](https://api.letz.ai/doc-json)
- **Developer docs:** [letz.ai/docs/api](https://letz.ai/docs/api)
- **Model catalogue:** [letz.ai/docs/models.json](https://letz.ai/docs/models.json)
- **Get an API key:** [letz.ai/subscription](https://letz.ai/subscription)

## License

MIT — see [LICENSE.txt](LICENSE.txt).

## Disclaimer

Model availability, capabilities and pricing change regularly. The Swagger document at
[api.letz.ai/doc](https://api.letz.ai/doc) and
[letz.ai/docs/models.json](https://letz.ai/docs/models.json) are the authoritative sources;
this skill is a snapshot. Always test against your own account before shipping.
