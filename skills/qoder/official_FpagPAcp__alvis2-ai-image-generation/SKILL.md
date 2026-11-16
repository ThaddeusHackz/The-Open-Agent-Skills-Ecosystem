---
name: ai-image-generation
description: "Generate AI images with FLUX, Gemini, Grok, Seedream, Reve and 50+ models via SkillBoss API Hub. Models: FLUX Dev LoRA, FLUX.2 Klein LoRA, Gemini 3 Pro Image, Grok Imagine, Seedream 4.5, Reve, ImagineArt. Capabilities: text-to-image, image-to-image, inpainting, LoRA, image editing, upscaling, text rendering. Use for: AI art, product mockups, concept art, social media graphics, marketing visuals, illustrations. Triggers: flux, image generation, ai image, text to image, stable diffusion, generate image, ai art, midjourney alternative, dall-e alternative, text2img, t2i, image generator, ai picture, create image with ai, generative ai, ai illustration, grok image, gemini image"
requires.env: [SkillBoss_API_KEY]
---

# AI Image Generation

Generate images with 50+ AI models via [SkillBoss API Hub](https://api.SkillBoss.co).

## Quick Start

```python
import requests, os

SkillBoss_API_KEY = os.environ["SkillBoss_API_KEY"]
API_BASE = "https://api.SkillBoss.co/v1"

def pilot(body: dict) -> dict:
    r = requests.post(
        f"{API_BASE}/pilot",
        headers={"Authorization": f"Bearer {SkillBoss_API_KEY}", "Content-Type": "application/json"},
        json=body,
        timeout=60,
    )
    return r.json()

# Generate an image (auto-routed to best model)
result = pilot({"type": "image", "inputs": {"prompt": "a cat astronaut in space"}, "prefer": "quality"})
image_url = result["result"]["image_url"]
print(image_url)
```

## Available Models

SkillBoss API Hub �Զ�·��������ͼ������ģ�ͣ�֧�� 50+ ģ�ͣ�������

| Model | Best For |
|-------|----------|
| FLUX Dev LoRA | High quality with custom styles |
| FLUX.2 Klein LoRA | Fast with LoRA support (4B/9B) |
| Gemini 3 Pro | Google's latest |
| Gemini 2.5 Flash | Fast Google model |
| Grok Imagine | xAI's model, multiple aspects |
| Seedream 4.5 | 2K-4K cinematic quality |
| Seedream 4.0 | High quality 2K-4K |
| Seedream 3.0 | Accurate text rendering |
| Reve | Natural language editing, text rendering |
| ImagineArt 1.5 Pro | Ultra-high-fidelity 4K |
| Topaz Upscaler | Professional upscaling |

## Browse All Image Models

```python
# Discover ģʽ����ѯ����֧�ֵ�ͼ������ģ��
result = pilot({"discover": True, "keyword": "image"})
print(result)
```

## Examples

### Text-to-Image (Quality)

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "professional product photo of a coffee mug, studio lighting"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### Fast Generation

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "sunset over mountains"},
    "prefer": "balanced"
})
image_url = result["result"]["image_url"]
```

### Photorealistic Landscape

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "photorealistic landscape with mountains and lake"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### With Aspect Ratio

```python
result = pilot({
    "type": "image",
    "inputs": {
        "prompt": "cyberpunk city at night",
        "aspect_ratio": "16:9"
    },
    "prefer": "balanced"
})
image_url = result["result"]["image_url"]
```

### Text Rendering in Image

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "A poster that says HELLO WORLD in bold letters"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### Cinematic Portrait (4K Quality)

```python
result = pilot({
    "type": "image",
    "inputs": {"prompt": "cinematic portrait of a woman, golden hour lighting"},
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

### Image Upscaling

```python
result = pilot({
    "type": "image",
    "inputs": {
        "prompt": "upscale",
        "image_url": "https://example.com/image.jpg"
    },
    "prefer": "quality"
})
image_url = result["result"]["image_url"]
```

## Response ��ʽ

```python
# ��׼ response ����
result = pilot({"type": "image", "inputs": {"prompt": "..."}, "prefer": "quality"})
image_url = result["result"]["image_url"]
# �򣨲���ģ�ͷ��������ʽ��
image_url = result["result"]["images"][0]["url"]
```

## ��������

| ���� | ˵�� |
|------|------|
| `SkillBoss_API_KEY` | SkillBoss API Hub ͳһ��Կ |

