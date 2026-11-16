---
name: leeeeezc-coldinventorycopilot
description: A ModelScope skill for coldinventorycopilotskill.
---

# 🧊 冷链库存智能副驾驶
## Cold Chain Inventory Copilot：零延迟企业级药品合规 Agent

> **为医院药剂科与冷链仓储而生。不是语音播报，是直接入库的合规 JSON。**

![Intel AI PC](https://img.shields.io/badge/Intel%20AI%20PC-Core%20Ultra%207%20258V-0071C5?style=flat-square&logo=intel&logoColor=white)
![Arc 140V GPU](https://img.shields.io/badge/GPU-Arc%20140V%20Xe2-0071C5?style=flat-square&logo=intel)
![OpenVINO](https://img.shields.io/badge/OpenVINO-2024.5%2B-FF6D00?style=flat-square)
![FastAPI](https://img.shields.io/badge/Skill%20API-FastAPI-009688?style=flat-square&logo=fastapi)
![HIS Ready](https://img.shields.io/badge/HIS%2FERP-JSON%20Ready-28a745?style=flat-square)
![License](https://img.shields.io/badge/License-Apache%202.0-blue?style=flat-square)

---

## 为什么选择这个项目？

市面上已有不少"药品 OCR"工具，它们的逻辑是：**拍照 → 识字 → 念给你听**。

这很好，但这是 To-C 的思路——为有视力障碍的用户设计的语音助手。

**本项目解决的是完全不同的问题：**

| 维度 | To-C 消费端方案 | 本项目（To-B 企业端） |
|------|----------------|----------------------|
| **目标用户** | 老人、视障患者 | 医院药剂师、冷链库管 |
| **输出形式** | 语音播报、自然语言 | 严格 Schema 的机器可读 JSON |
| **下游对接** | 无（人工处理） | HIS/ERP/WMS 系统零触碰入库 |
| **核心价值** | 读懂标签 | **批量合规审计 + 自动预警** |
| **模型调度** | 懒加载/释放节省内存 | 双模型常驻内存，零加载延迟 |
| **处理模式** | 单张交互 | 批量流水线（冷链到货扫描） |

**一句话定位：** 本项目是为医院药剂科和冷链仓储设计的 **AI 合规审计员**，它的每一行输出都是可以直接写入数据库的结构化数据——而不是说给人听的句子。

---

## 核心输出：机器直接可用的合规 JSON

拍一张药品包装照片，30 秒内得到：

```json
{
  "drug_name": "重组人胰岛素注射液",
  "lot_number": "BI20240318",
  "production_date": "2024-03-18",
  "expiration_date": "2026-03-18",
  "is_expired": false,
  "days_until_expiry": 661,
  "warning_level": "SAFE",
  "storage_conditions": "2~8℃冷藏，避免冻结",
  "manufacturer": "某某生物制药股份有限公司"
}
```

`warning_level` 三级预警直接映射到 ERP 告警优先级：

| 值 | 含义 | 推荐动作 |
|----|------|----------|
| `SAFE` | 距过期 >30 天 | 正常入库 |
| `WARNING: NEAR EXPIRY` | 距过期 ≤30 天 | 标记优先使用，触发补货 |
| `CRITICAL: EXPIRED` | 已过期 | **立即隔离，拒绝入库** |

---

## 架构设计：Intel Lunar Lake 混合算力

```
┌─────────────────────────────────────────────────────────────────┐
│                   Intel Core Ultra 7 258V                        │
│                   32 GB 统一内存 (MoP)                           │
│                                                                   │
│  ┌──────────────────────────┐  ┌──────────────────────────────┐  │
│  │   CPU / NPU              │  │   Arc 140V iGPU (Xe2)        │  │
│  │                          │  │                              │  │
│  │  Qwen3-VL-2B-Instruct   │  │  Qwen3-14B INT4              │  │
│  │  视觉 OCR Skill          │  │  企业合规审计 Brain           │  │
│  │  FastAPI ← HTTP ←       │  │  openvino-genai              │  │
│  │  skill_api.py            │  │  LLMPipeline                 │  │
│  └──────────┬───────────────┘  └──────────────┬───────────────┘  │
│             │  OCR 原始文本                    │  合规 JSON        │
│             └─────────────┐  ┌─────────────────┘                  │
│                           ▼  ▼                                    │
│                    local_agent.py                                  │
│                    编排器 / Copilot 入口                           │
└─────────────────────────────────────────────────────────────────┘
                              │
                              ▼
              HIS / ERP / 冷链 WMS 系统
```

### Intel MoP 统一内存：我们的核心技术优势

传统方案（竞品普遍采用）将两个模型**分时调度**：先加载 VLM 做 OCR，卸载后再加载 LLM 做分析。每次切换耗时 **15~60 秒**，批量处理时延迟叠加，无法胜任医院高频扫描场景。

**本项目的做法：**

- `Qwen3-14B INT4` 通过 `openvino-genai` **常驻 Arc 140V GPU**，显存占用约 8 GB
- `Qwen3-VL-2B` 通过 `transformers` **常驻 CPU 侧内存**，约 6 GB
- MoP 架构下 CPU 与 GPU 共享同一物理内存池，**两模型同时在线，零拷贝通信**
- 第一张图片后，所有后续推理均无加载开销——**纯推理延迟 < 30s/张**

```
懒加载方案（竞品）：  加载VLM(30s) → OCR(10s) → 卸载 → 加载LLM(30s) → 分析(15s) = 85s/张
本方案（常驻内存）：  OCR(10s) → 分析(15s) = 25s/张（模型已在内存中）
```

---

## 企业使用场景

### 场景一：冷链到货批量验收

```
冷链车到货 → 扫描每箱胰岛素包装 → 实时比对批号与效期
→ warning_level=CRITICAL 的批次自动触发退货单
→ 合格批次 lot_number + expiration_date 直接写入 WMS
```

### 场景二：药房冷库定期盘点

```
盘点员手持设备拍照 → Copilot 批量生成合规记录
→ days_until_expiry ≤ 30 的品种自动生成补货申请
→ 盘点报告导出，供 NMPA / GMP 审查备档
```

### 场景三：ERP 实时库龄预警

```
每日定时任务扫描库存照片 → JSON 结果推送 ERP
→ 按 warning_level 自动分级处理
→ 药剂科主任收到日报：今日 CRITICAL 0 项，WARNING 3 项，SAFE 247 项
```

---

## 快速开始

### 环境要求

```
操作系统：Windows 11（已针对 Lunar Lake 平台优化）
Python：3.10 ~ 3.12（不支持 3.14）
硬件：Intel Core Ultra 200V 系列（其他平台 CPU 推理可用，GPU 加速需 Intel Arc）
```

### 1. 创建环境并安装依赖

```bash
conda create -n aipc python=3.11 -y
conda activate aipc
pip install -r requirements.txt
```

### 2. 确认模型文件

```
D:\zichenglee\Qwen3-VL-2B-Instruct\        ← 视觉 OCR 模型
D:\zichenglee\Qwen3-14B-int4-ov\
    ├── openvino_model.xml
    ├── openvino_model.bin                  ← 必须存在（~7~8 GB，需 Git LFS 完整拉取）
    └── ...
```

> ⚠️ 若通过 `git clone` 下载，请先执行 `git lfs pull` 确保 `.bin` 权重文件已下载完整。

### 3. 启动 Skill 服务（终端 1）

```bash
conda activate aipc
python skill_api.py
```

模型首次加载约 1~2 分钟，出现以下日志即表示就绪：

```
INFO: Application startup complete.
INFO: Uvicorn running on http://0.0.0.0:8000
```

验证：

```bash
curl http://localhost:8000/health
# {"status":"ok","model":"Qwen3-VL-2B-Instruct"}
```

### 4. 运行完整合规流水线（终端 2）

```bash
conda activate aipc
python local_agent.py drug_package.jpg
```

或用端到端验证脚本（无需提前启动 API 服务）：

```bash
python validate_pipeline.py test_drug.png
```

---

## API 参考

### `POST /extract_drug_info`

#### 请求

```bash
curl -X POST http://localhost:8000/extract_drug_info \
  -F "file=@/path/to/label.jpg"
```

```python
import requests

with open("label.jpg", "rb") as f:
    r = requests.post(
        "http://localhost:8000/extract_drug_info",
        files={"file": ("label.jpg", f, "image/jpeg")}
    )

ocr_text = r.json()["extracted_text"]
```

#### 返回

```json
{
  "extracted_text": "药品名称：重组人胰岛素注射液\n批号：BI20240318\n有效期：2026年03月18日\n贮藏：2~8℃冷藏",
  "filename": "label.jpg"
}
```

完整 OpenAPI 规范见 [`openapi.yaml`](./openapi.yaml)，可直接导入 Postman / Swagger UI。

---

## 项目结构

```
drug-ocr-pipeline/
├── skill_api.py          # ★ Skill 核心：FastAPI + Qwen3-VL-2B OCR 服务
├── openapi.yaml          # ★ OpenAPI 3.0 规范（Agent 框架发现与调用）
├── local_agent.py        # 企业编排器：Brain 推理 + 合规 JSON 生成
├── validate_pipeline.py  # 端到端验证脚本（单命令跑通全流程）
├── requirements.txt      # Python 依赖清单
└── README.md
```

---

## 技术栈

| 组件 | 技术选型 | 运行设备 |
|------|----------|----------|
| 视觉 OCR 模型 | Qwen3-VL-2B-Instruct | CPU（OpenVINO 优化） |
| 合规分析模型 | Qwen3-14B INT4 | Arc 140V iGPU |
| Skill 框架 | FastAPI + Uvicorn | — |
| GPU 推理引擎 | openvino-genai `LLMPipeline` | Arc 140V |
| 图像处理 | Pillow + qwen-vl-utils | — |
| 接口规范 | OpenAPI 3.0 | — |

---

## 常见问题

**Q：报错 `Empty weights data in bin file`？**
> `openvino_model.bin` 权重文件缺失。执行 `git lfs pull` 或手动确认文件大小 ≥ 7 GB。

**Q：OCR 输出乱码或完全错误？**
> 确认 transformers ≥ 4.52（含 `Qwen3VLForConditionalGeneration` 支持）。执行 `pip install -U transformers`。

**Q：`GPU` 设备未找到？**
> 安装 Intel Arc 驱动及 OpenCL 运行时，然后验证：
> ```python
> import openvino; print(openvino.Core().available_devices)
> # 应输出包含 'GPU' 的列表
> ```

**Q：能否部署为医院内网服务？**
> 可以。`skill_api.py` 是标准 FastAPI 应用，支持 Docker 容器化部署，或直接绑定内网 IP 供 HIS 系统调用。

---

## 许可证

本项目采用 [Apache 2.0](https://www.apache.org/licenses/LICENSE-2.0) 开源协议。

---

<div align="center">

**零延迟 · 零云端 · 零数据泄露**

-*Built with ❤️ for ModelScope & Intel "AI PC Agent Skills" Competition*
*专为 Intel Lunar Lake AI PC 设计 · 参赛项目：ModelScope × Intel "AI PC Agent Skills" 竞赛*

</div>
