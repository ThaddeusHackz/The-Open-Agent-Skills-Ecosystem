---
name: waste-classification-agent
description: 识别垃圾类型并获取分类建议。当用户需要：对垃圾图片进行四分类（可回收物/有害垃圾/厨余垃圾/其他垃圾）判断、获取分类理由与处理建议时使用此技能。基于 Qwen3-VL + OpenVINO 本地推理，输出结构化 JSON 结果。

---

# 垃圾分类 Agent — Qwen3-VL + OpenVINO

基于 [modelscope-workshop](https://github.com/openvino-dev-samples/modelscope-workshop) 项目，使用 OpenVINO 运行 Qwen3-VL，对垃圾图片进行自动分类并给出处理建议。

## 前置条件

- 虚拟环境已激活：`source ~/modelscope-workshop/ov_workshop/bin/activate`
- 模型目录存在：`~/modelscope-workshop/lab1-multimodal-vlm/Qwen3-VL-4B-Instruct-int4-ov/`

---

## 加载模型

```python
import os
from optimum.intel.openvino import OVModelForVisualCausalLM
from transformers import AutoProcessor

model_dir = os.path.expanduser("~/modelscope-workshop/lab1-multimodal-vlm/Qwen3-VL-4B-Instruct-int4-ov")

model = OVModelForVisualCausalLM.from_pretrained(model_dir, device="AUTO")
print("✅ 模型加载完成")

min_pixels = 256 * 28 * 28
max_pixels = 1280 * 28 * 28
processor = AutoProcessor.from_pretrained(
    model_dir, min_pixels=min_pixels, max_pixels=max_pixels, fix_mistral_regex=True
)
```

> 若模型不存在，先下载：
>
> ```python
> from pathlib import Path
> from modelscope import snapshot_download
> model_dir = Path("~/modelscope-workshop/lab1-multimodal-vlm/Qwen3-VL-4B-Instruct-int4-ov").expanduser()
> if not model_dir.exists():
>  snapshot_download("snake7gun/Qwen3-VL-4B-Instruct-int4-ov", local_dir=str(model_dir))
> ```

---

## 垃圾分类推理

### 核心函数

```python
import json
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict

from PIL import Image

CATEGORIES = ["可回收物", "有害垃圾", "厨余垃圾", "其他垃圾"]


def _extract_json(text: str) -> Dict:
    """优先解析模型输出中的 JSON；失败时返回空字典。"""
    text = text.strip()
    candidate = text
    match = re.search(r"\{[\s\S]*\}", text)
    if match:
        candidate = match.group(0)
    try:
        return json.loads(candidate)
    except Exception:
        return {}


def _normalize_category(raw: str) -> str:
    """将模型输出的分类标签归一化到标准四分类。"""
    raw = (raw or "").strip()
    for c in CATEGORIES:
        if c in raw:
            return c
    keyword_map = {
        "可回收": "可回收物",
        "有害": "有害垃圾",
        "厨余": "厨余垃圾",
        "湿垃圾": "厨余垃圾",
        "干垃圾": "其他垃圾",
        "其他": "其他垃圾",
    }
    for k, v in keyword_map.items():
        if k in raw:
            return v
    return "其他垃圾"


def classify_waste(image_path: Path, user_note: str = "") -> Dict:
    """垃圾分类 Agent：输入图片路径，输出结构化分类结果。"""
    prompt = f"""
你是一个垃圾分类助手。请根据图片内容判断主要垃圾类别。
分类只能从以下四类中选择一项：{', '.join(CATEGORIES)}。
用户补充信息：{user_note or '无'}

请严格输出 JSON（不要额外文字），格式如下：
{{
  "category": "可回收物|有害垃圾|厨余垃圾|其他垃圾",
  "reason": "简要理由，不超过40字",
  "confidence": 0.0,
  "advice": "处理建议，不超过40字"
}}
""".strip()

    messages = [
        {
            "role": "user",
            "content": [
                {"type": "image", "image": str(image_path)},
                {"type": "text", "text": prompt},
            ],
        }
    ]

    inputs = processor.apply_chat_template(
        messages,
        tokenize=True,
        add_generation_prompt=True,
        return_dict=True,
        return_tensors="pt",
    )

    output_ids = model.generate(**inputs, max_new_tokens=160, do_sample=False)
    generated_trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, output_ids)]
    text = processor.batch_decode(
        generated_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0].strip()

    data = _extract_json(text)
    category = _normalize_category(str(data.get("category", "")))
    reason = str(data.get("reason", "未提供理由"))
    advice = str(data.get("advice", "请按当地垃圾分类规范投放。"))
    confidence = data.get("confidence", 0.5)
    try:
        confidence = float(confidence)
    except Exception:
        confidence = 0.5
    confidence = max(0.0, min(1.0, confidence))

    return {
        "category": category,
        "reason": reason,
        "confidence": confidence,
        "advice": advice,
        "raw_output": text,
    }


def classify_waste_image(image: Image.Image, user_note: str = "") -> Dict:
    """接受 PIL Image 对象的包装函数。"""
    if image is None:
        return {
            "category": "其他垃圾",
            "reason": "未上传图片",
            "confidence": 0.0,
            "advice": "请先上传图片再分类。",
            "raw_output": "",
        }

    with NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp_path = Path(f.name)
    image.save(tmp_path)

    try:
        result = classify_waste(tmp_path, user_note)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

    return result
```

### 使用示例

```python
# 对本地图片分类
result = classify_waste(Path("waste.jpg"))
print(json.dumps(result, ensure_ascii=False, indent=2))
# 输出示例:
# {
#   "category": "可回收物",
#   "reason": "塑料瓶为可回收材料，无有害成分",
#   "confidence": 0.98,
#   "advice": "投放至可回收物垃圾桶",
#   "raw_output": "{ ... }"
# }

# 带补充信息分类
result = classify_waste(Path("waste.jpg"), user_note="好像是电池")
# → category 会归为 "有害垃圾"
```

---

## Gradio 交互式演示

```python
import gradio as gr


def waste_agent_demo(image, user_note):
    result = classify_waste_image(image, user_note)
    answer = (
        f"分类结果：{result['category']}\n"
        f"置信度：{result['confidence']:.2f}\n"
        f"判断理由：{result['reason']}\n"
        f"处理建议：{result['advice']}"
    )
    return answer, result


with gr.Blocks(title="垃圾分类 Agent") as demo:
    gr.Markdown("# 垃圾分类 Agent\n上传图片，自动判断垃圾类别并给出处理建议。")
    with gr.Row():
        image_input = gr.Image(type="pil", label="上传垃圾图片")
        with gr.Column():
            note_input = gr.Textbox(label="补充描述（可选）", placeholder="例如：电池、塑料瓶、果皮等")
            run_button = gr.Button("开始分类")
    text_output = gr.Textbox(label="分类结果")
    json_output = gr.JSON(label="结构化输出")

    run_button.click(waste_agent_demo, [image_input, note_input], [text_output, json_output])

demo.launch(share=False)   # 浏览器打开 http://127.0.0.1:7860
```

---

## 输出说明

分类结果为结构化 JSON，包含以下字段：

| 字段         | 类型   | 说明                                                        |
| ------------ | ------ | ----------------------------------------------------------- |
| `category`   | string | 分类结果：`可回收物` / `有害垃圾` / `厨余垃圾` / `其他垃圾` |
| `reason`     | string | 判断理由（不超过 40 字）                                    |
| `confidence` | float  | 置信度（0.0 ~ 1.0）                                         |
| `advice`     | string | 处理建议（不超过 40 字）                                    |
| `raw_output` | string | 模型原始输出文本                                            |

---

## 常见错误排查

| 错误                           | 原因               | 解决方法                                                     |
| ------------------------------ | ------------------ | ------------------------------------------------------------ |
| `FileNotFoundError: model_dir` | 模型未下载         | 确认模型目录路径正确，或运行上方下载代码                     |
| JSON 解析失败返回空字典        | 模型输出格式不稳定 | `category` 会归一化到 `其他垃圾`，可调大 `max_new_tokens` 重试 |
| Gradio 端口占用                | 7860 端口被占用    | `demo.launch(server_port=7861)`                              |
