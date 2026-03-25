# 开发者指南

## 目录结构

```
├── src/                       # 源代码
│   ├── openclaw/              # OpenClaw 适配层
│   ├── agents/                # 多 Agent 编排
│   ├── plugins/               # 插件基类
│   └── core/                  # 原项目核心功能
├── config/                    # 配置文件
├── plugins/                   # 自定义插件
├── tests/                     # 测试代码
└── docs/                      # 文档
```

## 开发环境搭建

### 1. 克隆仓库

```bash
git clone https://github.com/your-username/daily-stock-analysis-openclaw-skill.git
cd daily-stock-analysis-openclaw-skill
```

### 2. 安装开发依赖

```bash
pip install -r requirements.txt
pip install pytest pytest-cov pylint black
```

### 3. 配置预提交钩子

```bash
# 创建 .pre-commit-config.yaml
pre-commit install
```

## 代码规范

### 1. 代码风格

遵循 PEP 8 规范，使用 Black 格式化：

```bash
black src/ tests/
```

### 2. 代码检查

```bash
pylint src/ tests/
```

### 3. 类型提示

使用类型提示：

```python
from typing import Dict, List, Optional

def analyze(stock_code: str, data: Dict) -> Dict:
    pass
```

## 测试

### 1. 运行测试

```bash
pytest tests/ -v
```

### 2. 覆盖率

```bash
pytest tests/ -v --cov=src --cov-report=html
```

### 3. 编写测试

```python
# tests/unit/test_example.py
import pytest

def test_example():
    assert 1 + 1 == 2
```

## 提交代码

### 1. 提交信息规范

```
feat: 添加新功能
fix: 修复 Bug
docs: 更新文档
style: 代码格式化
refactor: 重构代码
test: 添加测试
chore: 构建/工具链
```

### 2. Pull Request

1. Fork 仓库
2. 创建分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 开启 Pull Request

## 架构设计

### 核心组件

1. **OpenClaw 适配层** (`src/openclaw/`)
   - API 版本检测
   - API 适配器
   - tool 注册

2. **多 Agent 编排** (`src/agents/`)
   - Agent 基类
   - 分析 Agent
   - 调度 Agent
   - 报告 Agent

3. **插件系统** (`src/plugins/`)
   - 插件基类
   - 自定义 Agent
   - 自定义数据源
   - 自定义模板

4. **核心功能** (`src/core/`)
   - 数据获取
   - 分析引擎
   - 报告生成
   - 工具函数

## 下一步

- [API 参考](../api_reference/README.md) - 查看 API 文档
- [用户指南](../user_guide/README.md) - 学习如何使用
