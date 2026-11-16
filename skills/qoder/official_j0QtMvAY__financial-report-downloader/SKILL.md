---
name: financial-report
description: 财报PDF下载工具 - 支持A股（巨潮资讯网）、港股（港交所披露易）、美股（公司官网IR）。自动下载上市公司年报、季报PDF文件，验证文件完整性，标注数据来源。
version: 1.1.0
homepage: https://github.com/openclaw/financial-report
commands:
  - financial-report - 下载财报PDF
metadata:
  emoji: 📄
  requires:
    python: ">=3.8"
  features:
    - A股财报下载（巨潮资讯网）
    - 港股财报下载（港交所披露易）
    - 美股财报下载（公司IR）
    - 自动PDF验证
    - 多交易所支持
---

# Financial Report 财报PDF下载

自动下载A股、港股和美股上市公司财报PDF文件。

## 特点

- ✅ **A股支持** - 巨潮资讯网官方数据源
- ✅ **港股支持** - 港交所披露易
- ✅ **美股支持** - 公司官网投资者关系
- ✅ **自动验证** - 下载后验证PDF完整性
- ✅ **多交易所** - 支持上交所、深交所、北交所、港交所、美股
- ✅ **智能识别** - 自动识别股票代码所属市场
- ✅ **标准化命名** - 自动按规范命名文件

## 使用方法

### 命令行

```bash
# A股财报下载
financial-report 688111 2024      # 金山办公2024年报
financial-report 300442 2024      # 润泽科技2024年报
financial-report 600519 2024      # 贵州茅台2024年报

# 港股财报下载
financial-report 3690 2024 --hk   # 美团2024年报
financial-report 0700 2024 --hk   # 腾讯2024年报
financial-report 9988 2024 --hk   # 阿里巴巴2024年报

# 美股财报下载
financial-report AAPL 2024 --us   # 苹果2024年报
financial-report TSLA 2024 --us   # 特斯拉2024年报
financial-report MSTR 2024 --us   # MicroStrategy 2024年报
```

### Python调用

```python
from financial_report import (
    download_a_stock_report,
    download_hk_stock_report,
    download_us_stock_report
)

# 下载A股财报
pdf_path = download_a_stock_report('688111', 2024)

# 下载港股财报
pdf_path = download_hk_stock_report('03690', 2024)

# 下载美股财报
pdf_path = download_us_stock_report('AAPL', 2024)
```

## 支持的市场

### A股
| 交易所 | 代码特征 | 示例 |
|--------|----------|------|
| 上交所 | 6开头 | 600519.SH 贵州茅台 |
| 深交所 | 0或3开头 | 000001.SZ 平安银行 |
| 北交所 | 8或4开头 | 835305.BJ 云创数据 |

### 港股
| 代码 | 公司名称 | 市场 |
|------|----------|------|
| 03690 | 美团 | 港交所主板 |
| 00700 | 腾讯控股 | 港交所主板 |
| 09988 | 阿里巴巴 | 港交所主板 |
| 01810 | 小米集团 | 港交所主板 |
| 02318 | 中国平安 | 港交所主板 |

### 美股（预配置IR链接）
| 代码 | 公司 | IR网站 |
|------|------|--------|
| AAPL | 苹果 | investor.apple.com |
| MSFT | 微软 | microsoft.com/investor |
| GOOGL | 谷歌 | abc.xyz/investor |
| AMZN | 亚马逊 | ir.aboutamazon.com |
| META | Meta | investor.fb.com |
| TSLA | 特斯拉 | ir.tesla.com |
| NVDA | 英伟达 | investor.nvidia.com |
| BABA | 阿里巴巴 | alibabagroup.com/investor |
| MSTR | MicroStrategy | ir.microstrategy.com |

## 数据源

### A股 - 巨潮资讯网
- **官网**: http://www.cninfo.com.cn
- **数据类型**: 年报、季报、公告
- **覆盖范围**: 所有A股上市公司
- **更新频率**: 实时

### 港股 - 港交所披露易
- **官网**: https://www.hkexnews.hk
- **数据类型**: 年报、中期报告、公告
- **覆盖范围**: 所有港股上市公司
- **更新频率**: 实时

### 美股 - 公司IR网站
- **来源**: 各公司官方投资者关系网站
- **数据类型**: 10-K年报、10-Q季报、8-K公告
- **覆盖范围**: 预配置公司列表
- **更新频率**: 按公司发布

## 输出文件

下载的PDF文件保存在:
```
~/.openclaw/workspace/财报PDF/
```

文件命名规范:
```
A股: {代码}_{交易所}_{年份}年年度报告.pdf
     例: 688111_SH_2024年年度报告.pdf

港股: {代码}_HK_{年份}年年度报告.pdf
     例: 03690_HK_2024年年度报告.pdf

美股: {代码}_{年份}_10K.pdf
     例: AAPL_2024_10K.pdf
```

## 验证机制

下载完成后自动验证:
- ✅ 文件大小 > 1KB
- ✅ 文件头以 `%PDF` 开头
- ✅ 文件可正常打开

## 与其他技能配合

```bash
# 1. 下载财报PDF
financial-report 688111 2024

# 2. 使用pdfplumber提取数据（Python）
python3 -c "
import pdfplumber
with pdfplumber.open('财报PDF/688111_SH_2024年年度报告.pdf') as pdf:
    tables = pdf.pages[10].extract_tables()
    print(tables)
"

# 3. 进行价值投资分析
xiaoman-analyze 688111 SH
```

## 故障排除

### A股下载失败
```bash
# 检查股票代码是否正确
financial-report 688111 2024  # 正确
financial-report 688111.SH 2024  # 也支持

# 检查网络连接
curl -I http://www.cninfo.com.cn
```

### 港股下载失败
- 港股目前提供披露易搜索链接，需手动下载
- 或访问公司IR网站下载

### 美股下载失败
- 检查是否在支持列表中
- 访问公司IR网站手动下载
- 联系开发者添加新公司

## 更新日志

### v1.1.0 (2026-02-26)
- 添加港股支持（港交所披露易）
- 自动识别股票代码所属市场
- 添加港股公司映射

### v1.0.0 (2026-02-26)
- 初始版本
- 支持A股财报下载（巨潮资讯网）
- 支持美股财报下载（公司IR）
- 自动PDF验证
- 标准化文件命名

---

**免责声明:** 本工具仅供学习研究使用，下载的财报版权归上市公司所有。
