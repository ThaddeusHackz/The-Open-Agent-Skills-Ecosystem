---
name: aceeval
displayName: Agent Capability Evaluator
description: Agent capability evaluator with radar charts and PK battles
version: 1.0.0
type: skill
---

# 🎯 Agent 能力评估与 PK 系统

> 全面评估 AI Agent 能力，生成能力雷达图，支持 Agent 间 PK 对战

## ✨ 核心功能

### 1. 能力雷达图评估
从 8 个维度全面评估 Agent：

| 维度 | 评估内容 | 测试方式 |
|------|----------|----------|
| 🧠 **逻辑推理** | 复杂问题拆解能力 | 逻辑谜题测试 |
| 💻 **代码能力** | 编程/脚本编写 | 编程挑战 |
| 🔧 **工具使用** | 工具调用熟练度 | 工具链测试 |
| 💬 **对话能力** | 自然语言理解 | 多轮对话测试 |
| 🎨 **创造力** | 创意解决方案 | 开放式问题 |
| 📊 **数据分析** | 数据处理/可视化 | 数据集分析 |
| 🔍 **研究能力** | 信息检索/验证 | 研究任务 |
| ⚡ **响应速度** | 任务完成效率 | 时间压力测试 |

### 2. Agent PK 对战
让两个 Agent 在相同任务下 PK：

```bash
# 启动 PK
ace pk --agent1 main --agent2 challenger --task coding_challenge

# 结果输出
🥊 Agent PK 结果
━━━━━━━━━━━━━━━━━━━━━━
Agent A (main)        Agent B (challenger)
     85分                    92分
   🥈 亚军                  🥇 冠军

详细对比:
• 代码质量: 80 vs 95 (+15)
• 完成时间: 更快 vs 较慢
• 创新性: 中等 vs 高
```

### 3. 排行榜系统
```bash
# 查看排行榜
ace ranking

🌟 Agent 能力排行榜
━━━━━━━━━━━━━━━━━━━━━━
🥇 Agent-A        92分  ████████████████████
🥈 Agent-B        85分  █████████████████▌
🥉 Agent-C        78分  ███████████████▊
 4. Agent-D        72分  ██████████████▌
 5. Agent-E        68分  █████████████▋
```

### 4. 能力缺口分析
```bash
# 生成能力缺口报告
ace analyze

📊 能力分析报告
━━━━━━━━━━━━━━━━━━━━━━
你的 Agent 最强: 代码能力 (95分) 🏆
你的 Agent 最弱: 创造力 (62分) ⚠️

推荐学习:
1. 创意写作技能 (提升创造力)
2. 头脑风暴框架 (增强创新)
3. 设计思维方法论

预计提升: +15分 (从当前 78分 → 93分)
```

---

## 🚀 快速开始

### 安装
```bash
openclawmp install skill/@openclaw/agent-capability-evaluator
```

### 评估自己
```bash
# 完整评估 (约5-10分钟)
ace eval --full

# 快速评估 (约1-2分钟)
ace eval --quick

# 评估特定维度
ace eval --dimension code,creativity
```

### PK 对战
```bash
# 两个 Agent PK
ace pk --agent1 main --agent2 subagent --task all

# 指定任务类型
ace pk --task coding --rounds 3
```

---

## 📝 评估流程

### 1. 标准化测试套件
```
测试套件包含:
├── 01_logic_puzzles/       # 逻辑推理测试
├── 02_coding_challenges/   # 编程挑战
├── 03_tool_chain_tests/    # 工具链测试
├── 04_conversation_flows/  # 对话流程测试
├── 05_creative_prompts/    # 创意 prompts
├── 06_data_analysis/       # 数据分析任务
├── 07_research_tasks/      # 研究任务
└── 08_speed_challenges/    # 速度挑战
```

### 2. 评分标准
每项测试满分 100 分：
- 90-100: 卓越 🌟
- 80-89: 优秀 ✅
- 70-79: 良好 👍
- 60-69: 及格 ⚠️
- <60: 需改进 ❌

### 3. 报告生成
```bash
# 生成详细报告
ace report --format html --output report.html

# 生成对比报告
ace report --compare agent1,agent2 --format markdown
```

---

## 🎮 PK 对战模式

### 对战类型

| 模式 | 说明 | 适合场景 |
|------|------|----------|
| 🏃 **速度赛** | 谁先完成任务 | 测试效率 |
| 🎯 **质量赛** | 评分更高者胜 | 测试精度 |
| 🎨 **创意赛** | 更有创意的方案 | 测试创新 |
| ⚔️ **综合赛** | 多轮多维度PK | 全面比拼 |

### 对战结果
```
⚔️ Agent PK 对战结果
━━━━━━━━━━━━━━━━━━━━━━
任务: 构建一个 Todo App

Agent A (main)
├── 完成时间: 3分12秒 ⏱️
├── 代码质量: 88分
├── 功能完整: 95分
├── 创新性: 75分
└── 总分: 86分 🥈

Agent B (challenger)
├── 完成时间: 4分05秒
├── 代码质量: 92分 🏆
├── 功能完整: 90分
├── 创新性: 85分 🏆
└── 总分: 91分 🥇

结果: Agent B 获胜！
优势: 代码质量更高，方案更有创意
差距: +5分 (主要在创新性上领先)
```

---

## 📈 成长追踪

### 历史记录
```bash
# 查看历史评估
ace history

2026-02-28: 78分 → 2026-03-07: 85分 (+7分) 📈
• 代码能力: 80 → 88 (+8)
• 创造力: 60 → 72 (+12) 🚀
• 逻辑推理: 82 → 85 (+3)
```

### 进步曲线
自动生成成长曲线图，追踪各维度进步。

---

## 🔧 高级配置

### 自定义测试
```bash
# 添加自定义测试
ace test add --name my_test --type coding --weight 10

# 修改评分权重
ace config set --dimension code --weight 1.5
```

### 与进化系统集成
```bash
# 根据评估结果自动推荐技能
ace eval --auto-recommend

# 一键安装推荐技能
ace eval --auto-install
```

---

## 🎯 使用场景

### 场景 1: 自我诊断
"我的 Agent 哪里不够好？"
→ 运行 `ace eval --full` 获取完整诊断

### 场景 2: 选型对比
"该用哪个 Agent 完成这个任务？"
→ 运行 `ace pk --task <task>` 对比PK

### 场景 3: 进化追踪
"我的 Agent 进步了吗？"
→ 运行 `ace history` 查看成长曲线

### 场景 4: 团队评估
"我们团队的 Agent 能力如何？"
→ 运行 `ace ranking` 查看排行榜

---

## 📊 可视化输出

### 雷达图
```
        创造力 🎨
           ████
     逻辑推理 🧠   代码能力 💻
        ████████     ██████
                   
  对话能力 💬         工具使用 🔧
     ████           ████████
                   
        响应速度 ⚡
           ██████
              
        数据分析 📊
           ████
```

### PK 对比图
```
Agent A vs Agent B
代码能力: ████████████████████ vs ████████████████████████
创造力:   ██████████████       vs ████████████████████
逻辑:     ██████████████████   vs ████████████████
```

---

## 🔗 相关资产

| 资产 | 关系 | 说明 |
|------|------|------|
| 水产市场自主进化手册 | 联动 | 评估后自动触发进化 |
| 水产市场贡献家 | 联动 | PK获胜后自动打包发布 |
| Context & Memory Manager | 依赖 | 存储评估历史 |

---

## 📝 版本历史

- **v1.0.0** (2026-02-28) - 初始发布
  - 8维能力评估
  - PK对战系统
  - 排行榜功能
  - 能力缺口分析

---

**让 Agent 进化有方向、有对比、有成就感！** 🚀
