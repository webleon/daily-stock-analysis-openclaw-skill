# 📖 完整指南 / Complete Guide

A 股自选股智能分析系统的完整配置与使用指南。

Complete configuration and usage guide for the AI Stock Analysis System.

---

## 🚀 目录 / Table of Contents

1. [快速开始](#-快速开始--quick-start)
2. [部署指南](#-部署指南--deployment)
3. [LLM 配置](#-llm-配置--llm-configuration)
4. [环境变量](#-环境变量--environment-variables)
5. [常见问题](#-常见问题--faq)
6. [多 Agent 编排](#-多-agent-编排--multi-agent-orchestration)
7. [贡献指南](#-贡献指南--contributing)

---

## 🎯 快速开始 / Quick Start

### 方式 1: GitHub Actions (推荐)

```bash
# 1. Fork 仓库
# 2. 配置 Secrets
# 3. 启用 Actions
# 4. 手动测试运行
```

**最小配置**:
- AI 模型 API Key (AIHUBMIX_KEY 或 GEMINI_API_KEY)
- 通知渠道 (至少一个 Webhook)
- 股票列表 (STOCK_LIST)

### 方式 2: 本地运行

```bash
# 1. 克隆项目
git clone https://github.com/ZhuLinsen/daily_stock_analysis.git
cd daily_stock_analysis

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置环境变量
cp .env.example .env
# 编辑 .env 填写 API Keys

# 4. 运行分析
python main.py
```

---

## 🐳 部署指南 / Deployment

### Docker Compose (推荐)

```bash
# 1. 配置环境变量
cp .env.example .env

# 2. 启动服务
docker-compose up -d

# 3. 查看日志
docker-compose logs -f
```

### 直接部署

```bash
# 1. 创建虚拟环境
python -m venv venv
source venv/bin/activate

# 2. 安装依赖
pip install -r requirements.txt

# 3. 配置并运行
cp .env.example .env
python main.py
```

### 后台运行 (systemd)

```ini
[Unit]
Description=Stock Analysis System
After=network.target

[Service]
Type=simple
User=your_user
WorkingDirectory=/path/to/project
ExecStart=/path/to/venv/bin/python main.py
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 🤖 LLM 配置 / LLM Configuration

### 快速配置

**AIHubMix (推荐国内)**:
```bash
export AIHUBMIX_KEY=sk-xxxxx
```

**Gemini (推荐海外)**:
```bash
export GEMINI_API_KEY=xxxxx
```

**OpenAI 兼容**:
```bash
export OPENAI_API_KEY=xxxxx
export OPENAI_BASE_URL=https://api.deepseek.com/v1
```

### 三层配置体系

1. **环境变量** (最简单)
   ```bash
   export GEMINI_API_KEY=xxxxx
   ```

2. **.env 文件** (推荐)
   ```bash
   GEMINI_API_KEY=xxxxx
   LLM_MODEL=gemini-pro
   ```

3. **LiteLLM 配置** (高级)
   ```yaml
   model_list:
     - model_name: gemini-pro
       litellm_params:
         model: gemini/gemini-pro
   ```

### 常用模型

| 服务商 | 模型 | 配置 |
|--------|------|------|
| Google | gemini-pro | `GEMINI_API_KEY` |
| OpenAI | gpt-4o | `OPENAI_API_KEY` |
| DeepSeek | deepseek-chat | `OPENAI_API_KEY` + `BASE_URL` |
| Ollama | llama2 | `OLLAMA_API_BASE` |

---

## 📋 环境变量 / Environment Variables

### AI 模型配置

| 变量名 | 说明 | 必填 |
|--------|------|:----:|
| `AIHUBMIX_KEY` | AIHubMix API Key (一 Key 多模型) | 可选* |
| `GEMINI_API_KEY` | Google Gemini API Key | 可选* |
| `OPENAI_API_KEY` | OpenAI 兼容 API Key | 可选* |
| `OPENAI_BASE_URL` | OpenAI 兼容 API 地址 | 可选 |
| `ANTHROPIC_API_KEY` | Claude API Key | 可选 |

> *注：至少配置一个 API Key

### 通知渠道

| 变量名 | 说明 |
|--------|------|
| `WECHAT_WEBHOOK_URL` | 企业微信 Webhook |
| `FEISHU_WEBHOOK_URL` | 飞书 Webhook |
| `TELEGRAM_BOT_TOKEN` | Telegram Bot Token |
| `TELEGRAM_CHAT_ID` | Telegram Chat ID |
| `DISCORD_WEBHOOK_URL` | Discord Webhook |
| `EMAIL_SENDER` | 发件人邮箱 |
| `EMAIL_PASSWORD` | 邮箱授权码 |

> 至少配置一个通知渠道

### 核心配置

| 变量名 | 说明 | 默认值 |
|--------|------|--------|
| `STOCK_LIST` | 自选股代码列表 | 必填 |
| `TAVILY_API_KEYS` | Tavily 搜索 API | 推荐 |
| `REPORT_TYPE` | 报告类型 (simple/full/brief) | full |
| `SINGLE_STOCK_NOTIFY` | 单股推送模式 | false |

---

## ❓ 常见问题 / FAQ

### 数据相关

**Q: 美股价格显示不正确？**

A: 确保使用 YFinance 数据源，检查网络连接。

**Q: A 股数据获取失败？**

A: 
1. 检查网络连接
2. 等待 5 分钟后重试
3. 配置 Tushare 作为备用

---

### AI 模型相关

**Q: Gemini API 调用失败？**

A:
1. 检查 API Key 是否正确
2. 确认已开启科学上网
3. 考虑使用 AIHubMix 等中转服务

**Q: 分析报告生成慢？**

A:
1. 使用更快的模型 (gemini-pro)
2. 减少新闻搜索数量
3. 启用缓存

---

### 部署相关

**Q: Docker 容器启动失败？**

A: 检查 `docker-compose logs`，常见问题：
1. 端口被占用
2. 环境变量未配置
3. 镜像下载失败

**Q: 如何后台运行？**

A:
```bash
# 使用 nohup
nohup python main.py > output.log 2>&1 &

# 或使用 systemd
sudo systemctl start stock-analysis
```

---

### 功能相关

**Q: 如何添加自选股？**

A: 编辑 `.env` 文件：
```bash
STOCK_LIST=600519,AAPL,hk00700,TSLA
```

**Q: 如何推送到 Telegram？**

A:
1. 创建 Telegram Bot (@BotFather)
2. 获取 Bot Token
3. 配置：
```bash
TELEGRAM_BOT_TOKEN=your_token
TELEGRAM_CHAT_ID=your_chat_id
```

---

## 🤖 多 Agent 编排 / Multi-Agent Orchestration

### 概述

多 Agent 编排器 (`MultiAgentOrchestrator`) 提供完整的 Agent 生命周期管理：

- ✅ Agent 状态监控
- ✅ 错误恢复机制
- ✅ 日志记录
- ✅ 超时处理

### 使用示例

```python
from core.orchestrator import MultiAgentOrchestrator

# 创建协调器
orchestrator = MultiAgentOrchestrator("600519")

# 添加 Agent 结果
orchestrator.add_result(AgentResult(
    agent_type="technical",
    conclusion="看多",
    score=75,
    confidence=0.8
))

# 交叉验证
conflicts = orchestrator.cross_validate()

# 综合结果
synthesis = orchestrator.resolve_conflicts(strategy="weighted")
```

### Agent 类型

| 类型 | 职责 |
|------|------|
| technical | 技术面分析 |
| fundamental | 基本面分析 |
| sentiment | 舆情面分析 |
| risk | 风险评估 |

---

## 🤝 贡献指南 / Contributing

### 报告 Bug

1. 搜索 [Issues](https://github.com/ZhuLinsen/daily_stock_analysis/issues)
2. 使用 Bug Report 模板创建新 Issue
3. 提供详细复现步骤

### 功能建议

1. 搜索 Issues 确认建议未被提出
2. 使用 Feature Request 模板
3. 描述使用场景和期望

### 提交代码

```bash
# 1. Fork 仓库
# 2. 创建分支
git checkout -b feature/your-feature

# 3. 提交改动
git commit -m 'feat: add some feature'

# 4. 推送
git push origin feature/your-feature

# 5. 创建 Pull Request
```

### Commit 规范

使用 [Conventional Commits](https://www.conventionalcommits.org/):

```
feat: 新功能
fix: 修复 bug
docs: 文档更新
style: 代码格式
refactor: 重构
test: 测试
chore: 构建/工具
```

---

## 📚 更多资源 / More Resources

- [更新日志](CHANGELOG.md) - Version history
- [GitHub Issues](https://github.com/ZhuLinsen/daily_stock_analysis/issues) - Bug reports
- [讨论区](https://github.com/ZhuLinsen/daily_stock_analysis/discussions) - Q&A

---

**最后更新**: 2026-03-28
