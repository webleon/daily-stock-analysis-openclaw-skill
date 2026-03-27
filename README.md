# Daily Stock Analysis - OpenClaw Skill

基于 OpenClaw 的股票分析技能，支持 A 股/港股/美股数据分析。

## 功能特性

- ✅ 多市场支持（A 股/港股/美股）
- ✅ 16 模块技术分析
- ✅ 6 大投资视角
- ✅ HTML/Markdown/微信报告
- ✅ 多 Agent 编排
- ✅ 自动命名规范

## 环境要求

- Python 3.9+
- 已安装核心依赖

## 安装

### 1. 安装依赖（使用主机环境）

```bash
pip3 install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，配置必要的 API Key
```

### 3. 验证安装

```bash
./run.sh --check
```

## 使用方法

### 分析单只股票

```bash
./run.sh 600519
```

### 分析多只股票

```bash
./run.sh 600519,000858,00700
```

### 市场复盘

```bash
./run.sh --market-review
```

### 深度分析（多 Agent）

```bash
# 在 OpenClaw 中
深度分析 AAPL
```

## 输出目录

报告保存在：`~/.openclaw/workspace/output/daily-stock-analysis/`

命名规范：`{YYYY-MM-DD}_{SYMBOL}[_{HHMMSS}].html`

示例：
- `2026-03-26_600519.html` - 当天第一份
- `2026-03-26_600519_143022.html` - 当天第二份

## 项目结构

```
├── core/                    # 核心模块
│   ├── data/               # 数据获取
│   ├── analysis/           # 分析模块
│   └── report/             # 报告生成
├── data_provider/          # 数据提供器
├── templates/              # Jinja2 模板
├── scripts/                # 工具脚本
├── tests/                  # 测试文件
├── output/                 # 输出目录
└── docs/                   # 文档
```

## 依赖说明

### 核心依赖

- `akshare` - A 股数据
- `yfinance` - 美股/港股数据
- `tushare` - 备用数据源
- `pyyaml` - 配置文件
- `jinja2` - 模板引擎
- `openclaw` - OpenClaw SDK

### 测试依赖

- `pytest` - 测试框架
- `pytest-cov` - 测试覆盖

## 配置说明

### 环境变量 (.env)

```bash
# 数据源 API Key
TUSHARE_TOKEN=your_token
AKSHARE_QPS=1

# OpenClaw 配置
OPENCLAW_MODEL=modelstudio/qwen3.5-plus
```

## 常见问题

### Q: 数据不可用？

A: 检查 API Key 配置和网络连接。

### Q: 报告生成失败？

A: 检查模板文件是否完整。

### Q: 如何切换模型？

A: 修改 `.env` 中的 `OPENCLAW_MODEL`。

## 文档

- [安装指南](INSTALL.md)
- [功能说明](README_FEATURES.md)
- [清理报告](CLEANUP_REPORT.md)

## 许可证

MIT License

## 更新日志

详见 [review.md](review.md)

---

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
