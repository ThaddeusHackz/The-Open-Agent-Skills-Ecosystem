---
name: transcribe-translate
description: Build, install, and run an English audio transcription + translation tool using OpenVINO models (distil-whisper for ASR, HY-MT1.5 for translation). Use when the user wants to set up or use the transcribe-translate tool, download/install models, run speech-to-text transcription, translate audio to another language, or mentions OpenVINO, distil-whisper, HY-MT, modelscope.
---

# English Audio Transcription + Translation Tool

Full lifecycle skill: **write code → install dependencies → download models → auto-test → run inference**.
Cross-platform: macOS / Windows / Linux.

## Architecture

```
Audio (WAV/MP3/FLAC/M4A)
  → distil-whisper-large-v3-int8-ov (OpenVINO INT8 ASR)
  → English text
  → HY-MT1.5-1.8B-int4-ov (OpenVINO INT4 MT)
  → Translated text (33 languages, default: Chinese)
```

**Model sources (ModelScope):**
- https://modelscope.cn/models/snake7gun/distil-whisper-large-v3-int8-ov
- https://modelscope.cn/models/snake7gun/HY-MT1.5-1.8B-int4-ov

**Test audio:** `https://modelscope.cn/api/v1/models/snake7gun/distil-whisper-large-v3-int8-ov/repo?Revision=master&FilePath=test_audio.wav`

---

## Phase 1: Create Project

Create the project directory `<PROJECT_DIR>` (user-specified, or default `./transcribe-translate`).

### 1.1 Create `transcribe_translate.py`

Write the main tool script with the following structure:

```python
# Key imports
from optimum.intel.openvino import OVModelForSpeechSeq2Seq
from optimum.intel import OVModelForCausalLM
from transformers import AutoProcessor, AutoTokenizer
from modelscope import snapshot_download

# Default model dirs: <SCRIPT_DIR>/models/distil-whisper-large-v3-int8-ov
#                     <SCRIPT_DIR>/models/HY-MT1.5-1.8B-int4-ov
```

Critical implementation details:
- **Model download**: Use `from modelscope import snapshot_download` — do NOT use CLI (`modelscope download`), it does not expose `__main__`.
- **Tokenizer patch**: HY-MT1.5 declares `"tokenizer_class": "TokenizersBackend"` in `tokenizer_config.json`, but this class does not exist in transformers. Auto-patch it to `"PreTrainedTokenizerFast"` before loading.
- **Translation prompt templates** (from HY-MT official docs):
  - ZH target: `将以下文本翻译成中文，注意只需要输出翻译后的结果，不要额外解释：\n\n{source_text}`
  - Other target: `Translate the following segment into {target_language}, without additional explanation.\n\n{source_text}`
- **Translation output extraction**: Model output is wrapped between markers `<｜hy_place▁holder▁no▁8｜>` and `<｜hy_place▁holder▁no▁2｜>`. Extract text between them; fallback: split by `<|im_sep|>` or `assistant\n?`.
- **Inference params**: `top_k=20, top_p=0.6, repetition_penalty=1.05, temperature=0.7`
- **CLI args**: `--audio`, `--target-lang`, `--no-translate`, `--device`, `--download`, `--ui`, `--output`

### 1.2 Create `requirements.txt`

```
openvino>=2025.3.0
optimum-intel>=1.26.1,<1.27
transformers>=4.57.0
tokenizers>=0.22.0
numpy>=1.24.0
librosa>=0.10.0
soundfile>=0.12.0
modelscope
torch
```

---

## Phase 2: Platform-Adaptive Installation

Detect the current OS and adapt accordingly.

### 2.1 Detect platform

```bash
# macOS
[[ "$(uname)" == "Darwin" ]] && PLATFORM="macos"
# Linux
[[ "$(uname)" == "Linux" ]] && PLATFORM="linux"
# Windows (Git Bash / PowerShell)
uname -s | grep -q MINGW && PLATFORM="windows"
[[ "$OS" == "Windows_NT" ]] && PLATFORM="windows"
```

### 2.2 Create venv (platform-specific activate)

| Platform | Create | Activate |
|---|---|---|
| macOS / Linux | `python3 -m venv venv` | `source venv/bin/activate` |
| Windows (cmd) | `python -m venv venv` | `venv\Scripts\activate.bat` |
| Windows (PS) | `python -m venv venv` | `venv\Scripts\Activate.ps1` |

When running commands via terminal tool, always use the venv Python directly:
```bash
# macOS/Linux
<PROJECT_DIR>/venv/bin/python <PROJECT_DIR>/transcribe_translate.py --download

# Windows
<PROJECT_DIR>\venv\Scripts\python.exe <PROJECT_DIR>\transcribe_translate.py --download
```

### 2.3 Install dependencies

```bash
# Use venv pip directly (avoids activate issues)
<PROJECT_DIR>/venv/bin/pip install -r <PROJECT_DIR>/requirements.txt
# For Gradio UI (optional):
<PROJECT_DIR>/venv/bin/pip install gradio
```

### 2.4 Download models

Models are installed to `<PROJECT_DIR>/models/`:

```
<PROJECT_DIR>/models/
├── distil-whisper-large-v3-int8-ov/   (~730MB)
└── HY-MT1.5-1.8B-int4-ov/            (~1.12GB)
```

```bash
<PROJECT_DIR>/venv/bin/python <PROJECT_DIR>/transcribe_translate.py --download
```

This internally calls `modelscope.snapshot_download(model_id, local_dir=...)` for each model.
Skip if the directory already exists and is non-empty.

---

## Phase 3: Auto-Test

After installation, run an automatic test using the built-in test audio file from ModelScope.

### 3.1 Download test audio

```bash
# macOS / Linux
curl -L -o /tmp/test_audio.wav "https://modelscope.cn/api/v1/models/snake7gun/distil-whisper-large-v3-int8-ov/repo?Revision=master&FilePath=test_audio.wav"

# Windows (PowerShell)
Invoke-WebRequest -Uri "https://modelscope.cn/api/v1/models/snake7gun/distil-whisper-large-v3-int8-ov/repo?Revision=master&FilePath=test_audio.wav" -OutFile "$env:TEMP\test_audio.wav"
```

### 3.2 Run pipeline test

```bash
<PROJECT_DIR>/venv/bin/python <PROJECT_DIR>/transcribe_translate.py \
    --audio /tmp/test_audio.wav --target-lang Chinese
```

**Expected output:**
- Transcription: *"Mr. Quilter is the apostle of the middle classes, and we are glad to welcome his gospel."*
- Translation: *"奎特先生是中产阶级的使者，我们很高兴能够迎接他的福音。"*

If the test passes, report success to the user. If it fails, refer to Troubleshooting below.

---

## Phase 4: Daily Usage

### 4.1 CLI

```bash
<PROJECT_DIR>/venv/bin/python <PROJECT_DIR>/transcribe_translate.py \
    --audio <AUDIO_PATH> --target-lang Chinese
```

**Optional flags:**
- `--no-translate` — transcription only
- `--device GPU` / `--device NPU` / `--device AUTO` — change OpenVINO device
- `--output results.txt` — save results to file
- `--target-lang Japanese` / `French` / `Korean` / etc. (33 languages supported)

### 4.2 Gradio Web UI

```bash
<PROJECT_DIR>/venv/bin/pip install gradio
<PROJECT_DIR>/venv/bin/python <PROJECT_DIR>/transcribe_translate.py --ui --port 7860
```

### 4.3 Supported languages

Chinese, French, Portuguese, Spanish, Japanese, Turkish, Russian, Arabic, Korean, Thai, Italian, German, Vietnamese, Malay, Indonesian, Filipino, Hindi, Traditional Chinese, Polish, Czech, Dutch, Khmer, Burmese, Persian, Gujarati, Urdu, Telugu, Marathi, Hebrew, Bengali, Tamil, Ukrainian, Tibetan, Kazakh, Mongolian, Uyghur, Cantonese.

---

## Troubleshooting

| Issue | Fix |
|---|---|
| `No module named modelscope.__main__` | Use `from modelscope import snapshot_download` in Python, NOT `python -m modelscope` |
| `Tokenizer class TokenizersBackend does not exist` | Tool auto-patches this. If persisting: edit `models/HY-MT1.5-1.8B-int4-ov/tokenizer_config.json`, change `"tokenizer_class"` to `"PreTrainedTokenizerFast"` |
| `Optimum-intel requires OpenVINO 2025.4` | Pin `optimum-intel>=1.26.1,<1.27` for OpenVINO 2025.3 compatibility |
| `Models not found` | Run `python transcribe_translate.py --download` |
| Audio format not supported | Convert: `ffmpeg -i input.mp3 output.wav` |
| Windows venv activate fails | Use `venv\Scripts\python.exe` directly instead of activate |
