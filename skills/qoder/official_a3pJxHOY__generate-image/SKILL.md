---
name: generate-image
description: Generate images for slide presentations using OpenRouter's Gemini 3.1 Flash Image Preview model. Use this skill when the user asks to generate, create, or make an image for a slide deck, presentation, or any visual content needed in slides. Also trigger when creating slides that need illustrations, diagrams, backgrounds, or any AI-generated imagery.
---

# Generate Image for Presentations

Generate images using OpenRouter's `google/gemini-3.1-flash-image-preview` model and save them to the project for use in slide decks.

## How to generate an image

Use `curl` to call the OpenRouter API. The API key is stored in `.env.local` as `OPENROUTER_API_KEY`.

### Step 1: Generate the image

Run this command (substitute the prompt):

```bash
source /Users/pineapp/slide/.env.local && curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-3.1-flash-image-preview",
    "messages": [
      {
        "role": "user",
        "content": "Generate an image: YOUR_PROMPT_HERE"
      }
    ]
  }'
```

### Step 2: Extract and save the image

The response contains the image in the `message.images` array (not in `content`). Each image has `type: "image_url"` and `image_url.url` containing a `data:image/png;base64,...` data URL. Extract the base64 data and save to `public/images/`:

```bash
echo "$RESPONSE" | node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('/dev/stdin','utf8'));
if (data.error) { console.error('API Error:', JSON.stringify(data.error)); process.exit(1); }
const msg = data.choices[0].message;
if (msg.images && msg.images.length > 0) {
  const url = msg.images[0].image_url.url;
  const b64 = url.replace(/^data:image\/\w+;base64,/, '');
  fs.writeFileSync('public/images/FILENAME.png', Buffer.from(b64, 'base64'));
  console.log('Image saved to public/images/FILENAME.png');
} else {
  console.error('No images in response');
}
"
```

### Practical approach

In practice, combine it into a single bash script. Here's the recommended pattern:

```bash
source /Users/pineapp/slide/.env.local

RESPONSE=$(curl -s https://openrouter.ai/api/v1/chat/completions \
  -H "Authorization: Bearer $OPENROUTER_API_KEY" \
  -H "Content-Type: application/json" \
  -d '{
    "model": "google/gemini-3.1-flash-image-preview",
    "messages": [
      {
        "role": "user",
        "content": "Generate an image: A futuristic city skyline at sunset with neon lights"
      }
    ]
  }')

echo "$RESPONSE" | node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('/dev/stdin','utf8'));
if (data.error) { console.error('API Error:', JSON.stringify(data.error)); process.exit(1); }
const msg = data.choices[0].message;
if (msg.images && msg.images.length > 0) {
  const url = msg.images[0].image_url.url;
  const b64 = url.replace(/^data:image\/\w+;base64,/, '');
  fs.writeFileSync('public/images/FILENAME.png', Buffer.from(b64, 'base64'));
  console.log('Image saved to public/images/FILENAME.png');
} else {
  console.error('No images found in response');
  console.log('Message keys:', Object.keys(msg));
}
"
```

### Helper: Generate multiple images

For batch generation, use a shell function:

```bash
source /Users/pineapp/slide/.env.local

generate_image() {
  local PROMPT="$1"
  local FILENAME="$2"

  RESPONSE=$(curl -s https://openrouter.ai/api/v1/chat/completions \
    -H "Authorization: Bearer $OPENROUTER_API_KEY" \
    -H "Content-Type: application/json" \
    -d "{
      \"model\": \"google/gemini-3.1-flash-image-preview\",
      \"messages\": [{\"role\": \"user\", \"content\": \"Generate an image: $PROMPT\"}]
    }")

  echo "$RESPONSE" | node -e "
const fs = require('fs');
const data = JSON.parse(fs.readFileSync('/dev/stdin','utf8'));
if (data.error) { console.error('Error:', JSON.stringify(data.error)); process.exit(1); }
const msg = data.choices[0].message;
if (msg.images && msg.images.length > 0) {
  const url = msg.images[0].image_url.url;
  const b64 = url.replace(/^data:image\/\w+;base64,/, '');
  fs.writeFileSync('public/images/${FILENAME}', Buffer.from(b64, 'base64'));
  console.log('Saved: ${FILENAME}');
} else {
  console.error('No images for ${FILENAME}');
}
"
}

# Usage:
generate_image "A dark futuristic cityscape with neon lights" "hero-city.png"
generate_image "Abstract neural network on black background" "neural-net.png"
```

## File naming convention

Save images to `public/images/` with descriptive kebab-case names:
- `public/images/hero-cityscape.png`
- `public/images/team-collaboration.png`
- `public/images/data-flow-diagram.png`

## Using images in slides

Reference generated images in slide decks using Next.js `<img>` tags:

```tsx
<Slide>
  <img
    src="/images/hero-cityscape.png"
    alt="Futuristic cityscape"
    className="rounded-2xl shadow-2xl max-h-[60vh] object-contain"
  />
  <h2 className="text-4xl font-bold text-white mt-6">The Future of Cities</h2>
</Slide>
```

Or as a background using the `bg` prop:

```tsx
<Slide bg="url('/images/hero-cityscape.png') center/cover no-repeat">
  <div className="bg-black/50 rounded-2xl p-8">
    <h2 className="text-5xl font-bold text-white">The Future of Cities</h2>
  </div>
</Slide>
```

## Image prompt tips for presentations

- Be specific about style: "flat illustration", "3D render", "minimalist", "photorealistic"
- Specify aspect ratio needs: "wide landscape format" for full-bleed backgrounds
- Include color guidance: "using dark blues and purples" to match slide themes
- For diagrams: describe the layout explicitly
- Keep backgrounds simple if text will overlay them

## Important notes

- Always check the API response for errors before trying to extract image data
- The OpenRouter API key is in `.env.local` — never hardcode it
- Generated images go in `public/images/` so they're served statically by Next.js
- Use meaningful filenames that describe the image content
