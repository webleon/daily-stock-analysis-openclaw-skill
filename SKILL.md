---
name: "daily-stock-analysis"
description: "LLM 驱动的智能股票分析器。支持 A 股/港股/美股分析、大盘复盘、买卖点位推荐。当用户想要分析股票或查看市场复盘时调用。"
user-invocable: true
metadata:
  { "openclaw": { "requires": { "bins": ["python3"], "python": ["akshare", "yfinance", "pandas", "numpy"] }, "primaryEnv": ["STOCK_LIST", "GEMINI_API_KEY", "TELEGRAM_BOT_TOKEN"] } }
---

# Daily Stock Analysis - 智能股票分析器

基于 LLM 的多市场股票智能分析系统，支持 A 股、港股、美股。

---

## 触发条件

| 场景 | 示例 |
|------|------|
| 单股分析 | "帮我分析一下 AAPL" |
| 多股分析 | "分析下茅台、腾讯、特斯拉" |
| 大盘复盘 | "今天市场怎么样" |
| 买卖建议 | "现在适合买入 NVDA 吗" |

---

## 用法

### 命令行调用

```bash
# 分析单只股票
~/.openclaw/workspace/skills/daily-stock-analysis/run.sh AAPL

# 分析多只股票
~/.openclaw/workspace/skills/daily-stock-analysis/run.sh AAPL,MSFT,GOOGL

# 大盘复盘
~/.openclaw/workspace/skills/daily-stock-analysis/run.sh --market-review

# 指定市场
~/.openclaw/workspace/skills/daily-stock-analysis/run.sh --market us
```

### 对话中调用

- "帮我深度分析一下 NVDA"
- "今天 A 股市场怎么样"
- "推荐几只值得关注的股票"

---

## 输出结构

### 单股分析结果

```json
{
  "code": "AAPL",
  "name": "Apple Inc.",
  "dashboard": {
    "core_conclusion": "观望 | 评分 65 | 看多",
    "data_perspective": {
      "trend": "MA5>MA10>MA20 多头排列",
      "position": "价格位于 52 周高位",
      "volume": "缩量回调",
      "chips": "筹码集中度 35%"
    },
    "intelligence": {
      "news": ["AI 服务器需求强劲", "Q1 财报超预期"],
      "risks": ["主力资金流出", "乖离率偏高"],
      "catalysts": ["新品发布会", "财报季"]
    },
    "battle_plan": {
      "buy_point": "175-178 USD",
      "stop_loss": "165 USD",
      "target": "195 USD",
      "position": "30% 仓位"
    }
  }
}
```

### 大盘复盘结果

```markdown
📊 主要指数
- 上证指数：3250 (+0.85%)
- 纳斯达克：16500 (+1.2%)

📈 市场概况
上涨：3920 | 下跌：1349 | 涨停：155

🔥 板块表现
领涨：互联网服务、文化传媒
领跌：保险、航空机场
```

---

## 配置

### 环境变量

| 变量 | 说明 | 必填 |
|------|------|------|
| `STOCK_LIST` | 自选股代码列表 | ✅ |
| `GEMINI_API_KEY` | Gemini API Key | ✅ |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token | 可选 |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID | 可选 |
| `TAVILY_API_KEY` | Tavily 搜索 API | 推荐 |
| `TUSHARE_TOKEN` | Tushare Pro Token | 可选 |

### 配置文件

编辑 `~/.openclaw/workspace/skills/daily-stock-analysis/.env`：

```bash
# 自选股（逗号分隔）
STOCK_LIST=600519,hk00700,AAPL,TSLA,NVDA

# AI 模型（至少配置一个）
GEMINI_API_KEY=your_key_here
# 或
OPENAI_API_KEY=your_key_here
OPENAI_BASE_URL=https://api.deepseek.com/v1
OPENAI_MODEL=deepseek-chat

# 通知渠道
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 分析参数
BIAS_THRESHOLD=5.0  # 乖离率阈值（%）
NEWS_MAX_AGE_DAYS=3  # 新闻最大时效（天）
```

---

## 分析策略

### A 股策略（三段式复盘）

1. **大盘环境** - 判断市场整体趋势
2. **板块轮动** - 识别热点板块
3. **个股精选** - 筛选多头排列股票

### 美股策略（Regime Strategy）

1. **Risk-on** - 进攻型配置（科技成长）
2. **Neutral** - 均衡配置（价值 + 成长）
3. **Risk-off** - 防守型配置（必需消费、公用事业）

---

## 交易规则

| 规则 | 说明 |
|------|------|
| **严禁追高** | 乖离率 > 5% 自动提示风险 |
| **趋势交易** | 只做 MA5 > MA10 > MA20 多头排列 |
| **精确点位** | 提供买入价、止损价、目标价 |
| **检查清单** | 每项条件标记「满足/注意/不满足」 |

---

## 定时运行

### OpenClaw Cron Job

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

## 依赖安装

```bash
cd ~/.openclaw/workspace/skills/daily-stock-analysis
pip3 install -r requirements.txt
```

### 核心依赖

- **akshare** - A 股行情数据
- **yfinance** - 美股/港股行情数据
- **pandas** - 数据处理
- **numpy** - 数值计算
- **litellm** - LLM 统一接口

---

## 示例输出

### 单股分析

```
⚪ 中钨高新 (000657)

📰 重要信息速览
💭 舆情情绪：市场关注其 AI 属性与业绩高增长
📊 业绩预期：2025 年前三季度扣非净利润 +407.52%

🚨 风险警报:
- 2 月 5 日主力资金净卖出 3.63 亿元
- 筹码集中度 35.15%，筹码分散

✨ 利好催化:
- AI 服务器 HDI 核心供应商
- 业绩大幅增长

🎯 操作建议: 观望
📍 狙击点：12.5-13.0 元
🛑 止损：11.5 元
🎯 目标：15.0 元
```

### 大盘复盘

```
🎯 2026-03-10 大盘复盘

📊 主要指数
- 上证指数：3250.12 (+0.85%)
- 深证成指：10521.36 (+1.02%)
- 创业板指：2156.78 (+1.35%)

📈 市场概况
上涨：3920 | 下跌：1349 | 涨停：155

🔥 板块表现
领涨：互联网服务、文化传媒、小金属
领跌：保险、航空机场、光伏设备
```

---

## 故障排查

### 问题：数据获取失败

**解决：**
```bash
# 检查网络连接
ping akshare.akshare.xyz

# 检查 API Key
echo $GEMINI_API_KEY

# 测试数据源
python3 -c "import akshare as ak; print(ak.stock_zh_a_spot_em())"
```

### 问题：LLM 调用失败

**解决：**
```bash
# 检查 LiteLLM 配置
cat litellm_config.yaml

# 测试 LLM 调用
python3 -c "import litellm; response = litellm.completion(model='gemini/gemini-pro', messages=[{'role': 'user', 'content': 'test'}]); print(response)"
```

---

## 相关文档

- [完整配置指南](docs/full-guide.md)
- [LLM 配置指南](docs/LLM_CONFIG_GUIDE.md)
- [策略说明](strategies/README.md)

---

## 免责声明

⚠️ **本分析仅供参考，不构成投资建议**

股市有风险，投资需谨慎。请结合自身风险承受能力和独立判断做出投资决策。
