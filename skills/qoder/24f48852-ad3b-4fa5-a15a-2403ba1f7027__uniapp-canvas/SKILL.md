---
name: uniapp-canvas-gauge
description: >-
  Guide for drawing complex visual patterns using native Canvas 2D API in
  uni-app and mini-program mobile environments (Feishu/WeChat/Alipay).
  Covers the general methodology for Canvas drawing in mini-programs —
  coordinate system, drawing primitives, state management, animation loops,
  CSS text overlay, responsive sizing, and common pitfalls. Uses a 3/4 circle
  gauge chart with multi-level ticks and progress animation as the primary
  worked example. Applicable to gauges, dials, meters, radial progress,
  custom charts, decorative graphics, and any complex Canvas-drawn UI in
  mini-programs. Use when the user asks to draw anything with Canvas in a
  mini-program, when ECharts is unavailable or too heavy, or when precise
  visual control over shapes, ticks, and labels is needed.
version: 1.1.0
---

# uni-app Canvas Complex Drawing

Draw complex visual patterns using native `uni.createCanvasContext` in uni-app mini-programs — no ECharts dependency required. This skill covers the **general methodology** for Canvas drawing, using a 3/4 circle gauge chart as the primary worked example.

## When to Use This Skill

- The user asks to draw **anything** with Canvas in a mini-program (gauge, dial, meter, radial progress, custom chart, decorative graphic, etc.)
- ECharts is unavailable, too heavy, or causes circular reference errors
- Precise control over **shapes, lines, arcs, ticks, labels, and animation** is needed
- The target is **uni-app / Feishu mini-program / WeChat mini-program / Alipay mini-program**
- The user says "use Canvas to draw" or "don't use ECharts"

## When NOT to Use

- The chart is a simple line/bar/pie chart and ECharts is available → use the `feishu-echarts` skill instead
- The target is a web browser (not a mini-program) → use standard HTML5 Canvas or ECharts
- The user explicitly requests ECharts

## 1. General Methodology: Canvas Drawing in Mini-Programs

This section covers the **universal approach** for drawing any complex pattern with Canvas in uni-app/mini-programs. The gauge chart in later sections is a concrete application of these principles.

### 1.1 Canvas Context Creation

In uni-app, always use `uni.createCanvasContext` (not `document.getElementById`):

```js
const ctx = uni.createCanvasContext('canvasId', this);
// ... draw operations ...
ctx.draw(); // CRITICAL: must call to render
```

> **Key difference from browser**: Browser Canvas renders immediately; uni-app Canvas queues all commands and renders only when `ctx.draw()` is called. Forgetting `ctx.draw()` is the #1 cause of "nothing shows up".

### 1.2 Coordinate System

```
Origin (0,0) is top-left
  → X increases rightward
  → Y increases downward
  → Angles: 0 = right (3 o'clock), PI/2 = down (6 o'clock),
            PI = left (9 o'clock), 3*PI/2 = up (12 o'clock)
```

For radial/arc-based patterns, always compute the center first:
```js
const cx = canvasWidth / 2;
const cy = canvasHeight / 2; // or offset as needed
```

### 1.3 Drawing Primitives

| Primitive | Method | Use Case |
|-----------|--------|----------|
| **Arc** | `ctx.arc(cx, cy, r, startAngle, endAngle, anticlockwise)` | Circles, arcs, pie slices |
| **Line** | `ctx.moveTo(x1,y1); ctx.lineTo(x2,y2); ctx.stroke()` | Ticks, dividers, connectors |
| **Filled path** | `ctx.beginPath(); ...path...; ctx.fill()` | Shapes, backgrounds |
| **Text** | `ctx.fillText(text, x, y)` | Labels (but prefer CSS overlay, see 1.7) |
| **Rect** | `ctx.fillRect(x, y, w, h)` / `ctx.strokeRect(x, y, w, h)` | Bars, boxes |
| **Bezier** | `ctx.bezierCurveTo(cp1x, cp1y, cp2x, cp2y, x, y)` | Smooth curves |
| **Quadratic** | `ctx.quadraticCurveTo(cpx, cpy, x, y)` | Simple curves |

### 1.4 State Management — Set Before Each Layer

Canvas state persists between draw calls. Always re-set state before each layer:

```js
// Layer 1: background
ctx.setLineWidth(14);
ctx.setStrokeStyle('#F0F0F0');
ctx.setLineCap('butt');
ctx.beginPath();
ctx.arc(...); ctx.stroke();

// Layer 2: progress — MUST re-set width/style!
ctx.setLineWidth(14);        // re-set! (state persists)
ctx.setStrokeStyle('#2BA471'); // re-set!
ctx.setLineCap('butt');     // re-set!
ctx.beginPath();
ctx.arc(...); ctx.stroke();
```

> **Pitfall**: If you skip re-setting state between layers, the second layer may inherit unexpected style from the first.

### 1.5 Trigonometric Positioning

For radial patterns (gauges, clocks, dials, radial charts), use trig to position elements:

```js
// Convert value (0-100) to angle
const angleFor = (value) => startAngle + (value / maxValue) * totalSweep;

// Position a point on the arc at a given angle
const x = cx + radius * Math.cos(angle);
const y = cy + radius * Math.sin(angle);

// Draw a radial line (e.g., tick mark) from outer to inner
const outerR = radius;
const innerR = radius - tickLength;
ctx.moveTo(cx + outerR * Math.cos(a), cy + outerR * Math.sin(a));
ctx.lineTo(cx + innerR * Math.cos(a), cy + innerR * Math.sin(a));
```

This pattern works for: tick marks, labels, radial dividers, pie chart slices, gauge needles, etc.

### 1.6 Animation — setTimeout Loop (No requestAnimationFrame)

Mini-programs do NOT support `requestAnimationFrame`. Use `setTimeout` for animation:

```js
data() {
  return { animProgress: 0, animTimer: null };
},

mounted() {
  this.$nextTick(() => {
    setTimeout(() => this.startAnim(), 200); // wait for canvas ready
  });
},

beforeDestroy() {
  if (this.animTimer) clearTimeout(this.animTimer); // cleanup!
},

methods: {
  startAnim() {
    if (this.animTimer) clearTimeout(this.animTimer);
    this.animProgress = 0;
    this.animateFrame();
  },

  animateFrame() {
    const target = 75; // target value
    const step = Math.max(1, target / 40); // ~40 frames
    this.animProgress = Math.min(this.animProgress + step, target);
    this.draw(); // re-draw with new progress
    if (this.animProgress < target) {
      this.animTimer = setTimeout(() => this.animateFrame(), 16); // ~60fps
    }
  },
}
```

> **Pattern**: Increment → Draw → Schedule next frame. Always clean up timer in `beforeDestroy`.

### 1.7 CSS Overlay for Text — Not Canvas Text

Canvas `fillText` is unreliable across mini-program platforms (font fallback, baseline, kerning issues). For any text that needs precise styling, use a CSS overlay:

```html
<view class="canvas-box" style="position: relative;">
  <canvas canvas-id="myCanvas" :style="{ width: w+'px', height: h+'px' }"></canvas>
  <!-- CSS overlay positioned over the canvas -->
  <view class="overlay" :style="{ top: centerY+'px', left: 0, right: 0 }">
    <text class="big-number">{{ value }}</text>
    <text class="small-label">{{ label }}</text>
  </view>
</view>
```

```css
.overlay {
  position: absolute;
  display: flex;
  flex-direction: column;
  align-items: center;
  transform: translateY(-50%); /* center on target Y */
  pointer-events: none;
}
```

> **When to use Canvas text vs CSS text**: Use Canvas text ONLY for short labels tightly coupled to geometry (e.g., tick labels on an arc). Use CSS text for anything with complex styling (fonts, colors, transitions, animations).

### 1.8 Responsive Canvas Sizing

Canvas dimensions must be computed from `uni.getSystemInfoSync()`, not CSS:

```js
created() {
  try {
    const sys = uni.getSystemInfoSync();
    const w = Math.min(sys.windowWidth * 0.8, 300);
    this.canvasW = Math.round(w);
    this.canvasH = Math.round(w * 0.6); // aspect ratio
    // Pre-compute any derived values (center, radius, etc.)
    this.centerX = Math.round(this.canvasW / 2);
    this.centerY = Math.round(this.canvasH / 2);
  } catch (e) {}
}
```

> **Why `created()` not `mounted()`**: `created()` runs before the template renders. Setting canvas size here ensures the `<canvas>` element has correct dimensions when `mounted()` fires.

### 1.9 Universal Pitfalls

| Pitfall | Symptom | Fix |
|---------|---------|-----|
| Missing `ctx.draw()` | Nothing renders | Always call `ctx.draw()` at the end |
| Using `window.innerWidth` | Crash in mini-program | Use `uni.getSystemInfoSync().windowWidth` |
| Using `requestAnimationFrame` | Not defined error | Use `setTimeout(fn, 16)` instead |
| State not re-set between layers | Wrong colors/widths | Call `setLineWidth`/`setStrokeStyle` before each layer |
| Canvas text rendering issues | Garbled/offset text | Use CSS overlay for styled text |
| Timer not cleaned up | Memory leak / errors after unmount | `clearTimeout` in `beforeDestroy` |
| Canvas not ready on mount | First draw fails | Use `setTimeout(200ms)` after `$nextTick` |
| `lineCap: 'round'` at arc gap | Arc overshoots gap | Use `'butt'` for gaps, `'round'` only for progress tips |

## 1.10 Other Common Canvas Patterns

The methodology in §1 applies to many complex patterns beyond gauges. Here are brief recipes for common scenarios:

### Radial Progress Ring

A simpler version of the gauge — full circle, no ticks, just a progress arc:
```js
// Full circle: startAngle=0, endAngle=2π
// Draw background ring (full circle, gray)
ctx.arc(cx, cy, r, 0, 2 * Math.PI, false);
// Draw progress ring (partial arc)
ctx.arc(cx, cy, r, -Math.PI / 2, -Math.PI / 2 + (value / 100) * 2 * Math.PI, false);
// CSS overlay for center text (percentage)
```

### Custom Bar Chart (Horizontal)

When ECharts is unavailable, draw bars manually:
```js
const barH = 20; const gap = 8; const maxW = canvasW - labelW;
data.forEach((item, i) => {
  const y = i * (barH + gap);
  // Background bar
  ctx.setFillStyle('#F0F0F0');
  ctx.fillRect(labelW, y, maxW, barH);
  // Progress bar
  ctx.setFillStyle(item.color);
  ctx.fillRect(labelW, y, maxW * (item.value / maxValue), barH);
});
// Labels: use CSS overlay or ctx.fillText for short labels
```

### Radar/Spider Chart

Multi-axis radial chart using trig positioning (§1.5):
```js
const axes = 6; const angleStep = (2 * Math.PI) / axes;
// Draw axis lines from center to each vertex
for (let i = 0; i < axes; i++) {
  const a = i * angleStep - Math.PI / 2;
  ctx.moveTo(cx, cy);
  ctx.lineTo(cx + r * Math.cos(a), cy + r * Math.sin(a));
}
// Draw data polygon
ctx.beginPath();
data.forEach((v, i) => {
  const a = i * angleStep - Math.PI / 2;
  const dist = (v / maxValue) * r;
  const x = cx + dist * Math.cos(a);
  const y = cy + dist * Math.sin(a);
  i === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
});
ctx.closePath(); ctx.fill();
```

### Clock / Dial Face

Same trig positioning as gauge ticks, but full 360°:
```js
for (let i = 0; i < 60; i++) {
  const a = (i / 60) * 2 * Math.PI - Math.PI / 2;
  const isHour = i % 5 === 0;
  const len = isHour ? 10 : 5;
  const outerR = r;
  const innerR = r - len;
  // moveTo/lineTo using cos/sin (§1.5 pattern)
}
// Hour labels: ctx.fillText at innerR - 15
```

### Decorative Wave / Sine Pattern

Using bezier/quadratic curves for smooth decorative elements:
```js
ctx.beginPath();
const amplitude = 20; const wavelength = 80;
for (let x = 0; x <= canvasW; x += 2) {
  const y = cy + amplitude * Math.sin((x / wavelength) * 2 * Math.PI);
  x === 0 ? ctx.moveTo(x, y) : ctx.lineTo(x, y);
}
ctx.stroke();
// For smoother curves: use quadraticCurveTo between wave points
```

### Key Principle for All Patterns

1. **Compute geometry first** — center, radius, angles, positions
2. **Draw bottom-to-top** — background → tracks → data → ticks/labels
3. **Re-set state per layer** — `setLineWidth`, `setStrokeStyle`, `setFillStyle` before each
4. **Use CSS overlay for text** — Canvas text is unreliable
5. **Call `ctx.draw()` at end** — or nothing renders
6. **Animate with `setTimeout`** — never `requestAnimationFrame`

---

## 2. Worked Example: 3/4 Circle Gauge Chart

The following sections apply the methodology above to a specific example: a 3/4 circle gauge with multi-level ticks, progress animation, and CSS text overlay.

```
┌─────────────────────────────────┐
│       gauge-canvas-box          │  position: relative
│  ┌───────────────────────────┐  │
│  │     <canvas>              │  │  Canvas draws: arc + ticks + labels
│  │                           │  │
│  ├───────────────────────────┤  │
│  │  gauge-center-text (CSS)  │  │  Absolute overlay: % + description
│  └───────────────────────────┘  │
└─────────────────────────────────┘
```

**Canvas** draws the geometric elements (arc, ticks, labels). **CSS overlay** draws the center text (percentage, description). This separation avoids Canvas text rendering inconsistencies across mini-program platforms.

## 3. Core Architecture (Gauge Example)

Canvas dimensions must be computed in `created()` from `uni.getSystemInfoSync()`:

```js
created() {
  try {
    const sys = uni.getSystemInfoSync();
    const w = Math.min(sys.windowWidth * 0.74, 270);
    this.canvasW = Math.round(w);
    this.canvasH = Math.round(w * 0.88); // ~square for 3/4 circle
    const r = Math.min(w / 2 - 30, this.canvasH * 0.5);
    this.gaugeCenterY = Math.round(r + 50); // for CSS text overlay
  } catch (e) {}
}
```

> **Critical**: Do NOT use `window.innerWidth` — it may be undefined in mini-program environments. Always use `uni.getSystemInfoSync().windowWidth`.

## 4. Angle System — 3/4 Circle (270°)

The gauge is a 3/4 circle with a 90° gap at the bottom:

```
        0% ─────────── 100%
       ╱                     ╲
      /        TOP ARC         \
     │                           │
    0%                         100%
      ╲                       ╱
       └──── BOTTOM GAP ────┘
```

```js
// Canvas coordinate: 0=right, PI/2=down, PI=left, 3*PI/2=up
const startAngle = 3 * Math.PI / 4;           // Left-bottom (7:30 position)
const endAngle = Math.PI / 4 + 2 * Math.PI;  // Right-bottom (4:30 position)
const totalSweep = 3 * Math.PI / 2;           // 270°
const angleFor = (v) => startAngle + (v / 100) * totalSweep;
```

> **Why `+2π`**: Canvas `arc()` draws counter-clockwise by default when `anticlockwise=false`. Adding `2π` to the end angle ensures the arc sweeps clockwise through the top.

## 5. Drawing Layers

Draw in this order (bottom to top):

### Layer 1: Background Arc (Track)
```js
ctx.setLineWidth(arcW);
ctx.setStrokeStyle('#F0F0F0');
ctx.setLineCap('butt');          // Square ends at the gap
ctx.beginPath();
ctx.arc(cx, cy, r, startAngle, endAngle, false);
ctx.stroke();
```

### Layer 2: Progress Arc (Value)
```js
if (value > 0) {
  ctx.setLineWidth(arcW);
  ctx.setStrokeStyle(color);     // #2BA471 or #D54941
  ctx.setLineCap('butt');
  ctx.beginPath();
  ctx.arc(cx, cy, r, startAngle, angleFor(value), false);
  ctx.stroke();
}
```

### Layer 3: Tick Marks (Inside the Arc)

Three levels of ticks, all pointing inward from the arc's inner edge:

```js
const tickStart = r - arcW / 2 - 3;  // 3px gap from arc inner edge

// Micro ticks: every 5 units, shortest, lightest
ctx.setLineWidth(0.8);
ctx.setStrokeStyle('#C8C8C8');
microTicks.forEach((v) => { /* draw line from tickStart to tickStart-3 */ });

// Minor ticks: every 10 units, medium
ctx.setLineWidth(1);
ctx.setStrokeStyle('#B0B0B0');
minorTicks.forEach((v) => { /* draw line from tickStart to tickStart-4 */ });

// Major ticks: every 20 units, longest, darkest
ctx.setLineWidth(1.5);
ctx.setStrokeStyle('#C0C0C0');
majorTicks.forEach((v) => { /* draw line from tickStart to tickStart-7 */ });
```

Tick values:
- `majorTicks = [0, 20, 40, 60, 80, 100]` — labeled
- `minorTicks = [10, 30, 50, 70, 90]` — unlabeled
- `microTicks = [5, 15, 25, 35, 45, 55, 65, 75, 85, 95]` — unlabeled

### Layer 4: Tick Labels (Inside, Deeper)
```js
ctx.setFillStyle('#AAAAAA');
ctx.setFontSize(10);
ctx.setTextAlign('center');
ctx.setTextBaseline('middle');
const labelR = tickStart - 14;   // Deeper than tick ends
majorTicks.forEach((v) => {
  const a = angleFor(v);
  const x = cx + labelR * Math.cos(a);
  const y = cy + labelR * Math.sin(a);
  ctx.fillText(String(v), x, y);
});
```

### Final: Flush to Canvas
```js
ctx.draw();  // Required in uni-app — renders all queued drawing commands
```

## 6. Progress Fill Animation

Animate the arc from 0 to the target value:

```js
data() {
  return {
    animProgress: 0,
    animTimer: null,
  };
},

mounted() {
  this.$nextTick(() => {
    setTimeout(() => this.startGaugeAnim(), 200);  // Wait for canvas ready
  });
},

beforeDestroy() {
  if (this.animTimer) clearTimeout(this.animTimer);
},

methods: {
  startGaugeAnim() {
    if (this.animTimer) clearTimeout(this.animTimer);
    this.animProgress = 0;
    this.animateGauge();
  },

  animateGauge() {
    const target = this.gaugePerValid ? Math.min(this.gaugePerNum, 100) : 0;
    const step = Math.max(1, target / 40);    // ~40 frames
    this.animProgress = Math.min(this.animProgress + step, target);
    this.drawGauge();
    if (this.animProgress < target) {
      this.animTimer = setTimeout(() => this.animateGauge(), 16); // ~60fps
    }
  },
},
```

> **Why not `requestAnimationFrame`**: Mini-program Canvas does not support `requestAnimationFrame`. Use `setTimeout(fn, 16)` to approximate 60fps.

## 7. CSS Text Overlay

Center text is rendered as a CSS overlay, NOT on the Canvas:

```html
<view class="gauge-canvas-box">
  <canvas canvas-id="gaugeCanvas" id="gaugeCanvas"
    :style="{ width: canvasW + 'px', height: canvasH + 'px' }"
  ></canvas>
  <view class="gauge-center-text" :style="{ top: gaugeCenterY + 'px' }">
    <view class="gauge-percent-wrap">
      <text class="gauge-percent" :style="{ color: gaugeTextColor }">{{ gaugePercentNum }}</text>
      <text v-if="showPercentSign" class="gauge-percent-sign" :style="{ color: gaugeTextColor }">%</text>
    </view>
    <text class="gauge-desc">{{ descText }}</text>
  </view>
</view>
```

```css
.gauge-center-text {
  position: absolute;
  left: 0;
  right: 0;
  display: flex;
  flex-direction: column;
  align-items: center;
  justify-content: center;
  transform: translateY(-50%);   /* Center on the gauge's circle center */
  pointer-events: none;
}
.gauge-percent {
  font-weight: 700;
  font-size: 36px;
  line-height: 1.1;
}
.gauge-percent-sign {
  font-weight: 700;
  font-size: 14px;    /* ~40% of the main number height */
  margin-left: 2px;
}
```

> **Why CSS overlay**: Canvas `fillText` rendering varies across mini-program platforms (font fallback, baseline, kerning). CSS `<text>` is consistent and supports transitions/animations.

## 8. Value & Color States

```js
computed: {
  gaugeTextColor() {
    if (!this.gaugePerValid || this.gaugePerNum === 0) return "#999";  // gray for invalid/zero
    const behind = this.gaugePerNum < this.threshold;
    return behind ? "#D54941" : "#2BA471";  // red if behind, green if ahead
  },
  gaugePercentNum() {
    if (!this.gaugePerValid || this.gaugePerNum === 0) return "—";  // em dash
    return this.gaugePerNum.toFixed(2);  // two decimal places
  },
}
```

| State | Value | Color | `%` sign |
|-------|-------|-------|----------|
| Valid & ahead | `42.50` | `#2BA471` (green) | Shown |
| Valid & behind | `18.30` | `#D54941` (red) | Shown |
| Zero / null | `—` | `#999` (gray) | Hidden |

## 9. Data Normalization

Always normalize input before using — values from APIs may be strings, null, `"-"`, or contain `%`:

```js
function normalizeGaugePercent(targetComplete) {
  const tcRaw = targetComplete != null
    ? String(targetComplete).replace(/%/g, "").trim()
    : "";
  const parsed = parseFloat(tcRaw);
  const invalid = tcRaw === "" || tcRaw === "-" || /^null$/i.test(tcRaw) || !Number.isFinite(parsed);
  return { valid: !invalid, value: invalid ? 0 : parsed, raw: tcRaw };
}
```

## 10. Full Template

See [references/template.md](references/template.md) for the complete Vue component code.

## 11. Example Data

See [references/example.json](references/example.json) for sample input data.

## 12. Pitfalls (Gauge-Specific)

These are pitfalls specific to the gauge implementation, in addition to the universal pitfalls in §1.9.

- **`window.innerWidth` is undefined** in mini-programs → use `uni.getSystemInfoSync().windowWidth`
- **`requestAnimationFrame` is unavailable** → use `setTimeout(fn, 16)` for ~60fps
- **`ctx.draw()` is required** — without it, nothing renders (uni-app Canvas quirk)
- **Canvas text is unreliable** across platforms → use CSS overlay for text
- **`lineCap: 'round'`** causes arc ends to overshoot the gap → use `'butt'` for 3/4 circle
- **`+2π` on end angle** is needed for clockwise sweep through the top
- **Setting `setLineWidth` / `setStrokeStyle` per layer** — Canvas state persists between strokes, so re-set before each layer

## 13. Customization Guide

| Parameter | Default | What it controls |
|-----------|---------|------------------|
| `arcW` | `11` | Thickness of the arc |
| `startAngle` | `3π/4` | Start position (change for full circle, half circle, etc.) |
| `totalSweep` | `3π/2` | Arc span (270° = 3/4 circle, π = half circle, 2π = full circle) |
| `majorTicks` | `[0,20,40,60,80,100]` | Labeled tick positions |
| `minorTicks` | `[10,30,50,70,90]` | Unlabeled tick positions |
| `microTicks` | `[5,15,...,95]` | Micro tick positions |
| `tickStart gap` | `3px` | Distance between arc inner edge and tick start |
| `labelR offset` | `14px` | Distance from tick start to label center |
| Animation frames | `40` | Number of animation frames (~640ms at 60fps) |
| `gaugePercent font-size` | `36px` | Main number size |
| `gauge-percent-sign font-size` | `14px` | % sign size (~40% of main) |
