# Daily Stock Analysis for OpenClaw

LLM 驱动的智能股票分析器，支持 A 股/港股/美股。

---

## 快速开始

### 1. 安装依赖

```bash
cd ~/.openclaw/workspace/skills/daily-stock-analysis
pip3 install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
vim .env
```

**必填配置：**
```bash
# 自选股
STOCK_LIST=600519,hk00700,AAPL,TSLA

# AI 模型（至少一个）
GEMINI_API_KEY=your_key_here
```

### 3. 测试运行

```bash
# 分析单只股票
./run.sh AAPL

# 大盘复盘
./run.sh --market-review
```

---

## 功能特性

| 功能 | 说明 |
|------|------|
| **AI 决策仪表盘** | 一句话结论 + 精确买卖点位 |
| **多维度分析** | 技术面 + 筹码 + 舆情 |
| **全球市场** | A 股/港股/美股 |
| **策略系统** | A 股三段式/美股 Regime |
| **大盘复盘** | 每日市场概览 |
| **定时运行** | OpenClaw Cron Job |

---

## 使用方式

### 命令行

```bash
# 单股分析
./run.sh AAPL

# 多股分析
./run.sh AAPL,MSFT,GOOGL

# 大盘复盘
./run.sh --market-review

# 指定市场
./run.sh --market us
```

### OpenClaw 对话

- "帮我分析一下 NVDA"
- "今天市场怎么样"
- "推荐几只值得关注的股票"

---

## 定时配置

编辑 `~/.openclaw/cron/jobs.json`：

```json
{
  "daily-stock-analysis": {
    "schedule": "0 18 * * 1-5",
    "command": "~/.openclaw/workspace/skills/daily-stock-analysis/run.sh",
    "timeout": 1800,
    "enabled": true
  }
}
```

**执行时间：** 每个工作日 18:00（北京时间）

---

## 输出示例

### 单股分析

```
⚪ AAPL (Apple Inc.)

📰 重要信息速览
💭 舆情情绪：AI 服务器需求强劲
📊 业绩预期：Q1 财报超预期

🎯 操作建议：观望
📍 狙击点：175-178 USD
🛑 止损：165 USD
🎯 目标：195 USD
```

### 大盘复盘

```
🎯 2026-03-10 大盘复盘

📊 主要指数
- 上证指数：3250 (+0.85%)
- 纳斯达克：16500 (+1.2%)

📈 市场概况
上涨：3920 | 下跌：1349
```

---

## 依赖说明

### 核心依赖

- **akshare** - A 股行情（免费）
- **yfinance** - 美股/港股（免费）
- **pandas/numpy** - 数据处理
- **litellm** - LLM 统一接口

### 可选依赖

- **tavily-python** - 新闻搜索
- **tushare** - A 股数据（需 Token）

---

## 故障排查

### 数据获取失败

```bash
# 检查网络
ping akshare.akshare.xyz

# 测试数据源
python3 -c "import akshare as ak; print(ak.stock_zh_a_spot_em())"
```

### LLM 调用失败

```bash
# 检查 API Key
echo $GEMINI_API_KEY

# 测试 LLM
python3 -c "import litellm; r = litellm.completion(model='gemini/gemini-pro', messages=[{'role':'user','content':'test'}]); print(r)"
```

---

## 项目结构

```
daily-stock-analysis/
├── SKILL.md              # OpenClaw Skill 定义
├── run.sh                # 入口脚本
├── main.py               # 主调度程序
├── analyzer_service.py   # 核心分析服务
├── requirements.txt      # Python 依赖
├── .env.example          # 环境变量模板
├── src/                  # 核心逻辑
│   ├── config.py         # 配置管理
│   ├── pipeline.py       # 分析流水线
│   └── market_review.py  # 大盘复盘
├── data_provider/        # 数据源
│   ├── akshare_provider.py
│   └── yfinance_provider.py
└── strategies/           # 交易策略
    ├── a_stock_strategy.py
    └── us_stock_strategy.py
```

---

## 免责声明

⚠️ **本分析仅供参考，不构成投资建议**

股市有风险，投资需谨慎。

---

## 原项目

- GitHub: https://github.com/ZhuLinsen/daily_stock_analysis
- 作者：ZhuLinsen
