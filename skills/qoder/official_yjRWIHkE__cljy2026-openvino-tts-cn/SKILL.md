---
name: openvino-tts-cn
description: 在 Windows 本地运行 OpenVINO 端侧中文语音合成（OpenVoice V2 + MeloTTS）。当用户需要：合成中文语音、把文字念出来、文本转语音、或替代 cloud-TTS/GPT-SoVITS 服务时使用此技能。HTTP 接口与 GPT-SoVITS api_v2.py 完全兼容，上游项目只需改一行 URL。
allowed-tools: Bash(python *), Bash(pip *), Bash(cd *), Bash(call *), Bash(curl *), Read, Glob, Write
---

# OpenVINO 端侧中文 TTS (Windows 本地)

基于 OpenVoice V2 + MeloTTS，使用 OpenVINO Runtime 在 Intel CPU/iGPU/NPU 上运行中文语音合成。HTTP 接口与 [GPT-SoVITS api_v2.py](https://github.com/RVC-Boss/GPT-SoVITS) 完全兼容。

## 工作目录结构

```
D:\P\openvino\
├── app.py                         # Gradio 前端入口（创空间 / 本地 UI）
├── pyproject.toml                 # 项目配置，pip install -e . 即可
├── src/openvino_tts_cn/
│   ├── __main__.py                # CLI: python -m openvino_tts_cn
│   ├── config.py                  # Pydantic Settings (env_prefix=OVTTS_)
│   ├── pipeline.py                # OpenVoicePipeline + Stub fallback
│   ├── server.py                  # FastAPI app（POST /tts, GET /health）
│   ├── audio_io.py                # wav 编解码 + 静音生成
│   └── exceptions.py              # 业务异常 → HTTP 状态码
├── scripts/
│   ├── convert_models.py          # PyTorch → OpenVINO IR
│   └── benchmark.py               # RTF 基准测试
├── models/openvino/               # 转换后的 IR 模型（可选，无模型进 Stub 模式）
├── tests/                         # 20 个测试，纯 stub，2 秒跑完
└── docs/
    └── evidence/                  # 运行证据 (wav/png/log)
```

---

## 第一步：环境搭建

### 方式 A：使用虚拟环境（推荐）

```bat
cd D:\P\openvino
python -m venv .venv
call .venv\Scripts\activate.bat
pip install -e .
```

### 方式 B：直接安装到当前环境

```bat
cd D:\P\openvino
pip install -e .
```

### 核心依赖说明

```
openvino>=2025.0          # OpenVINO 推理引擎
fastapi>=0.115            # HTTP 服务框架
uvicorn>=0.32             # ASGI 服务器
gradio>=5.0               # Web UI（Gradio 前端）
soundfile>=0.12           # wav 编解码
librosa>=0.10             # 音频重采样
pydantic>=2.9             # 请求校验
```

### 验证安装

```bat
cd D:\P\openvino
python -c "import openvino as ov; print(ov.__version__); print(ov.Core().available_devices)"
pytest -v    # → 20 passed in ~2s
```

---

## 第二步：启动 HTTP 服务

服务监听 `127.0.0.1:9880`，与 GPT-SoVITS 默认端口一致。

```bat
cd D:\P\openvino
python -m openvino_tts_cn -p 9880
```

启动后检查健康状态：

```bat
curl -s http://127.0.0.1:9880/health
```

预期输出：

```json
{
    "status": "ok",
    "stub_mode": true,
    "device": "CPU",
    "models_dir": "D:\\P\\openvino\\models",
    "version": "0.1.0"
}
```

- `stub_mode: true` 表示 IR 模型未就绪，返回静音 wav（HTTP 契约完全真实，可联调）
- `stub_mode: false` 表示真实推理模式

### 环境变量配置

| 变量 | 默认 | 说明 |
|------|------|------|
| `OVTTS_HOST` | `127.0.0.1` | 监听地址 |
| `OVTTS_PORT` | `9880` | 监听端口 |
| `OVTTS_DEVICE` | `CPU` | OpenVINO device：CPU / GPU / NPU / AUTO |
| `OVTTS_MODELS_DIR` | `./models` | IR 模型根目录 |
| `OVTTS_DEFAULT_SPEED` | `1.0` | 默认语速 |

---

## 第三步：合成语音

### 最小调用（仅 text 字段）

```bat
curl -s -X POST http://127.0.0.1:9880/tts ^
  -H "Content-Type: application/json" ^
  -d "{\"text\":\"你好，欢迎使用 OpenVINO 端侧语音合成\",\"speed_factor\":1.0}" ^
  -o output.wav
```

### 程序调用（Python）

```python
import requests

resp = requests.post("http://127.0.0.1:9880/tts", json={
    "text": "苹果公司最新财报显示，营收同比增长百分之八点二",
    "text_lang": "zh",
    "speed_factor": 1.0,
})
resp.raise_for_status()
with open("output.wav", "wb") as f:
    f.write(resp.content)

# 响应头包含元信息
print(f"时长: {resp.headers.get('x-ovtts-duration-ms')} ms")
print(f"采样率: {resp.headers.get('x-ovtts-sample-rate')} Hz")
print(f"Stub模式: {resp.headers.get('x-ovtts-stub-mode')}")
```

### GPT-SoVITS 全套字段兼容

以下字段全部接受，GPT-SoVITS 独有字段被静默忽略（不报错）：

```python
requests.post("http://127.0.0.1:9880/tts", json={
    "text": "要合成的文本",
    "text_lang": "zh",
    "ref_audio_path": "",
    "prompt_text": "",
    "speed_factor": 1.0,
    "media_type": "wav",
    "streaming_mode": False,
    # 以下为 GPT-SoVITS 独有字段，接受并忽略
    "top_k": 10, "top_p": 1.0, "temperature": 0.7,
    "n_timesteps": 20, "text_split_method": "cut2",
    "fragment_interval": 0.05,
    "inference_cfg_rate": 0.7, "cfm_temperature": 0.6,
})
```

---

## 第四步：Gradio UI

启动 Gradio 前端（监听 7860 端口）：

```bat
cd D:\P\openvino
python app.py
```

浏览器打开 `http://127.0.0.1:7860`，界面包含：

- 文本输入框（支持多行中文）
- 语速滑块（0.5–2.0）
- 参考音频上传（可选，用于音色克隆）
- 合成按钮 → 在线播放 + 显示 RTF / 推理耗时 / stub_mode 状态

---

## 第五步：模型转换（可选，获得真实推理）

Stub 模式已可完成联调。如需真实语音输出：

```bat
cd D:\P\openvino
pip install -e .[convert]

python scripts/convert_models.py ^
  --melotts vendor/melotts_zh ^
  --openvoice vendor/checkpoints_v2 ^
  --out models/openvino
```

转换后 `models/openvino/` 下应有：

```
models/openvino/
├── melotts/         model.xml + model.bin
├── speaker_encoder/ model.xml + model.bin
└── tone_converter/  model.xml + model.bin
```

重启服务后 `/health` 显示 `"stub_mode": false`。

---

## 快速检查清单

1. **Python 版本**：3.10–3.12
2. **依赖已装**：`pip install -e .` 无报错
3. **OpenVINO 版本**：`python -c "import openvino; print(openvino.__version__)"` 应 >= 2025.0
4. **可用设备**：`python -c "import openvino as ov; print(ov.Core().available_devices)"`
5. **测试通过**：`pytest -v` → 20 passed
6. **服务可达**：`curl http://127.0.0.1:9880/health` 返回 JSON

---

## 性能参考 (Intel Core Ultra 7 155H, Windows 11)

| 模式 | RTF | 说明 |
|------|-----|------|
| Stub 模式 | ~0.001 | 返回静音 wav，用于联调 |
| CPU 真实推理 | < 0.3 | 合成 1 秒音频 < 0.3 秒 |
| GPU/NPU | 待测 | tone converter 部分算子回落 CPU |

---

## 常见错误排查

| 错误 | 原因 | 解决方法 |
|------|------|----------|
| `ModuleNotFoundError: openvino` | 未安装依赖 | `pip install -e .` |
| HTTP 422 `text too short` | text 为空 | 传入至少 1 个字符 |
| `stub_mode: true` | IR 模型未就绪 | 运行 `scripts/convert_models.py` 或继续用 Stub 联调 |
| 端口 9880 被占用 | GPT-SoVITS 或其他服务占用 | `OVTTS_PORT=9881 python -m openvino_tts_cn` |
| Windows curl 中文乱码 | shell 编码问题 | 用 `--data-binary @req.json` 代替命令行直接写中文 |
