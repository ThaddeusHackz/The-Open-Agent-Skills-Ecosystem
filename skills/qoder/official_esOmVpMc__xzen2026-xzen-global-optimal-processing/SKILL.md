---
name: xzen-global-optimal-processing
description: "全局最优数据处理系统 -- 多线程并行方案评估引擎，以全局最优为核心目标。三大原则：全局最优目标(多线程并行计算所有方案+流程量化)、精细优化机制(异常检测自动触发)、利益权衡维度(多方利益最大化)。支持8工作线程并行评估所有可能任务组合。"
version: "1.0.0"
author: "XZEN"
created: "2026-04-21"
type: "optimization"
tags: ["parallel", "optimization", "quantization", "decision"]
entry: "scripts/global_optimal_data_processing_system.py"
---

# XZEN 全局最优数据处理系统 Skill

## 三大核心原则

### 1: 全局最优目标
- 多线程并行计算所有可能方案
- 搭配流程量化处理
- 目标：任务准确性提升45%，系统损耗降低43%

### 2: 精细优化机制
- 运行中检测异常数据
- 单一任务偏差时立即触发精细优化
- 实时调整执行策略

### 3: 利益权衡维度
- 所有任务分配纳入利益权衡
- 优先选择多方利益最大化组合
- 资源调度兼顾效率与公平

## 核心组件

### ParallelSolutionEvaluator
- 8工作线程并行评估
- 生成所有可能任务顺序组合
- 考虑任务依赖关系
- 输出按全局目标得分排序

### ProcessQuantizationHandler
- 将任务流程量化
- 分配优先级权重
- 监控执行质量

## 文件结构

- `scripts/global_optimal_data_processing_system.py` -- 主系统(47KB)
- `scripts/GLOBAL_OPTIMAL_SYSTEM_REPORT.md` -- 系统报告
- `scripts/global_optimal_system_summary.json` -- 执行摘要

## 与流程量化框架的关系

全局最优系统是xzen-process-quantization-workflow的扩展与升华 -- 在基础流程量化之上增加了多线程并行评估和全局优化策略。
