# 安装指南

## 快速安装（5 分钟）

### 1. 安装 Python 依赖

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
# 自选股（逗号分隔）
STOCK_LIST=600519,hk00700,AAPL,TSLA,NVDA

# AI 模型（至少配置一个）
GEMINI_API_KEY=your_key_here

# 可选：通知渠道
TELEGRAM_BOT_TOKEN=your_bot_token
TELEGRAM_CHAT_ID=your_chat_id
```

### 3. 测试运行

```bash
# 分析单只股票
./run.sh AAPL

# 大盘复盘
./run.sh --market-review
```

---

## 配置 OpenClaw Cron Job

### 编辑 Cron 配置

```bash
vim ~/.openclaw/cron/jobs.json
```

### 添加任务

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

## 获取 API Key

### LLM 配置（已配置 ✅）

**当前配置：** 使用 OpenClaw 现有的 Bailian（通义千问）配置

```bash
OPENAI_API_KEY=sk-sp-0f31fbee0fd044e8941c1714f447433e
OPENAI_BASE_URL=https://coding.dashscope.aliyuncs.com/v1
OPENAI_MODEL=qwen3.5-plus
```

**如需更换模型：**

1. **Volces（火山方舟）**
   ```bash
   OPENAI_API_KEY=84915a62-b2c0-4cf8-b00c-3d1f7fa5dc27
   OPENAI_BASE_URL=https://ark.cn-beijing.volces.com/api/coding/v3
   OPENAI_MODEL=ark-code-latest
   ```

2. **Gemini**
   ```bash
   OPENAI_API_KEY=your_gemini_key
   OPENAI_BASE_URL=https://generativelanguage.googleapis.com/v1beta/openai/
   OPENAI_MODEL=gemini-2.0-flash
   ```

### Tavily 搜索（可选）

1. 访问：https://tavily.com/
2. 注册并获取 API Key
3. 配置到 `.env`：
   ```bash
   TAVILY_API_KEY=your_key_here
   ```

### Telegram Bot（可选）

1. 在 Telegram 搜索 @BotFather
2. 发送 `/newbot` 创建机器人
3. 复制 Token 到 `.env`：
   ```bash
   TELEGRAM_BOT_TOKEN=your_bot_token
   TELEGRAM_CHAT_ID=your_chat_id
   ```

---

## 故障排查

### 依赖安装失败

```bash
# 使用国内镜像
pip3 install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 数据获取失败

```bash
# 测试 AkShare
python3 -c "import akshare as ak; print(ak.stock_zh_a_spot_em())"

# 测试 YFinance
python3 -c "import yfinance as yf; print(yf.Ticker('AAPL').info)"
```

### LLM 调用失败

```bash
# 测试 Gemini
python3 -c "
import litellm
response = litellm.completion(
    model='gemini/gemini-pro',
    messages=[{'role': 'user', 'content': 'test'}]
)
print(response)
"
```

---

## 下一步

- ✅ 测试单股分析：`./run.sh AAPL`
- ✅ 测试大盘复盘：`./run.sh --market-review`
- ✅ 配置定时任务：编辑 `~/.openclaw/cron/jobs.json`
- ✅ 查看日志：`cat log/$(date +%Y-%m-%d).log`

---

## 相关文档

- [README.md](README.md) - 项目说明
- [SKILL.md](SKILL.md) - OpenClaw Skill 定义
- [原项目文档](https://github.com/ZhuLinsen/daily_stock_analysis) - 完整功能说明
