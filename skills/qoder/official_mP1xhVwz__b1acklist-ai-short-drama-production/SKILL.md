---
name: ai-short-drama-production
description: Create a complete AI short-drama production package from an outline, episode script, novel excerpt, or rough idea. Use for Chinese/Douyin/Hongguo-style vertical short dramas when the user needs project folders, character bibles, cinematic character concept board prompts and images, character lock prompts, scene bible, detailed storyboard markdown, first-frame prompts/images, 3x3 storyboard board prompts/images, Jimeng/Seedance image-to-video prompts, voice generation prompts, audio-role notes, asset index, and QA checklist.
---

# AI Short Drama Production

## Overview

Turn a short-drama idea or episode into a complete AI production asset package: writing, visual identity, storyboard, video-generation prompts, and voice prompts. Default language is Chinese, default format is vertical short drama `9:16`, with commercial Douyin/Hongguo pacing.

Use this skill when the user asks for “AI短剧物料”, “短剧全套生成”, “EP01物料”, “人物/分镜/即梦/声音prompt”, “故事板”, “首帧”, “九宫格分镜板”, “图生视频”, “角色设定板”, or wants a reusable production folder.

## Core Principle

Keep all outputs stable and reusable. Every character, scene, and story block needs a fixed ID and a copy-paste-ready prompt. Do not generate isolated pretty assets that cannot be reused in later shots.

## Workflow

1. **Create or inspect the project**
   - If starting from scratch, create a project folder such as `剧名_YYYYMMDD_HHMMSS/EP01`.
   - Use the folder structure in `references/file-structure.md`.
   - If the user already has an EP folder, inspect existing `characters`, `storyboards`, `voices`, `scenes`, and prompt files before adding anything.

2. **Build the episode spine**
   - Write or extract: title, genre, core hook, protagonist pressure, antagonist/pressure source, final reversal.
   - Split the episode into stable blocks: `B01`, `B02`, etc.
   - For 2-minute episodes, 12-18 blocks works well; for 5-minute episodes, 20-35 blocks.
   - Each block must have: time target, action, dialogue/sound, emotional purpose, visual hook, ending hook.

3. **Build the character package**
   - Assign IDs: `C01`, `C02`, etc. Never renumber approved/generated characters; add new missing characters with the next ID.
   - Create:
     - `characters/EP01_角色卡.md`
     - `characters/EP01_角色提示词锁定速查.md`
     - `characters/CXX_角色名_角色卡.md` for important late-added characters
     - `characters/CXX_角色名_角色设定板_prompt.md`
   - For each important character, generate or request:
     - base character image: `CXX_角色名.png`
     - cinematic concept board: `CXX_角色名_电影级角色设定板_FINAL.png`
   - For concept board format, read `references/prompt-templates.md`.

4. **Create scene and continuity locks**
   - Create `scenes/EP01_场景设定.md` when locations matter.
   - Lock cabin/cockpit/airport lighting, props, seat numbers, uniforms, badges, phones, drawings, and evidence objects.
   - Separate “what must remain readable” from “what should not become model-generated fake text”.

5. **Write detailed storyboard markdown**
   - Create one file per block: `storyboards/md/B01_故事板.md`.
   - This is not an image prompt unless the user asks. A pure story board should include: duration, scene, characters, dramatic function, ending hook, shot beats, performance notes, sound design, edit point.
   - See `references/prompt-templates.md` for the exact block template.

6. **Generate image/video prompt package**
   - For each block, create first-frame prompts and optional 3x3 storyboard prompts only when requested.
   - First frame: one strong frame for image-to-video.
   - 3x3 storyboard: one image containing nine sequential shot panels, no dense text.
   - Jimeng/Seedance prompt: movement, timing, camera, acting, sound if supported, and hard continuity locks.
   - Avoid mixing too much action into one video-generation unit; keep one clear subject/action per clip.

7. **Create voice package**
   - Create `voices/EP01_人物声音生成prompt.md`.
   - For each character: identity, vocal age, timbre, speed, emotional range, performance direction, sample audition lines.
   - Use original voices. Do not imitate real actors, celebrities, influencers, or private persons without explicit authorization.
   - Store selected audio samples or generated voice references in `voices/`, and record voice IDs if the platform provides them.

8. **Create asset index and missing-material report**
   - Maintain a short index listing what exists and what is missing.
   - Typical missing items after character work: scene bible, all B-block first frames, all 3x3 boards, all image-to-video prompts, selected voice IDs, final audio lines.
   - Be concrete: name exact filenames, not vague categories.

9. **Validate**
   - Run through `references/qa-checklist.md`.
   - Confirm continuity: faces, wardrobe, props, seat numbers, evidence objects, block IDs, and voice IDs.
   - If images are generated with built-in imagegen, copy final assets from Codex generated images into the project folder. Never leave project assets only under `$CODEX_HOME/generated_images`.

## When User Asks For Only One Artifact

Produce exactly that artifact, but keep IDs compatible with the whole package. Examples:

- “只要故事板” means do not include first-frame/image/video prompt sections.
- “先来 B01” means produce B01 with the same format planned for all blocks.
- “先生成第一个角色设定板” means generate one character preview, save prompt and image non-destructively.
- “保存成 md” means write the markdown file into the appropriate project folder.

## Image Generation Rules

Use the built-in image generation path for actual raster assets unless the user requests another platform. Save project-bound final images into the workspace.

For character boards:
- Chinese labels for Chinese projects.
- Landscape large-format board.
- Include main standing figure, full-body turnaround, head studies, cinematic emotional portrait, costume/accessory breakdowns, sparse professional annotations.
- Preserve approved character identity. Iterate from feedback without renaming/replacing accepted files; save versions and copy the approved one to `_FINAL.png`.

For storyboards:
- Avoid unreadable dense text in generated images.
- Use role-image references and repeat continuity anchors.
- First frames should be vertical `9:16`; 3x3 storyboard sheets can be landscape.

## References

- `references/file-structure.md`: folder and filename convention.
- `references/prompt-templates.md`: copyable templates for character cards, storyboards, first frames, 3x3 boards, Jimeng/Seedance, and voices.
- `references/qa-checklist.md`: final validation checklist.
