---
name: muji-ppt
description: >
  Generate Muji-style PPT web pages (HTML) based on user-provided content.
  Use when the user wants to create a presentation, slideshow, or PPT in HTML format
  with a clean, minimalist Muji-inspired design. Trigger keywords include
  "生成PPT", "制作PPT", "make a presentation", "create a slides", "生成幻灯片",
  "Muji风格PPT", "网页PPT", etc.
agent_created: true
---

# muji-ppt Skill

Generate clean, minimalist Muji-style HTML presentations. The output is a single self-contained HTML file with embedded CSS and JS, ready to open in any browser.

## Design Language

- **Palette**: Warm off-white (`#F5F4F0`), dark ink (`#1A1A1A`), muted gray (`#6B6B6B`), faint rule lines (`#D8D5CE`)
- **Typography**: Noto Sans SC / PingFang SC, font-weight 300 (light) for body, 700 (bold) for emphasis
- **Layout**: A4-like slide ratio, generous whitespace, left-aligned content, subtle dividers
- **Vibe**: Quiet, premium, editorial — like a Muji store flyer

## Slide Types

Support these slide layouts (use the most appropriate one for each slide):

### 1. Cover Slide
- Eyebrow (small uppercase label, optional)
- Large title (light weight, 60-80px)
- Bold subtitle on separate lines
- Optional right-side decorative block (gradient panel with concentric circles)

### 2. Section Title Slide
- Small uppercase section tag with left rule line
- Large title (light weight)
- Optional subtitle/tagline

### 3. Two-Column Content
- Left: heading + body text
- Right: heading + body text
- Separated by a subtle vertical rule

### 4. Three-Column Grid
- Three side-by-side columns with top icons/labels
- Each column: icon, title, description
- No borders between columns (use whitespace)

### 5. Value/Feature Grid (2x2)
- Four cards in a 2x2 grid
- Each card: number, title, description
- Bordered cards with hover effect

### 6. Step Flow (Horizontal)
- 3-4 steps in a horizontal row
- Each step: step number, title, bullet list
- Arrow (`→`) between steps

### 7. Case Study / Comparison Row
- 3 side-by-side panels (light background)
- Each panel: label (uppercase small), content
- Separated by 1px rule

### 8. Summary / List Slide
- Numbered list (01, 02, 03...)
- Each item: number (faint), bold title, description
- Optional bottom closing statement with top border

## HTML Template Structure

Generate a complete self-contained HTML file. Use this structure:

```
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>[User's Title]</title>
  <style>
    /* ── CSS Variables ── */
    :root {
      --bg: #F5F4F0;
      --ink: #1A1A1A;
      --ink-light: #6B6B6B;
      --ink-faint: #B8B4AC;
      --rule: #D8D5CE;
      --white: #FAFAF8;
    }

    * { box-sizing: border-box; margin: 0; padding: 0; }

    body {
      font-family: 'Noto Sans SC', 'PingFang SC', 'Hiragino Sans GB', sans-serif;
      background: #1C1C1C;
      display: flex; flex-direction: column;
      align-items: center; justify-content: center;
      min-height: 100vh; padding: 20px 0;
    }

    .deck { width: 1035px; }
    .slide {
      width: 1035px; height: 582px;
      background: var(--bg);
      position: relative; overflow: hidden;
      display: none; flex-direction: column;
      padding: 60px 90px;
    }
    .slide.active { display: flex; }

    .slide-num {
      position: absolute; bottom: 32px; right: 46px;
      font-size: 13px; letter-spacing: 0.15em;
      color: var(--ink-faint); font-weight: 300;
    }

    /* Navigation */
    .nav { display: flex; align-items: center; justify-content: center;
           gap: 23px; margin-top: 21px; }
    .nav button {
      background: none; border: 1px solid #555;
      color: #aaa; padding: 9px 32px; font-size: 15px;
      letter-spacing: 0.1em; cursor: pointer; transition: all 0.2s;
      font-family: inherit;
    }
    .nav button:hover { border-color: #aaa; color: #eee; }
    .nav button:disabled { opacity: 0.25; cursor: default; }
    .nav .counter {
      font-size: 14px; color: #666;
      letter-spacing: 0.12em; min-width: 69px; text-align: center;
    }

    /* Section tag */
    .section-tag {
      font-size: 12px; letter-spacing: 0.3em;
      text-transform: uppercase; color: var(--ink-faint);
      margin-bottom: 16px; display: flex; align-items: center; gap: 12px;
    }
    .section-tag::before {
      content: ''; display: inline-block;
      width: 28px; height: 1px; background: var(--ink-faint);
    }

    /* Typography */
    h1, h2, h3 { font-weight: 300; color: var(--ink); line-height: 1.2; }
    strong { font-weight: 700; }

    /* Keyboard hint */
    .key-hint {
      font-size: 13px; color: #444;
      text-align: center; margin-top: 12px; letter-spacing: 0.1em;
    }
  </style>
</head>
<body>
  <div class="deck" id="deck">
    <!-- Slides go here -->
  </div>
  <div class="nav">
    <button id="prev" disabled>← 上一页</button>
    <div class="counter" id="counter">1 / N</div>
    <button id="next">下一页 →</button>
  </div>
  <div class="key-hint">← → 方向键翻页</div>

  <script>
    const slides = document.querySelectorAll('.slide');
    let cur = 0;
    function goto(n) {
      slides[cur].classList.remove('active');
      cur = n;
      slides[cur].classList.add('active');
      document.getElementById('counter').textContent = (cur+1) + ' / ' + slides.length;
      document.getElementById('prev').disabled = cur === 0;
      document.getElementById('next').disabled = cur === slides.length - 1;
    }
    document.getElementById('prev').onclick = () => { if(cur>0) goto(cur-1); };
    document.getElementById('next').onclick = () => { if(cur<slides.length-1) goto(cur+1); };
    document.addEventListener('keydown', e => {
      if(e.key==='ArrowRight'||e.key==='ArrowDown') { if(cur<slides.length-1) goto(cur+1); }
      if(e.key==='ArrowLeft'||e.key==='ArrowUp')   { if(cur>0) goto(cur-1); }
    });
  </script>
</body>
</html>
```

## Workflow

1. **Collect content from user**: Ask for (or extract from conversation):
   - Presentation title
   - Number of slides and topic of each
   - Any specific content, data, or key points

2. **Plan slide layout**: For each slide, pick the most appropriate layout type from the Slide Types above.

3. **Generate the HTML**: Write a single self-contained HTML file with:
   - All slides in the `<body>` inside `.deck`
   - Each slide as a `<div class="slide sN">` (with appropriate class for styling)
   - Correct slide numbering (`01 / 07` format)
   - All CSS embedded in `<style>` tag
   - Navigation JS included

4. **Save to file**: Write the generated HTML to a `.html` file in the user's workspace.

## Important Rules

- **One slide per viewport**: Each `.slide` is exactly 1035×582px, `overflow: hidden`
- **No external dependencies**: Do NOT use Google Fonts CDN or any external links. Use system font stack: `'Noto Sans SC', 'PingFang SC', 'Hiragino Sans GB', sans-serif`
- **Consistent numbering**: Use `01 / 07` format for slide numbers
- **First slide is active**: The first `.slide` must have class `active`
- **Navigation always works**: Include the standard nav JS exactly as shown above
- **Language**: All user-facing text in the PPT should match the user's language (Chinese unless specified otherwise)

## Quick Reference: CSS Classes for Slide Layouts

| Layout | Suggested class | Key CSS |
|--------|----------------|---------|
| Cover | `.s1` | Centered or left-aligned title, large type, optional right deco panel |
| Section title | `.s2` | section-tag + h2, generous padding |
| 3-column | `.metaphor-row` | Flex row, 3 × `.metaphor-item` |
| 2x2 grid | `.value-grid` | CSS grid, 2 columns |
| Step flow | `.steps-flow` | Flex row, arrows between steps |
| Case/compare | `.case-row` | Flex row, equal-width panels |
| Summary list | `.summary-list` | Vertical numbered list |

Refer to the template file at `assets/skill-share-ppt.html` for exact CSS implementation details of each layout.
