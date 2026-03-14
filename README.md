# Daily Stock Analysis for OpenClaw

🤖 **LLM 驱动的智能股票分析系统**，支持 A 股/港股/美股自选股深度分析，每日自动推送「决策仪表盘」到 Telegram/邮件。

[![GitHub stars](https://img.shields.io/github/stars/webleon/daily-stock-analysis-openclaw-skill?style=social)](https://github.com/webleon/daily-stock-analysis-openclaw-skill/stargazers)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)
[![Python 3.10+](https://img.shields.io/badge/python-3.10+-blue.svg)](https://www.python.org/downloads/)

> 基于 AI 大模型的股票智能分析，每日自动推送决策仪表盘

简体中文 | [English](docs/README_EN.md)

---

## ✨ 核心功能

| 功能 | 说明 |
|------|------|
| **AI 决策仪表盘** | 一句话核心结论 + 精确买卖点位 + 操作检查清单 |
| **多维度分析** | 技术面（MA/MACD/RSI）+ 筹码分布 + 舆情情报 |
| **全球市场** | 支持 A 股、港股、美股及美股指数 |
| **策略系统** | 内置 A 股「三段式复盘」与美股「Regime Strategy」 |
| **大盘复盘** | 每日市场概览、板块涨跌榜 |
| **多渠道推送** | Telegram、邮件、企业微信、飞书等 |
| **定时运行** | OpenClaw Cron Job 自动执行 |

---

## 🚀 快速开始

### 方式一：OpenClaw Skill（推荐）

#### 1. 安装 Skill

```bash
cd ~/.openclaw/workspace/skills
git clone https://github.com/webleon/daily-stock-analysis-openclaw-skill.git
cd daily-stock-analysis-openclaw-skill
pip3 install -r requirements.txt
```

#### 2. 配置环境变量

```bash
cp .env.example .env
vim .env
```

**必填配置：**
```bash
# === 股票列表 ===
STOCK_LIST=600519,hk00700,AAPL,TSLA,NVDA

# === AI 模型（至少配置一个）===
# 推荐：Gemini（免费）
GEMINI_API_KEY=your_gemini_key_here

# 或：通义千问
DASHSCOPE_API_KEY=your_dashscope_key_here

# 或：DeepSeek
DEEPSEEK_API_KEY=your_deepseek_key_here
```

**可选配置：**
```bash
# === 通知渠道（至少配置一个）===
# Telegram
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id

# 邮件
EMAIL_SENDER=your_email@qq.com
EMAIL_PASSWORD=your_email_auth_code
EMAIL_RECEIVERS=receiver@example.com

# 企业微信
WECHAT_WEBHOOK_URL=https://qyapi.weixin.qq.com/cgi-bin/webhook/send?key=xxx

# 飞书
FEISHU_WEBHOOK_URL=https://open.feishu.cn/open-apis/bot/v2/hook/xxx

# === 交易参数 ===
# 乖离率阈值（%），超过此值提示不追高
BIAS_THRESHOLD=5.0

# 新闻最大时效（天）
NEWS_MAX_AGE_DAYS=3
```

#### 3. 测试运行

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

#### 4. 配置定时任务

编辑 `~/.openclaw/cron/jobs.json`：

```json
{
  "daily-stock-analysis": {
    "schedule": "0 18 * * 1-5",
    "command": "~/.openclaw/workspace/skills/daily-stock-analysis-openclaw-skill/run.sh",
    "timeout": 1800,
    "enabled": true
  }
}
```

**执行时间：** 每个工作日 18:00（北京时间）

---

### 方式二：OpenClaw 对话

在 OpenClaw 中直接对话：

```
"帮我分析一下 NVDA"
"今天市场怎么样"
"推荐几只值得关注的股票"
"分析一下 600519 贵州茅台"
```

---

## 📊 推送效果

### 决策仪表盘示例

```
📊 决策仪表盘 - AAPL

🎯 核心结论
一句话：多头排列 + 低乖离率，最佳买点出现
信号类型：🟢 买入信号
紧急程度：立即行动

📈 数据视角
趋势状态：多头排列（MA5>MA10>MA20）
现价：$178.72
MA5: $177.50 (乖离 +0.69%)
MA10: $175.20 (乖离 +2.01%)
MA20: $172.30 (乖离 +3.73%)
支撑位：$177.50
压力位：$182.50

💰 狙击点位
理想买入点：$177.50（MA5 附近，乖离率<2%）
次优买入点：$175.20（MA10 附近，乖离率<5%）
止损位：$172.30（跌破 MA20）
目标位：$182.50（前高压力位）

✅ 检查清单
✅ 多头排列：MA5>MA10>MA20
✅ 乖离率合理：+0.69% < 2%
✅ 缩量回调：量比 0.72
✅ MA5 支撑有效
✅ MACD 金叉
⚠️ RSI 中性：52.3

💡 操作建议
空仓者：建议立即建仓 3 成仓位
持仓者：继续持有，以 MA5 为防守位
```

---

## 🎯 核心交易理念

### 1. 严进策略（不追高）
- **绝对不追高**：当股价偏离 MA5 超过 5% 时，坚决不买入
- 乖离率 < 2%：最佳买点区间
- 乖离率 2-5%：可小仓介入
- 乖离率 > 5%：严禁追高！直接判定为"观望"

### 2. 趋势交易（顺势而为）
- **多头排列必须条件**：MA5 > MA10 > MA20
- 只做多头排列的股票，空头排列坚决不碰
- 均线发散上行优于均线粘合

### 3. 效率优先（筹码结构）
- 关注筹码集中度：90% 集中度 < 15% 表示筹码集中
- 获利比例分析：70-90% 获利盘时需警惕获利回吐
- 平均成本与现价关系：现价高于平均成本 5-15% 为健康

### 4. 买点偏好（回踩支撑）
- **最佳买点**：缩量回踩 MA5 获得支撑
- **次优买点**：回踩 MA10 获得支撑
- **观望情况**：跌破 MA20 时观望

### 5. 风险排查重点
- 减持公告、业绩预亏、监管处罚、行业政策利空、大额解禁

---

## 📈 技术指标说明

### 均线系统
- **MA5**：5 日均线，短期趋势
- **MA10**：10 日均线，中期趋势
- **MA20**：20 日均线，中期支撑/压力
- **MA60**：60 日均线，长期趋势

### MACD 指标
- **金叉**：DIF 上穿 DEA，买入信号
- **死叉**：DIF 下穿 DEA，卖出信号
- **零轴上金叉**：最强买入信号
- **零轴下死叉**：最强卖出信号

### RSI 指标
- **RSI > 70**：超买，警惕回调
- **RSI < 30**：超卖，可能反弹
- **RSI 50**：中性

### 乖离率（BIAS）
- **公式**：(现价 - MA5) / MA5 × 100%
- **< 2%**：最佳买点
- **2-5%**：可小仓介入
- **> 5%**：严禁追高

---

## 🛠️ 技术栈

| 类型 | 技术 |
|------|------|
| **核心语言** | Python 3.10+ |
| **AI 框架** | LiteLLM（支持多模型） |
| **数据源** | AkShare、Tushare、YFinance |
| **技术指标** | 自研 StockAnalyzer |
| **推送渠道** | Telegram、邮件、企业微信、飞书 |

---

## 📦 数据源

| 数据源 | 市场 | 特点 |
|--------|------|------|
| **AkShare** | A 股/港股 | 免费、数据全、稳定 |
| **Tushare** | A 股 | 需 Token、数据质量高 |
| **YFinance** | 美股/港股 | 免费、雅虎数据 |
| **Efinance** | A 股 | 东方财富数据 |
| **Pytdx** | A 股 | 通达信行情，实时 |
| **Baostock** | A 股 | 证券宝，免费 |

---

## ⚙️ 高级配置

### 多模型配置

支持同时配置多个 AI 模型，自动故障切换：

```bash
# 主模型
LITELLM_MODEL=gemini/gemini-2.5-flash

# 备用模型
LITELLM_FALLBACK_MODELS=dashscope/qwen-plus,deepseek/deepseek-chat
```

### 自定义策略

激活额外的交易策略：

```bash
# 激活策略（逗号分隔）
AGENT_SKILLS=chan_theory,wave_theory,box_oscillation

# 或激活所有策略
AGENT_SKILLS=all
```

**内置策略：**
- `chan_theory` - 缠论分析
- `wave_theory` - 波浪理论
- `box_oscillation` - 箱体震荡
- `dragon_head` - 龙头战法
- `one_yang_three_yin` - 一阳穿三阴
- `volume_breakout` - 放量突破
- `shrink_pullback` - 缩量回踩
- `bottom_volume` - 地量见底
- `emotion_cycle` - 情绪周期
- `ma_golden_cross` - 均线金叉
- `bull_trend` - 多头趋势

---

## 🔧 故障排查

### 常见问题

#### 1. 数据获取失败
```bash
# 检查网络连接
ping akshare.eastmoney.com

# 检查数据源配置
vim .env
# 确保 STOCK_LIST 格式正确
```

#### 2. AI 模型不可用
```bash
# 检查 API Key
echo $GEMINI_API_KEY

# 测试 API 连接
curl -X POST https://generativelanguage.googleapis.com/v1beta/models/gemini-2.5-flash:generateContent?key=$GEMINI_API_KEY
```

#### 3. 推送失败
```bash
# 检查 Telegram Bot Token
curl https://api.telegram.org/bot$TELEGRAM_BOT_TOKEN/getMe

# 检查邮件配置
# 确保使用邮箱授权码，不是登录密码
```

---

## 📝 更新日志

### v2026.3.14
- ✅ 完整功能实现
- ✅ 所有数据源集成
- ✅ 多渠道推送
- ✅ AI 决策仪表盘

---

## 🤝 贡献

欢迎提交 Issue 和 Pull Request！

---

## 📄 许可证

MIT License

---

## 🙏 致谢

感谢以下开源项目：
- [AkShare](https://github.com/akfamily/akshare)
- [Tushare](https://tushare.pro/)
- [YFinance](https://github.com/ranaroussi/yfinance)
- [LiteLLM](https://github.com/BerriAI/litellm)

---

**⚠️ 免责声明：本项目仅供参考，不构成投资建议。股市有风险，投资需谨慎。**
