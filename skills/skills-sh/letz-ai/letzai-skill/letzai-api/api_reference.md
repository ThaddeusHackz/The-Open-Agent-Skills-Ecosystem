# LetzAI API Reference

Complete reference for the LetzAI **public** API.

Generated against the live OpenAPI document at
[api.letz.ai/doc-json](https://api.letz.ai/doc-json). When this file and the Swagger
document disagree, Swagger wins.

## Base Configuration

| Property | Value |
|---|---|
| Base URL | `https://api.letz.ai` |
| Authentication | `Authorization: Bearer YOUR_API_KEY` |
| Content-Type | `application/json` |
| Swagger UI | [api.letz.ai/doc](https://api.letz.ai/doc) |
| OpenAPI JSON / YAML | `/doc-json` · `/doc-yaml` |

Get your API key at [letz.ai/subscription](https://letz.ai/subscription).

### Public API vs private API

LetzAI runs two surfaces from the same backend:

| | Public (`api.letz.ai`) | Private (`private-api.letz.ai`) |
|---|---|---|
| Audience | Third-party developers | The letz.ai web app |
| Auth | Integration Bearer token | Session JWT |
| Images | `/images` | `/image_completions` |
| Upscaling | `/upscale` | `/upscales` |
| Video edits | *not available* | `/video-edits` |
| Video interrupt | *not available* | `PUT /videos/{id}/interruption` |

Everything below describes the **public** surface. Blog posts, older SDK snippets and the
web app's own network traffic sometimes reference the private routes; those return `404`
against `api.letz.ai`.

### Request validation

Bodies are validated strictly and unknown properties are rejected with `400`. Fields such
as `negativePrompt`, `seed` and `aspectRatio` do **not** exist on `POST /images`.

### Pagination

List endpoints return the page as the body and the counts as response headers:

| Header | Meaning |
|---|---|
| `X-Total-Count` | Total matching items |
| `X-Current-Page` | Current page |
| `X-Per-Page` | Page size |
| `X-Total-Pages` | Total pages |

---

## Image Generation

### Create image

**`POST /images`**

| Parameter | Type | Required | Default | Constraints |
|---|---|---|---|---|
| `prompt` | string | Yes | — | May contain `@modelname` tags |
| `baseModel` | string | No | account default | ≤255 chars |
| `mode` | string | No | model default | Resolution tier, model-specific |
| `width` | number | No | `1600` | 480–2160 |
| `height` | number | No | `1600` | 480–2160 |
| `quality` | number | No | `2` | 1–6 |
| `creativity` | number | No | `2` | 1–6 |
| `hasWatermark` | boolean | No | `true` | |
| `systemVersion` | number | No | account default | `2` or `3` |
| `hideFromUserProfile` | boolean | No | `false` | |
| `webhookUrl` | string | No | — | Valid URL |
| `organizationId` | string | No | — | UUID v4; you must be a member |

> **`mode` is the resolution tier**, not a generation style. The OpenAPI document
> currently declares `mode` with an `enum: ["default", "sigma"]`; that decorator is stale
> and is not enforced. The values the platform actually uses are `default`, `1k`, `2k`,
> `hd`, `4k` and `uhd`, and each model supports only a subset. The system-version selector
> is the separate `systemVersion` field.

#### Available base models

| Model | `baseModel` | `mode` values | Generate credits | Edit credits |
|---|---|---|---|---|
| Nano Banana Pro | `gemini-3-pro-image` | `default` (1K) · `2k` (HD) · `4k` | 80 / 160 / 240 | 80 / 160 / 240 |
| Nano Banana 2 | `nbf-inferencesh` | `default` (1K) · `2k` (HD) · `4k` | 40 / 80 / 160 | 50 / 100 / 150 |
| Nano Banana 2 Lite | `nano-banana-2-lite` | `default` (1K) | 20 | 25 |
| Seedream 5 Pro | `seedream-5-0-pro` | `2k` (HD) · `4k` | 80 / 160 | 80 / 160 |
| Seedream 4.5 | `seedream-4-5-251128` | `2k` (HD) · `4k` | 80 / 160 | 80 / 160 |
| Flux 2 | `flux2` | `1k` · `hd` | 60 / 120 | 60 / 120 |
| GPT Image 2 | `gpt-image-2` | `1k` · `hd` · `4k` | 160 / 240 / 480 | 160 / 240 / 480 |
| WAN 2.7 Image Pro | `wan-2-7-image-pro` | `1k` · `2k` | 10 | 10 |

Common aliases also resolve: `gemini-3-pro-image-preview` → Nano Banana Pro,
`flux-2` / `flux2-max` → Flux 2, `seedream-4-5` → Seedream 4.5, `seedream-5` → Seedream 5 Pro.
The authoritative, always-current catalogue is
[letz.ai/docs/models.json](https://letz.ai/docs/models.json).

#### Example request

```json
{
  "prompt": "A majestic mountain landscape at sunset with golden light",
  "baseModel": "gemini-3-pro-image",
  "mode": "2k",
  "width": 1920,
  "height": 1080
}
```

#### Response — `201`

Returns an `ImageDto`. Immediately after creation only the job fields are populated:

```json
{
  "id": "6f1c1f4e-4c2a-4c07-9b5e-2b2f0a4d9f11",
  "status": "new",
  "progress": 0,
  "prompt": "A majestic mountain landscape at sunset with golden light",
  "baseModel": "gemini-3-pro-image",
  "privacy": "private",
  "hasWatermark": true,
  "imageVersions": {},
  "createdAt": "2026-07-28T10:00:00.000Z"
}
```

#### Errors

| Code | Cause |
|---|---|
| 400 | `width`/`height` outside 480–2160, `quality`/`creativity` outside 1–6, `systemVersion` not 2 or 3, malformed `organizationId`, unknown model referenced in the prompt |
| 401 | Missing/invalid token, or not a member of the organization |
| 402 | Insufficient credits |
| 500 | Server error |

### Get image

**`GET /images/{id}`** — `id` is a UUID.

```json
{
  "id": "6f1c1f4e-4c2a-4c07-9b5e-2b2f0a4d9f11",
  "status": "ready",
  "progress": 100,
  "prompt": "A majestic mountain landscape at sunset",
  "baseModel": "gemini-3-pro-image",
  "imageVersions": {
    "original": "https://images.letz.ai/.../original.png",
    "1920x1920": "https://images.letz.ai/.../1920x1920.png",
    "640x640": "https://images.letz.ai/.../640x640.png"
  },
  "generationSettings": { "width": 1920, "height": 1080, "quality": 2, "creativity": 2, "mode": "2k" },
  "models": [],
  "privacy": "private",
  "createdAt": "2026-07-28T10:00:00.000Z"
}
```

While generating, `previewImage` holds a base64 preview and `progress` counts to 100.
On failure, `statusDetail` carries the worker's error message.

### List images

**`GET /images`**

| Query | Default | Notes |
|---|---|---|
| `page` | `1` | |
| `limit` | `10` | 1–50 |
| `sortBy` | — | e.g. `createdAt`, `likes`, `regenerations` |
| `sortOrder` | — | `ASC` \| `DESC` |
| `userId` / `username` | — | Filter by creator |
| `privacy` | — | `public` \| `private` \| `licensed` |
| `systemVersion` | — | |
| `isHot` | — | |
| `includeNsfw` | `false` | |
| `onlyFollowing` | — | |
| `modelIds` | — | Filter by trained models used |
| `status` | — | See status values |

### Interrupt image generation

**`PUT /images/{id}/interruption`** — stops an in-flight job. Returns `204`.

### Change image privacy

**`PUT /images/{id}/privacy`**

```json
{ "privacy": "public" }
```

`privacy` is one of `public`, `private`, `licensed`. Public images appear on the LetzAI feed.

### Change prompt privacy

**`PUT /images/{id}/prompt-privacy`** — hides or reveals the prompt on public listings.

---

## Video Generation

### Create video

**`POST /videos`**

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `prompt` | string | Yes | |
| `originalImageCompletionId` | string | No | UUID of a LetzAI image to animate |
| `imageUrl` | string | No | Public source image URL |
| `imageUrls` | string[] | No | Multi-frame: `[0]` first frame, `[1]` last frame |
| `prompts` | object[] | No | Multi-shot: `[{ "prompt": "...", "duration": 3 }]` |
| `width` / `height` | number | No | |
| `resolution` | number | No | |
| `baseModel` | string | No | ≤255 chars; merged into `settings` |
| `settings` | object | No | See below |
| `webhookUrl` | string | No | |
| `hidePrompt` | boolean | No | Default `false` |
| `organizationId` | string | No | UUID |

**A source image is optional.** Omit all image inputs for text-to-video. (Some Swagger
descriptions still say an image input is required; the service does not enforce it.)

#### `settings`

| Field | Type | Notes |
|---|---|---|
| `mode` | string | Video model key — see table below |
| `duration` | number | Seconds; clamped to the model's allowed values |
| `withSound` | boolean | Native audio, where supported |
| `highQuality` | boolean | Higher-resolution tier; typically ×2 credits |
| `resolution` | string | `"480p"` · `"720p"` · `"1080p"` · `"4k"` for per-second models |

#### Available video models

`settings.mode` uses the `video-` prefixed key.

| Model | `settings.mode` | Duration | Audio | Credits |
|---|---|---|---|---|
| Google Veo 3.1 | `video-veo31` | 8 s fixed | opt-in | 1500 flat · ×2 with audio · ×2 at 1080p |
| Kling V3 | `video-kling3` | 3–15 s | opt-in | 150 flat · 300 with audio |
| Kling V2.6 | `video-kling26` | 5 or 10 s | opt-in | 150 flat · ×2 with audio · ×2 at 1080p |
| WAN 2.5 | `video-wan25` | 5 or 10 s | no | 110 flat · ×2 at 1080p |
| Seedance 2.0 | `video-seedance2` | 4–15 s | always | per second: 105 @480p · 210 @720p · 500 @1080p · 1000 @4K |
| Seedance 2.0 Enterprise | `video-seedance2-enterprise` | 4–15 s | always | same as above; requires `organizationId` |
| Gemini Omni Flash | `video-gemini-omni` | 3–10 s | always | 100 per second |

Capabilities worth knowing:

- `video-veo31` and `video-kling3` support first/last-frame control via `imageUrls`.
- `video-kling3` supports multi-shot storyboards via the top-level `prompts` array
  (minimum 3 s per shot, 15 s total).
- `video-wan25` is image-to-video only.

#### Example request

```json
{
  "prompt": "The camera slowly pans across the mountain as clouds drift by",
  "originalImageCompletionId": "6f1c1f4e-4c2a-4c07-9b5e-2b2f0a4d9f11",
  "settings": {
    "mode": "video-kling26",
    "duration": 5,
    "withSound": false
  }
}
```

#### Response — `201`

```json
{
  "id": "0a6d9e28-9a3b-4d2c-8b3f-9f8a13c4e5d6",
  "status": "new",
  "progress": 0,
  "prompt": "The camera slowly pans across the mountain as clouds drift by",
  "settings": { "mode": "video-kling26", "duration": 5 },
  "privacy": "private",
  "createdAt": "2026-07-28T10:05:00.000Z"
}
```

### Get video

**`GET /videos/{id}`**

```json
{
  "id": "0a6d9e28-9a3b-4d2c-8b3f-9f8a13c4e5d6",
  "status": "ready",
  "progress": 100,
  "videoVersions": { "original": "https://videos.letz.ai/.../original.mp4" },
  "previewImage": "https://images.letz.ai/.../thumb.jpg",
  "settings": { "mode": "video-kling26", "duration": 5 },
  "createdAt": "2026-07-28T10:05:00.000Z"
}
```

Read the finished video from `videoVersions.original`. (`videoPaths` is an internal field
and is not part of the public contract.)

### List videos

**`GET /videos`** — `page`, `limit` (1–50), `sortBy`, `sortOrder`, `userId`, `username`,
`status`, `width`, `height`, `resolution`, `prompt`, `hidePrompt`.

### Video privacy

**`PUT /videos/{id}/privacy`** — body `{ "privacy": "public" }`.
**`PUT /videos/{id}/prompt-privacy`** — hide/show the prompt publicly.

There is **no** `PUT /videos/{id}/interruption` on the public API.

---

## Image Editing

### Create image edit

**`POST /image-edits`**

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `mode` | string | Yes | `context`, `skin` (or legacy `in` / `out`); ≤32 chars |
| `prompt` | string | No | Edit instruction; may contain `@modelname` |
| `imageUrl` | string | No | Single source image URL |
| `inputImageUrls` | string[] | No | Multiple source images (up to 9 in practice) |
| `originalImageCompletionId` | string | No | UUID of a LetzAI image |
| `originalImageCompletionIds` | string[] | No | Several LetzAI images |
| `baseModel` | string | No | Same identifiers as image generation |
| `settings` | object | No | `resolution`, `aspect_ratio`, `model` |
| `imageCompletionsCount` | number | No | Variations, 1–5 (default 1); ignored by `skin` |
| `mask` | string | No | Base64 mask; legacy inpainting only |
| `width` / `height` | number | No | Target dimensions |
| `generationSeconds` | number | No | Overrides the fixed credit cost for the mode |
| `webhookUrl` | string | No | |
| `hidePrompt` | boolean | No | Default `false` |
| `organizationId` | string | No | UUID |

Provide at least one source (`imageUrl`, `inputImageUrls`, `originalImageCompletionId`
or `originalImageCompletionIds`).

#### `settings`

| Field | Values |
|---|---|
| `resolution` | `"2k"` (HD) · `"4k"` (Ultra HD) |
| `aspect_ratio` | `"1:1"` · `"16:9"` · `"9:16"` · `"4:3"` · `"3:4"` · `"21:9"` · `"9:21"` |
| `model` | Same identifiers as `baseModel` |

`baseModel` is what the backend uses to route the job to a provider queue; `settings.model`
is forwarded to the worker. Set both to the same value, or just set `baseModel`.

#### Edit modes

| Mode | Description |
|---|---|
| `context` | AI-powered contextual editing — the primary mode |
| `skin` | Skin fix / enhancement |
| `in` | Inpainting — **deprecated**, use `context` |
| `out` | Outpainting — **deprecated**, use `context` |

#### Example — single image

```json
{
  "mode": "context",
  "prompt": "Change the background to a tropical beach with palm trees",
  "imageUrl": "https://example.com/my-photo.jpg",
  "baseModel": "gemini-3-pro-image",
  "settings": {
    "resolution": "2k",
    "aspect_ratio": "16:9",
    "model": "gemini-3-pro-image"
  }
}
```

#### Example — multi-reference

```json
{
  "mode": "context",
  "prompt": "Put the jacket from image 2 on the person in image 1",
  "inputImageUrls": [
    "https://example.com/person.jpg",
    "https://example.com/jacket.jpg"
  ],
  "baseModel": "seedream-5-0-pro",
  "settings": { "resolution": "4k", "model": "seedream-5-0-pro" }
}
```

### Get image edit

**`GET /image-edits/{id}`**

```json
{
  "id": "8b7c1a90-2f44-4c11-a1cd-3d6e4c2b7a90",
  "status": "ready",
  "progress": 100,
  "mode": "context",
  "prompt": "Change the background to a tropical beach",
  "originalImageCompletion": {
    "imageVersions": { "original": "https://images.letz.ai/.../original.png" }
  },
  "generatedImageCompletion": {
    "imageVersions": {
      "original": "https://images.letz.ai/.../edited-original.png",
      "1920x1920": "https://images.letz.ai/.../edited-1920x1920.png",
      "640x640": "https://images.letz.ai/.../edited-640x640.png"
    }
  },
  "imageCompletionChoices": [],
  "settings": { "resolution": "2k", "aspect_ratio": "16:9" },
  "createdAt": "2026-07-28T10:10:00.000Z"
}
```

The result is `generatedImageCompletion.imageVersions.original`. When
`imageCompletionsCount > 1`, the extra variations are listed in `imageCompletionChoices`.

### List image edits

**`GET /image-edits`** — `page`, `limit` (default 20), `sortBy` (`createdAt`, `status`),
`sortOrder`, `status`.

### Get inpainting mask

**`GET /image-edits/{imageCompletionId}/mask`** — returns the mask used for a legacy
inpainting edit.

---

## Upscaling

> The public route is **`/upscale`** (singular). `/upscales` belongs to the private API and
> returns `404` here.

### Create upscale

**`POST /upscale`**

| Parameter | Type | Required | Default | Notes |
|---|---|---|---|---|
| `imageId` | string | Conditional | — | UUID of a LetzAI image completion |
| `imageUrl` | string | Conditional | — | Public image URL; use instead of `imageId` |
| `mode` | string | No | `default` | Upscaler model, ≤32 chars |
| `size` | number | No | — | 2–12; output tier — see table |
| `strength` | number | No | `1` | 1–5 |
| `prompt` | string | No | — | Guidance for creative upscalers |
| `webhookUrl` | string | No | — | |
| `organizationId` | string | No | — | UUID |

#### Upscale modes

| `mode` | Upscaler | `size` → output | Credits |
|---|---|---|---|
| `nano-banana-pro` | Google Gemini 3 Pro | 4 → 1K · 8 → 2K · 12 → 4K | 80 / 160 / 240 |
| `nano-banana-2` | Google Gemini 3.1 Flash | 4 → 1K · 8 → 2K · 12 → 4K | 50 / 100 / 150 |
| `gpt-image-2` | OpenAI GPT Image 2 | 4 → 1K · 8 → 2K · 12 → 4K | 160 / 240 / 480 |
| `pruna` | Pruna P-Image-Upscale | 4 → 1 MP · 8 → 4 MP · 12 → 16 MP | 20 / 40 / 80 |
| `default` | LetzAI in-house | — | 20 |

To upscale your own file, upload it through `/user-assets` first and pass the returned
`imageUrl`. The public route accepts no `assetId`, `assetUrl` or `type` field.

#### Example

```json
{
  "imageId": "6f1c1f4e-4c2a-4c07-9b5e-2b2f0a4d9f11",
  "mode": "nano-banana-pro",
  "size": 8,
  "strength": 2
}
```

### Get / list / delete upscales

- **`GET /upscale/{id}`** — status and `imageVersions`
- **`GET /upscale`** — `page`, `limit` (1–50), `sortBy`, `sortOrder`, `userId`, `username`, `imageId`, `onlyFollowing`, `status`
- **`DELETE /upscale/{id}`**

---

## User Assets (uploads)

Two-step pre-signed S3 upload for using your own files as sources.

### Create an upload URL

**`POST /user-assets`**

| Parameter | Type | Required | Notes |
|---|---|---|---|
| `extension` | string | Yes | `jpg`, `jpeg`, `png`, `gif`, `webp`, `mp4`, `webm`, `mov`, `avi`, `mp3`, `wav`, `ogg`, `m4a`, `aac`, `flac` |
| `numberOfImages` | number | No | Default `1`; generate several upload URLs at once |
| `originalFilename` | string | No | Stored for reference only |
| `mimeType` | string | No | e.g. `image/jpeg` |
| `fileSize` | number | No | Bytes |
| `caption` | string | No | |
| `metadata` | object | No | Arbitrary JSON |

Response contains `uploadUrl` (pre-signed) and `imageUrl` (where the file will live).

### Upload the bytes

`PUT` the raw file to `uploadUrl` with the matching `Content-Type`. **Send no
`Authorization` header** — the URL is already signed.

```bash
curl -X PUT -H "Content-Type: image/jpeg" \
  --data-binary "@/path/to/image.jpg" \
  "https://<pre-signed-url-from-response>"
```

### Manage assets

- **`GET /user-assets`** — newest first, max 100 per page
- **`GET /user-assets/{id}`**
- **`PATCH /user-assets/{id}`** — update `caption` / `metadata`
- **`DELETE /user-assets/{id}`**

### Legacy: user images

`POST /user-images`, `GET /user-images`, `GET /user-images/{id}`,
`DELETE /user-images/{id}` implement the same flow but accept image and video extensions
only. Prefer `/user-assets`.

---

## Custom AI Models

Trained models are referenced inside prompts with `@modelname`.

### List models

**`GET /models`**

| Query | Notes |
|---|---|
| `page`, `limit` | Pagination |
| `sortBy`, `sortOrder` | `ASC` \| `DESC` |
| `search` | Free-text search |
| `name`, `userId`, `username`, `description` | Filters |
| `class` | `person` \| `object` \| `style` |
| `type` | Model type |
| `privacy` | `public` \| `private` \| `licensed` |
| `systemVersion`, `isActive`, `status` | Filters |

Counts come back in the `X-Total-Count` / `X-Current-Page` / `X-Per-Page` /
`X-Total-Pages` headers.

Model classes:

| Class | Trained on |
|---|---|
| `person` | Photos of a specific person |
| `object` | Product / object images |
| `style` | Artistic style examples |

### Get model

**`GET /models/{id}`** — returns id, name, class, type, status, progress, privacy,
usages, thumbnail, settings, versions, and the owning user.

### Train a model

**`POST /models`** — available over the API on Enterprise plans. Training starts
automatically.

| Parameter | Required | Notes |
|---|---|---|
| `name` | Yes | Alphanumeric plus `_` and `.`, max 50 chars — this becomes the `@tag` |
| `class` | Yes | `person` \| `style` \| `object` |
| `privacy` | No | `public` \| `private` \| `licensed` |
| `type` | No | Auto-generated when omitted |
| `trainingDataUrls` | No | 1–50 publicly reachable image URLs |
| `trainingMode` | No | e.g. `default`, `slow` (person class) |
| `settings` | No | e.g. `["NO_ADULT_CONTENT", "NO_VIOLENCE"]` |
| `description`, `website` | No | |
| `webhookUrl` | No | Called when training finishes |
| `organizationId` | No | Bill the organization |

```json
{
  "name": "my_product",
  "class": "object",
  "privacy": "private",
  "trainingDataUrls": [
    "https://images.letz.ai/user-assets/.../1.jpg",
    "https://images.letz.ai/user-assets/.../2.jpg"
  ],
  "settings": ["NO_ADULT_CONTENT"]
}
```

Poll `GET /models/{id}` until `status` is `available`.

### Update / delete / thumbnail

- **`PATCH /models/{id}`** — `privacy`, `type`, `description`, `website`, `settings`
  (the name cannot be changed)
- **`DELETE /models/{id}`**
- **`PUT /models/{id}/thumbnail`** — body `{ "imageCompletionId": "<uuid>" }`

### Using models in prompts

```json
{ "prompt": "@john_doe on the beach at sunset", "baseModel": "gemini-3-pro-image", "mode": "2k" }
{ "prompt": "Product photo of @my_product in studio lighting", "baseModel": "flux2", "mode": "hd" }
{ "prompt": "Portrait of a woman in @vintage_style aesthetic", "baseModel": "seedream-5-0-pro", "mode": "2k" }
```

The models resolved from a prompt come back in the `models` array on the completion.

---

## Status Values

| Resource | Statuses |
|---|---|
| Images | `new`, `generating`, `ready`, `hidden`, `failed`, `interrupted`, `not_allowed` |
| Videos | `new`, `generating`, `ready`, `saved`, `failed`, `interrupted` |
| Image edits | `new`, `generating`, `ready`, `saved`, `failed`, `interrupted` |
| Upscales | `new`, `generating`, `ready`, `failed` |
| Models | `new`, `pending`, `training`, `finished`, `available`, `failed` |

Treat `ready` (and `saved` for videos/edits) as success. `failed`, `interrupted` and
`not_allowed` are terminal failures — `statusDetail` explains why.

There is no `"in progress"` status; older documentation that mentions it is wrong.

---

## Error Responses

| Code | Meaning |
|---|---|
| 200 | Success |
| 201 | Created |
| 400 | Bad request — invalid parameter, or an unknown field in the body |
| 401 | Unauthorized — bad token, or not a member of `organizationId` |
| 402 | Payment required — insufficient credits |
| 404 | Not found — bad id, or a route that only exists on the private API |
| 429 | Too many requests |
| 500 | Internal server error |

Errors follow the NestJS shape:

```json
{
  "statusCode": 400,
  "message": ["width must not be less than 480"],
  "error": "Bad Request"
}
```

`message` is a string for single errors and an array for validation failures.

---

## Webhooks

Pass `webhookUrl` on any create call (`/images`, `/videos`, `/image-edits`, `/upscale`,
`/models`) and LetzAI will `POST` to it when the job reaches a terminal state:

```json
{
  "prompt": "A beautiful landscape",
  "baseModel": "gemini-3-pro-image",
  "webhookUrl": "https://your-server.com/api/letzai/callback"
}
```

The callback body is the same DTO you would get from the corresponding `GET`. Because
webhooks can be lost or delayed, keep a polling fallback for anything critical. Verify the
job id against your own records before acting on a callback.
