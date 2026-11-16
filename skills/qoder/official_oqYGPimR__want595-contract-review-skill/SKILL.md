---
name: contract-review-agent
description: 审查合同图片，识别风险条款并给出修改建议。当用户需要：对合同图片进行风险识别（高风险/中风险/低风险/无风险）、获取合同类型判断、风险条款与原因分析、修改建议时使用此技能。基于 Qwen3-VL + OpenVINO 本地推理，输出结构化 JSON 结果。
allowed-tools: Bash(python *), Bash(pip *), Bash(cd *), Bash(source *), Read, Glob, Write

---

# 合同审查 Agent — Qwen3-VL + OpenVINO

基于 [modelscope-workshop](https://github.com/openvino-dev-samples/modelscope-workshop) 项目，使用 OpenVINO 运行 Qwen3-VL，对合同图片进行自动审查分析并给出风险评级和修改建议。

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

## 合同审查推理

### 核心函数

```python
import json
import re
from pathlib import Path
from tempfile import NamedTemporaryFile
from typing import Dict, List

from PIL import Image

RISK_LEVELS = ["高风险", "中风险", "低风险", "无风险"]


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


def _normalize_risk(raw: str) -> str:
    """将模型输出的风险等级归一化到标准四等级。"""
    raw = (raw or "").strip()
    for r in RISK_LEVELS:
        if r in raw:
            return r

    keyword_map = {
        "高": "高风险",
        "严重": "高风险",
        "中": "中风险",
        "一般": "中风险",
        "低": "低风险",
        "轻微": "低风险",
        "无": "无风险",
        "安全": "无风险",
        "合规": "无风险",
    }
    for k, v in keyword_map.items():
        if k in raw:
            return v
    return "中风险"


def _normalize_list(raw_items) -> List[str]:
    """将模型输出的列表规范化为字符串列表。"""
    if isinstance(raw_items, list):
        return [str(item) for item in raw_items if item]
    if isinstance(raw_items, str):
        items = re.split(r"[；;\n]", raw_items)
        return [item.strip().lstrip("0123456789.、") for item in items if item.strip()]
    return []


def review_contract(image_path: Path, user_note: str = "") -> Dict:
    """合同审查 Agent：输入合同图片路径，输出结构化审查结果。"""
    prompt = f"""
你是一个专业的合同审查助手。请根据图片中的合同内容进行审查分析。
风险等级只能从以下四类中选择一项：{', '.join(RISK_LEVELS)}。
用户补充信息：{user_note or '无'}

请严格输出 JSON（不要额外文字），格式如下：
{{
  "contract_type": "合同类型，如劳动合同、租赁合同、买卖合同等",
  "risk_level": "高风险|中风险|低风险|无风险",
  "risk_clauses": ["风险条款1", "风险条款2"],
  "risk_reasons": ["风险原因1", "风险原因2"],
  "suggestions": ["修改建议1", "修改建议2"],
  "summary": "综合审查意见，不超过100字"
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

    output_ids = model.generate(**inputs, max_new_tokens=512, do_sample=True)
    generated_trimmed = [out[len(inp):] for inp, out in zip(inputs.input_ids, output_ids)]
    text = processor.batch_decode(
        generated_trimmed,
        skip_special_tokens=True,
        clean_up_tokenization_spaces=False,
    )[0].strip()

    data = _extract_json(text)
    contract_type = str(data.get("contract_type", "未识别"))
    risk_level = _normalize_risk(str(data.get("risk_level", "")))
    risk_clauses = _normalize_list(data.get("risk_clauses", []))
    risk_reasons = _normalize_list(data.get("risk_reasons", []))
    suggestions = _normalize_list(data.get("suggestions", []))
    summary = str(data.get("summary", "暂无综合审查意见。"))

    # 若没有识别到风险条款但风险等级为高/中，补充提示
    if not risk_clauses and risk_level in ("高风险", "中风险"):
        risk_clauses = ["未识别到具体风险条款，但合同整体存在风险"]
    if not risk_reasons and risk_level in ("高风险", "中风险"):
        risk_reasons = ["建议由专业律师进一步审查"]
    if not suggestions and risk_level in ("高风险", "中风险"):
        suggestions = ["建议咨询专业律师进行详细审查"]

    return {
        "contract_type": contract_type,
        "risk_level": risk_level,
        "risk_clauses": risk_clauses,
        "risk_reasons": risk_reasons,
        "suggestions": suggestions,
        "summary": summary,
        "raw_output": text,
    }


def review_contract_image(image: Image.Image, user_note: str = "") -> Dict:
    """接受 PIL Image 对象的包装函数。"""
    if image is None:
        return {
            "contract_type": "未识别",
            "risk_level": "中风险",
            "risk_clauses": [],
            "risk_reasons": ["未上传合同图片"],
            "suggestions": ["请先上传合同图片再审查。"],
            "summary": "未上传合同，无法审查。",
            "raw_output": "",
        }

    with NamedTemporaryFile(suffix=".png", delete=False) as f:
        tmp_path = Path(f.name)
    image.save(tmp_path)

    try:
        result = review_contract(tmp_path, user_note)
    finally:
        if tmp_path.exists():
            tmp_path.unlink()

    return result
```

### 使用示例

```python
# 对本地合同图片审查
result = review_contract(Path("contract.jpg"))
print(json.dumps(result, ensure_ascii=False, indent=2))
# 输出示例:
# {
#   "contract_type": "劳动合同",
#   "risk_level": "中风险",
#   "risk_clauses": ["竞业限制条款范围过宽", "违约金比例过高"],
#   "risk_reasons": ["竞业限制未明确地域和行业范围", "违约金超出法定上限"],
#   "suggestions": ["明确竞业限制的地域和行业范围", "将违约金调整至法定合理范围"],
#   "summary": "该劳动合同竞业限制和违约条款存在风险，建议进一步协商修改。",
#   "raw_output": "{ ... }"
# }

# 带补充信息审查
result = review_contract(Path("contract.jpg"), user_note="重点关注违约责任")
# → risk_clauses 会侧重违约相关条款
```

---

## Gradio 交互式演示

```python
import gradio as gr

RISK_EMOJI = {"高风险": "🔴", "中风险": "🟡", "低风险": "🟢", "无风险": "✅"}


def contract_agent_demo(image, user_note):
    result = review_contract_image(image, user_note)
    risk_emoji = RISK_EMOJI.get(result["risk_level"], "⚪")

    clauses_text = "\n".join(f"  - {c}" for c in result["risk_clauses"]) if result["risk_clauses"] else "  无"
    reasons_text = "\n".join(f"  - {r}" for r in result["risk_reasons"]) if result["risk_reasons"] else "  无"
    suggestions_text = "\n".join(f"  - {s}" for s in result["suggestions"]) if result["suggestions"] else "  无"

    answer = (
        f"合同类型：{result['contract_type']}\n"
        f"风险等级：{risk_emoji} {result['risk_level']}\n\n"
        f"⚠️ 风险条款：\n{clauses_text}\n\n"
        f"📋 风险原因：\n{reasons_text}\n\n"
        f"💡 修改建议：\n{suggestions_text}\n\n"
        f"📝 综合意见：{result['summary']}"
    )
    return answer, result


with gr.Blocks(title="合同审查 Agent", theme=gr.themes.Soft()) as demo:
    gr.Markdown("# 合同审查 Agent\n上传合同图片，自动识别合同类型、分析风险条款并给出修改建议。")
    with gr.Row():
        image_input = gr.Image(type="pil", label="上传合同图片")
        with gr.Column():
            note_input = gr.Textbox(
                label="补充描述（可选）",
                placeholder="例如：劳动合同、租赁合同、关注违约条款等",
                lines=3,
            )
            review_focus = gr.CheckboxGroup(
                choices=["违约责任", "付款条款", "保密条款", "竞业限制", "争议解决", "知识产权"],
                label="重点关注（可选）",
            )
            run_button = gr.Button("开始审查", variant="primary")
    text_output = gr.Textbox(label="审查报告", lines=18)
    json_output = gr.JSON(label="结构化输出")

    run_button.click(contract_agent_demo, [image_input, note_input], [text_output, json_output])

demo.launch(share=False)   # 浏览器打开 http://127.0.0.1:7860
```

---

## 输出说明

审查结果为结构化 JSON，包含以下字段：

| 字段            | 类型         | 说明                                                         |
| --------------- | ------------ | ------------------------------------------------------------ |
| `contract_type` | string       | 合同类型：`劳动合同` / `租赁合同` / `买卖合同` / `服务合同` 等 |
| `risk_level`    | string       | 风险等级：`高风险` / `中风险` / `低风险` / `无风险`          |
| `risk_clauses`  | list[string] | 识别到的风险条款列表                                         |
| `risk_reasons`  | list[string] | 风险原因列表                                                 |
| `suggestions`   | list[string] | 修改建议列表                                                 |
| `summary`       | string       | 综合审查意见（不超过 100 字）                                |
| `raw_output`    | string       | 模型原始输出文本                                             |

---

## 常见错误排查

| 错误                           | 原因               | 解决方法                                                     |
| ------------------------------ | ------------------ | ------------------------------------------------------------ |
| `FileNotFoundError: model_dir` | 模型未下载         | 确认模型目录路径正确，或运行上方下载代码                     |
| JSON 解析失败返回空字典        | 模型输出格式不稳定 | `risk_level` 会归一化到 `中风险`，可调大 `max_new_tokens` 重试 |
| Gradio 端口占用                | 7860 端口被占用    | `demo.launch(server_port=7861)`                              |
