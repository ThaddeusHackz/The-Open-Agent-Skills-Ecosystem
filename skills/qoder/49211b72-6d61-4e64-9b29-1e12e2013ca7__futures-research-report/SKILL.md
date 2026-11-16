---
name: futures-research-report
description: 生成国内商品期货主力连续合约的标准化研究报告（PDF）。覆盖行情回顾、技术分析、基本面、资金面、市场情绪、操作建议六大维度，含专业图表与数据表格。自包含纯Python指标引擎，数据源用新浪财经稳定接口。当用户要求生成期货研报、商品期货分析报告、沪金/沪银/沪铜/螺纹钢/原油等期货品种研究报告，或需要期货行情技术分析+持仓量分析+PDF报告时使用。邮件发送请配合 agently-mail 技能。
---

# 商品期货研究报告生成

为国内商品期货主力连续合约生成机构级标准化研报（PDF）。数据驱动章节自动生成，
基本面/操作建议等需领域判断的章节由 Agent 撰写叙述覆盖，缺省时用数据推导的通用研判兜底。

## 依赖

首次使用前安装（仅需一次）：

```bash
pip3 install matplotlib reportlab numpy
```

可选：`pip3 install pypdf`（供 run_all.py 自动校验 PDF 页数与文本；缺省跳过校验）。

中文字体自动探测（macOS/Linux/Windows 常见 CJK 字体），无需手动配置；也可用 `--font`
参数手动指定字体文件（TTF/TTC），缺字体时错误信息内含各平台安装指引。

## 工作流

复制以下清单并跟踪进度：

```
研报生成进度：
- [ ] 1. 确认品种与参数（不明确时用 AskUserQuestion 询问）
- [ ] 2. 获取数据 fetch_futures.py
- [ ] 3. 计算分析 analyze.py
- [ ] 4. 撰写叙述 narrative.json（基本面/操作建议/结论）
- [ ] 5. 生成图表 make_charts.py
- [ ] 6. 生成 PDF build_report.py
- [ ] 7. 校验 PDF（页数 + 文本提取）
- [ ] 8. （可选）交付/邮件发送
```

**第 1 步：确认参数。** 关键参数：品种代码与中文名（见 [reference/symbols.md](reference/symbols.md)）、
分析窗口（默认近3个月）、关联品种（用于相关性）、输出格式。用户未明确时，用 AskUserQuestion 询问
品种、时间窗口、是否需要邮件发送。所有脚本在**同一个工作目录**下运行（数据文件用相对路径）。

**第 2 步：获取数据。**

```bash
python scripts/fetch_futures.py AU0 --name 沪金主连 --days 130 \
    --extra AG0:沪银主连,SC0:原油主连 --out futures_data.json
```

`--days 130` 约覆盖3个月（含60日均线所需余量）。`--extra` 用于相关性分析，格式 `代码:名称`，逗号分隔。

**第 3 步：计算分析。**

```bash
python scripts/analyze.py --data futures_data.json --symbol AU0 --out analysis.json
```

输出当前快照、全部技术指标、近1月/近3月区间统计、量仓趋势、相关性、支撑阻力、近10日明细。

**第 4 步：撰写叙述（关键增值环节）。** 脚本无法获知品种的领域基本面（如黄金的美元/实际利率逻辑、
铜的供需/库存逻辑）。Agent 应基于 analysis.json 的数据 + 品种领域知识，撰写 narrative.json：

```json
{
  "rating": "中性偏谨慎",
  "rating_short": "震荡企稳（反弹待确认）",
  "rating_mid": "空头格局未改",
  "summary_points": ["<font color='#1a3a5c'>中期趋势：</font>……", "……"],
  "fundamental": [
    {"h": "3.1 国际金价联动", "p": "沪金以国际金价为定价锚……"},
    {"h": "3.2 美元指数", "p": "……"}
  ],
  "sentiment_extra": "……（可选，市场情绪补充）",
  "strategy": ["<font color='#1a3a5c'>区间策略：</font>……", "……"],
  "risks": ["<font color='#1a3a5c'>仓位管理：</font>……", "……"],
  "conclusion": ["综合……，……", "操作层面……"],
  "disclaimer_extra": "3. 本次XX数据不完整……（可选，数据局限说明）"
}
```

字段均可选；缺省的章节由 build_report.py 用数据自动推导的通用内容兜底。
`summary_points`/`strategy`/`risks` 为数组（每项一个要点）；`fundamental` 为 `{h,p}` 数组。
要点中的小标题建议用 `<font color='#1a3a5c'>标签：</font>` 着色（避免 `<b>`，无独立粗体字重）。
**叙述必须与 analysis.json 的真实数据一致**，不得编造数字。

**第 5 步：生成图表。**

```bash
python scripts/make_charts.py --data futures_data.json --symbol AU0 \
    --name 沪金主连 --outdir ./charts --window 63
```

生成 `chart_price.png`（K线+均线+布林带+成交量+持仓量）、`chart_macd.png`、`chart_rsi_kdj.png`。

**第 6 步：生成 PDF。**

```bash
python scripts/build_report.py --analysis analysis.json --charts ./charts \
    --name 沪金主连 --symbol AU0 --narrative narrative.json \
    --out 沪金主连研究报告.pdf
```

`--narrative` 可省略（用通用兜底）。输出含封面、摘要、六大章节、结论、免责声明的完整研报。

**第 7 步：校验。**

```bash
python3 -c "import pypdf; r=pypdf.PdfReader('沪金主连研究报告.pdf'); print('页数:', len(r.pages)); print(r.pages[2].extract_text()[:150])"
```

确认页数 ≥ 10、中文提取无乱码、关键数据正确。

**第 8 步：交付。** 将 PDF 复制到用户输出目录并提供 file:// 链接。如需邮件发送，调用 agently-mail
技能（发送已设为自动确认、无需停顿，附件用相对路径，须在附件所在目录运行）。

### 快速路径：一键生成

常规场景（无需人工撰写叙述、接受通用研判兜底）可跳过第 2–6 步，一条命令完成
fetch → analyze → charts → build → verify：

```bash
python scripts/run_all.py AU0 --name 沪金主连 --extra AG0:沪银主连
```

参数与各子脚本一致（`--days` `--extra` `--window` `--out` `--font` `--narrative`）。
输出 `futures_data.json`、`analysis.json`、`charts/` 与 PDF，并自动校验页数 ≥10 与
中文文本（需 pypdf，缺省跳过并提示）。跑通后如需补充基本面/操作建议叙述，写
narrative.json 再只重跑 build_report.py 覆盖叙述章节即可。

## 脚本一览

| 脚本 | 作用 | 依赖 |
|------|------|------|
| `scripts/indicators.py` | 纯Python技术指标库（MA/MACD/RSI/BOLL/KDJ/WR/CCI/MFI/ATR/ADX/OBV），可独立调用 | 标准库 |
| `scripts/fetch_futures.py` | 新浪 InnerFutures K线获取（含成交量v+持仓量p），零依赖 | 标准库 |
| `scripts/analyze.py` | 区间统计/量仓趋势/相关性/支撑阻力/指标汇总 → analysis.json | indicators |
| `scripts/make_charts.py` | 3张专业图表（红涨绿跌） | matplotlib, numpy |
| `scripts/build_report.py` | reportlab 研报PDF（数据驱动+叙述覆盖） | reportlab |
| `scripts/run_all.py` | 一键生成：fetch→analyze→charts→build→verify 合并为一条命令 | 同各子脚本（pypdf 可选） |

## 数据源与坑（重要）

- **用新浪，不用东财K线**：东方财富 `push2his.eastmoney.com` K线端点对期货品种间歇性限流，
  常返回空数组或含零值残缺数据（会导致除零错误）。新浪 InnerFutures 接口稳定，且日K自带
  成交量与持仓量字段。**不要**改用 `stock-researcher` 的 `fetch_global_kline` 取期货K线。
- 新浪**外盘**服务（OuterFuturesNewService）无效，本技能仅覆盖国内期货。COMEX/WTI 等外盘数据
  需另寻数据源，或在 narrative.json 中定性说明。
- 新浪接口偶尔触发限流，`fetch_futures.py` 已内置重试（3次）；连续大量请求时建议品种间留间隔。
- 免费接口延迟约3–5秒，非交易时段返回收盘价；不同源报价口径（结算价/收盘价）可能略有出入。
- `fetch_futures.py` 会校验收盘价非零，脏数据会被拒绝并重试。

## 常见问题 FAQ

**Q1 生成 PDF 报错"未找到可用的中文字体"怎么办？**
系统缺中文字体时 build_report.py 不再直接崩溃——错误信息内含 macOS/Linux/Windows
三条安装命令；也可用 `--font /path/to/font.ttf` 直接指定任意字体文件（TTF/TTC）。
图表（make_charts.py）缺字体时不报错但中文显示为方框，同样可用 `--font` 解决。

**Q2 数据获取失败/超时怎么办？**
fetch_futures.py 已内置 3 次重试 + 脏数据（零值收盘价）校验，重试仍失败会打印具体
原因（网络/限流/代码错误）。可稍后重试，或先单独运行 `fetch_futures.py <代码>` 验证
品种代码（新浪返回 `__ERROR` 即代码有误，见 reference/symbols.md 顶部说明）。

**Q3 为什么不用东方财富的数据？**
东财 `push2his` K线端点对期货品种间歇性限流，常返回空数组或含零值残缺数据（引发
除零错误）；新浪 InnerFutures 接口稳定且日K自带成交量与持仓量字段。**不要**改用
stock-researcher 的 `fetch_global_kline` 取期货K线。

**Q4 支持外盘期货吗？**
不支持。新浪外盘服务无效，本技能仅覆盖国内期货（上期所/能源中心/郑商所/大商所/广期所
主力连续合约）。COMEX/WTI 等外盘需另寻数据源，或在 narrative.json 中定性说明。

**Q5 研报"基本面/操作建议"章节内容偏通用？**
这两章需要领域判断（如黄金的美元/实际利率逻辑、铜的供需/库存），脚本无法自动获取。
缺省时用数据推导的通用框架兜底；要专业内容，Agent 按第 4 步模板撰写 narrative.json
（`fundamental`/`strategy`/`risks`/`conclusion` 字段），再重跑 build_report.py 或
run_all.py 加 `--narrative`。

**Q6 报告页数不足 10 页？**
可能原因：未传 `--extra` 导致相关性/对比表缺失、图表生成失败（matplotlib 未装或
缺字体）、数据天数不足。先看 run_all.py 的校验输出与 stderr 警告定位。

**Q7 PDF 打开后中文乱码或方框？**
乱码：正常生成不会乱码，确认报告内置免责声明/页脚未被删除。方框：图表缺中文字体
（见 Q1），重跑 make_charts.py 或 run_all.py 并加 `--font`。

**Q8 校验必须手动跑命令吗？**
run_all.py 已内置校验（页数 + 第 3 页文本提取，需 pypdf）。单独生成 PDF 时可手动
执行第 7 步的校验命令。

**Q9 能否配合邮件发送？**
可以。交付时调用 agently-mail 技能发送（发送已设为自动确认无需停顿；附件用相对路径，
须在附件所在目录运行）。

## 报告样例预览

以下为报告版面示意（文字版），实际数据随品种与日期变化：

- **封面**：深蓝底标题条「沪金主连（AU0）市场综合研究报告」→ 金色评级表（综合评级/
  数据截至/短期趋势/中期趋势）→ 报告日期/分析引擎/数据来源 → 免责声明。
- **摘要**：核心观点 4 条（中期趋势/短期信号/当前位置/综合研判）+ 关键数据速览表
  （开高低收/量仓/MA5-60/RSI/ATR）。
- **一 行情数据回顾**：区间统计表（近1月/近3月涨跌幅·高低点·振幅）+ 量仓变化 + 近10日
  明细表 + 图1 K线主图（K线+均线+布林带+成交量+持仓量）。
- **二 技术分析**：均线系统/MACD/RSI-KDJ/布林带文字分析 + 图2图3 + 指标信号表。
- **三 基本面分析**：narrative 覆盖（推荐）或通用框架。
- **四 资金面分析**：持仓量趋势表 + 关联品种对比表。
- **五 市场情绪**：波动率 + 相关品种相关系数表。
- **六 风险提示与操作建议**：支撑阻力表 + 区间/突破/趋势三策略 + 风控要点。
- **结论**：评级框（综合评级/操作倾向/短中期观点/核心支撑阻力）。
- **附 免责声明与数据说明**。

全文约 11–13 页 A4，每页含页眉（报告名+日期）与页脚（免责声明+页码）。红涨绿跌
配色，机构风格（深蓝 #1a3a5c + 金色 #b8860b）。

## 研报结构（build_report 输出）

封面（标题+评级表+元数据+免责声明）→ 摘要（核心观点+KPI+速览表）→
一 行情数据回顾（区间统计+量仓+近10日明细+图1）→ 二 技术分析（均线/MACD/RSI-KDJ/布林+图2图3+指标表）→
三 基本面分析（narrative覆盖或通用框架）→ 四 资金面分析（持仓量+多空+关联品种）→
五 市场情绪（波动率+相关性）→ 六 风险提示与操作建议（支撑阻力表+策略+风控）→
结论（评级框）→ 免责声明与数据说明。每页含页眉（报告名+日期）页脚（免责声明+页码）。

## 免责声明

本技能生成的报告仅供研究参考，不构成投资建议。期货交易高杠杆、高风险，投资者据此操作风险自担。
生成报告时必须保留报告内置的免责声明与数据说明章节，不得删除。
