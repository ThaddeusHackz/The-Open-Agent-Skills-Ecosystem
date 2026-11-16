---
name: audio-translator
description: Translate English audio files to Chinese text using OpenVINO-optimized Whisper (ASR) and HY-MT1.5 (translation) models. Use when the user provides an audio file and wants it transcribed and translated, or mentions audio translation, speech-to-text translation, or English-to-Chinese audio conversion.
---

# Audio Translator (English → Chinese)

Translates English audio to Chinese text using two OpenVINO-optimized models:
1. **distil-whisper-large-v3-int8-ov** — English speech recognition
2. **HY-MT1.5-1.8B-int4-ov** — Machine translation (EN → ZH)

## Prerequisites

### System Requirements
- Python 3.10+
- ~2GB disk space for models
- Recommended: 8GB+ RAM (CPU inference)

### Install Dependencies

Use Aliyun PyPI mirror for faster downloads in China:

```bash
pip install openvino-genai librosa soundfile numpy modelscope -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

Or install from the bundled requirements file:

```bash
pip install -r scripts/requirements.txt -i https://mirrors.aliyun.com/pypi/simple/ --trusted-host mirrors.aliyun.com
```

**Package details:**

| Package | Version | Purpose |
|---------|---------|---------|
| `openvino-genai` | >=2025.0 | OpenVINO GenAI inference engine (WhisperPipeline, LLMPipeline) |
| `librosa` | >=0.10 | Audio loading and resampling to 16kHz mono |
| `soundfile` | >=0.12 | Audio file I/O backend for librosa |
| `numpy` | >=1.24 | Array operations for audio data |
| `modelscope` | >=1.10 | Download models from ModelScope hub |

### Download Models

Models are downloaded from ModelScope (Aliyun-hosted). Run once:

```bash
python scripts/download_models.py
```

Models are stored at the workspace root `models/` directory (~1.8GB total):
- `models/distil-whisper-large-v3-int8-ov/` — Whisper ASR model (~730MB)
- `models/HY-MT1.5-1.8B-int4-ov/` — Translation model (~1.12GB)

Already-downloaded models are automatically skipped on re-run.

#### Custom Models Directory

If you want to store models in a different location, use `--models-dir` or set the environment variable:

```bash
# Option 1: CLI argument
python scripts/download_models.py --models-dir /your/custom/path
python scripts/translate.py --models-dir /your/custom/path audio.wav

# Option 2: Environment variable (applies to both scripts)
export AUDIO_TRANSLATOR_MODELS_DIR=/your/custom/path
python scripts/download_models.py
python scripts/translate.py audio.wav
```

Priority: `--models-dir` > `AUDIO_TRANSLATOR_MODELS_DIR` env var > default (`scripts/models/`).

## Usage

### Basic Translation

When the user provides an English audio file, run:

```bash
python scripts/translate.py <audio_file>
```

### Options

```bash
# Use GPU for faster inference (if available)
python scripts/translate.py --device GPU <audio_file>

# Save result to file
python scripts/translate.py -o output.txt <audio_file>

# Change target language
python scripts/translate.py --target-lang Japanese <audio_file>
```

| Option | Default | Description |
|--------|---------|-------------|
| `--device` | `CPU` | Inference device: `CPU`, `GPU`, `NPU` |
| `--source-lang` | `English` | Source language |
| `--target-lang` | `Chinese` | Target language |
| `--output`, `-o` | (none) | Save translation result to file |
| `--models-dir` | (see below) | Custom path to models directory |

### Supported Audio Formats

wav, mp3, flac, ogg — audio is automatically resampled to 16kHz mono.

## Workflow

When this skill is triggered:

1. **Verify setup**: Check that `models/` directory exists and contains model files. If not, run `python scripts/download_models.py` first.
2. **Run translation**: Execute `python scripts/translate.py <audio_file>` with the user's audio file path.
3. **Return results**: Present the English transcription and Chinese translation to the user.

### Expected Output

```
============================================================
  English Audio → Chinese Translation
  Input: audio.wav
============================================================
[INFO] Loading Whisper model on CPU ...
[INFO] Whisper model loaded.
[INFO] Audio: audio.wav (5.9s)
[INFO] Transcribing audio ...
[INFO] Transcription done (6.0s): Mr. Quilter is the apostle of the middle classes.
[INFO] Loading translation model on CPU ...
[INFO] Translation model loaded.
[INFO] Translating English → Chinese ...
[INFO] Translation done (178.8s): 奎特先生是中产阶级的使者。
============================================================
  Result
============================================================
  🇬🇧 English : Mr. Quilter is the apostle of the middle classes.
  🇨🇳 Chinese : 奎尔特先生是中产阶级的使者。
============================================================
```

## Troubleshooting

- **Model not found**: Run `python scripts/download_models.py` to download models
- **`No module named 'openvino_genai'`**: Ensure using the correct Python environment where dependencies are installed
- **Slow CPU translation**: The HY-MT1.5 model takes ~3min/CPU for a short sentence. Use `--device GPU` if GPU is available
- **Audio format error**: Ensure `librosa` and `soundfile` are installed; convert audio to wav as fallback

## Additional Resources

- For detailed model information and architecture, see [reference.md](reference.md)
