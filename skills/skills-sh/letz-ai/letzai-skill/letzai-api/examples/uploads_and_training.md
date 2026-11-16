# Uploading Files and Training Custom Models

Two things the LetzAI public API can do that are easy to miss: hosting your own files, and
training custom `@model` LoRAs over HTTP.

## Uploading your own files

Editing, video generation and upscaling all take **public URLs** as sources. If your file
lives on disk, upload it first through `/user-assets`, which hands back a pre-signed S3
URL.

The flow is two steps:

1. `POST /user-assets` with the file extension → returns `uploadUrl` and `imageUrl`
2. `PUT` the raw bytes to `uploadUrl` — **no `Authorization` header**, the URL is signed

After the PUT succeeds, `imageUrl` is the public URL you pass to other endpoints.

### Supported extensions

| Kind | Extensions |
|---|---|
| Images | `jpg`, `jpeg`, `png`, `gif`, `webp` |
| Video | `mp4`, `webm`, `mov`, `avi` |
| Audio | `mp3`, `wav`, `ogg`, `m4a`, `aac`, `flac` |

`POST /user-images` is the older variant of the same flow and accepts images and video
only. Prefer `/user-assets`.

### cURL

```bash
# 1. Ask for an upload URL
RESPONSE=$(curl -sS -X POST https://api.letz.ai/user-assets \
  -H "Authorization: Bearer $LETZAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"extension":"jpg","originalFilename":"photo.jpg","mimeType":"image/jpeg"}')

UPLOAD_URL=$(jq -r '.uploadUrl' <<<"$RESPONSE")
PUBLIC_URL=$(jq -r '.imageUrl'  <<<"$RESPONSE")

# 2. Upload the bytes (no auth header — the URL is pre-signed)
curl -sS -X PUT -H "Content-Type: image/jpeg" \
  --data-binary "@./photo.jpg" "$UPLOAD_URL"

echo "Available at: $PUBLIC_URL"
```

### Node

```javascript
const fs = require('node:fs/promises');
const path = require('node:path');

const API_BASE_URL = 'https://api.letz.ai';
const MIME_TYPES = {
  '.jpg': 'image/jpeg',
  '.jpeg': 'image/jpeg',
  '.png': 'image/png',
  '.webp': 'image/webp',
  '.gif': 'image/gif',
  '.mp4': 'video/mp4',
  '.webm': 'video/webm',
  '.mov': 'video/quicktime',
  '.mp3': 'audio/mpeg',
  '.wav': 'audio/wav',
};

/** Upload a local file and return its public URL. */
async function uploadAsset(filePath, { caption } = {}) {
  const extension = path.extname(filePath).slice(1).toLowerCase();
  const mimeType = MIME_TYPES[`.${extension}`];
  if (!mimeType) throw new Error(`Unsupported extension: .${extension}`);

  const bytes = await fs.readFile(filePath);

  const createResponse = await fetch(`${API_BASE_URL}/user-assets`, {
    method: 'POST',
    headers: {
      Authorization: `Bearer ${process.env.LETZAI_API_KEY}`,
      'Content-Type': 'application/json',
    },
    body: JSON.stringify({
      extension,
      mimeType,
      originalFilename: path.basename(filePath),
      fileSize: bytes.byteLength,
      ...(caption ? { caption } : {}),
    }),
  });

  if (!createResponse.ok) {
    throw new Error(`Could not create upload URL: HTTP ${createResponse.status}`);
  }

  const { uploadUrl, imageUrl } = await createResponse.json();

  // Pre-signed: sending an Authorization header here makes S3 reject the PUT.
  const putResponse = await fetch(uploadUrl, {
    method: 'PUT',
    headers: { 'Content-Type': mimeType },
    body: bytes,
  });

  if (!putResponse.ok) {
    throw new Error(`Upload failed: HTTP ${putResponse.status}`);
  }

  return imageUrl;
}

// Use it as an edit source
const sourceUrl = await uploadAsset('./portrait.jpg');
```

### Python

```python
import mimetypes
import os
from pathlib import Path

import requests

API_BASE_URL = "https://api.letz.ai"


def upload_asset(file_path: str, caption: str | None = None) -> str:
    """Upload a local file and return its public URL."""
    path = Path(file_path)
    extension = path.suffix.lstrip(".").lower()
    mime_type = mimetypes.guess_type(path.name)[0] or "application/octet-stream"
    data = path.read_bytes()

    created = requests.post(
        f"{API_BASE_URL}/user-assets",
        headers={
            "Authorization": f"Bearer {os.environ['LETZAI_API_KEY']}",
            "Content-Type": "application/json",
        },
        json={
            "extension": extension,
            "mimeType": mime_type,
            "originalFilename": path.name,
            "fileSize": len(data),
            **({"caption": caption} if caption else {}),
        },
    )
    created.raise_for_status()
    body = created.json()

    # Pre-signed URL — do not send the Authorization header on this request.
    uploaded = requests.put(
        body["uploadUrl"],
        data=data,
        headers={"Content-Type": mime_type},
    )
    uploaded.raise_for_status()

    return body["imageUrl"]
```

### Managing uploads

| Endpoint | Purpose |
|---|---|
| `GET /user-assets` | List your uploads, newest first (max 100 per page) |
| `GET /user-assets/{id}` | Fetch one |
| `PATCH /user-assets/{id}` | Update `caption` / `metadata` |
| `DELETE /user-assets/{id}` | Delete |

### Batch upload URLs

Set `numberOfImages` on the create call to get several signed URLs in one round trip —
handy when assembling a training set.

```json
{ "extension": "jpg", "numberOfImages": 20 }
```

---

## Training a custom model

`POST /models` trains a LoRA on your own images. It is available over the API on
Enterprise plans; training begins as soon as the model is created.

| Parameter | Required | Notes |
|---|---|---|
| `name` | Yes | Alphanumeric plus `_` and `.`, max 50 chars — this becomes the `@tag` |
| `class` | Yes | `person` · `style` · `object` |
| `privacy` | No | `public` · `private` · `licensed` |
| `type` | No | Auto-generated when omitted |
| `trainingDataUrls` | No | 1–50 publicly reachable image URLs |
| `trainingMode` | No | e.g. `default`, `slow` (person class) |
| `settings` | No | Content flags, e.g. `["NO_ADULT_CONTENT", "NO_VIOLENCE"]` |
| `description`, `website` | No | Metadata |
| `webhookUrl` | No | Called when training finishes |
| `organizationId` | No | Bill the organization |

The name cannot be changed later — `PATCH /models/{id}` accepts `privacy`, `type`,
`description`, `website` and `settings` only.

### End-to-end: upload a training set, then train

```javascript
const trainingImages = [
  './training/01.jpg',
  './training/02.jpg',
  './training/03.jpg',
  // ... up to 50
];

// 1. Host every image
const trainingDataUrls = [];
for (const file of trainingImages) {
  trainingDataUrls.push(await uploadAsset(file));
}

// 2. Kick off training
const createResponse = await fetch('https://api.letz.ai/models', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.LETZAI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    name: 'my_product',
    class: 'object',
    privacy: 'private',
    trainingDataUrls,
    settings: ['NO_ADULT_CONTENT'],
    webhookUrl: 'https://your-server.com/api/letzai/model-trained',
  }),
});

const model = await createResponse.json();

// 3. Training takes minutes, so poll slowly (or just wait for the webhook)
async function waitForModel(modelId) {
  while (true) {
    const response = await fetch(`https://api.letz.ai/models/${modelId}`, {
      headers: { Authorization: `Bearer ${process.env.LETZAI_API_KEY}` },
    });
    const data = await response.json();

    if (data.status === 'available') return data;
    if (data.status === 'failed') throw new Error(data.statusDetail ?? 'Training failed');

    await new Promise((r) => setTimeout(r, 30000));
  }
}

await waitForModel(model.id);

// 4. Use it
await fetch('https://api.letz.ai/images', {
  method: 'POST',
  headers: {
    Authorization: `Bearer ${process.env.LETZAI_API_KEY}`,
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    prompt: 'Studio product shot of @my_product on a marble surface',
    baseModel: 'gemini-3-pro-image',
    mode: '2k',
  }),
});
```

### Model training statuses

`new` → `pending` → `training` → `finished` → `available`, or `failed`.

A model is only usable in prompts once it reaches `available`. Poll at ~30 s intervals, or
pass a `webhookUrl` and skip polling entirely.

### Set a thumbnail

```bash
curl -X PUT "https://api.letz.ai/models/$MODEL_ID/thumbnail" \
  -H "Authorization: Bearer $LETZAI_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{"imageCompletionId":"<uuid-of-a-generated-image>"}'
```
