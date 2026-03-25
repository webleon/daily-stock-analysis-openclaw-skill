# 安装指南

## 系统要求

- Python 3.9+
- pip 20.0+
- Git

## 快速安装

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/daily-stock-analysis-openclaw-skill.git
cd daily-stock-analysis-openclaw-skill
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 验证安装

```bash
python -m scripts.validate_config
```

如果显示"✅ 所有配置文件验证通过"，则安装成功。

## 配置

### 1. 配置数据源

编辑 `config/data_sources.yaml`：

```yaml
data_sources:
  - name: akshare
    enabled: true
    config:
      # AkShare 配置
  - name: tushare
    enabled: true
    config:
      # Tushare 配置
```

### 2. 配置 Agent

编辑 `config/agents.yaml`：

```yaml
agents:
  - name: analysis_agent
    enabled: true
    config:
      model: qwen3.5-plus
      max_tokens: 4096
```

### 3. 配置 OpenClaw

编辑 `SKILL.md`：

```yaml
---
name: "stock_analyzer"
description: "股票分析技能"
---
```

## 验证安装

### 运行测试

```bash
pip install pytest pytest-cov
pytest tests/ -v
```

### 运行示例

```bash
python -m scripts.generate_report AAPL
```

## 故障排查

### 常见问题

#### 1. 依赖安装失败

```bash
# 升级 pip
pip install --upgrade pip

# 清除缓存重新安装
pip cache purge
pip install -r requirements.txt
```

#### 2. 配置验证失败

```bash
# 检查配置文件格式
python -m scripts.validate_config

# 检查 YAML 语法
python -c "import yaml; yaml.safe_load(open('config/agents.yaml'))"
```

#### 3. 数据获取失败

```bash
# 检查网络连接
ping akshare.akshare.xyz

# 检查 API 密钥
echo $TUSHARE_TOKEN
```

## 下一步

- [用户指南](README.md) - 学习如何使用
- [API 参考](../api_reference/README.md) - 查看 API 文档
- [开发者指南](../developer_guide/README.md) - 参与开发
