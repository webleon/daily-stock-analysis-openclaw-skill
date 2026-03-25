# OpenClaw sessions_spawn 集成指南

**版本**: 1.0  
**创建日期**: 2026-03-25  
**状态**: 📋 规划中

---

## 📊 API 确认

### 调用方式

`sessions_spawn` 是 OpenClaw 的**tool**，通过 tool 调用，不是 Python import。

### 调用示例

```json
{
  "tool": "sessions_spawn",
  "params": {
    "task": "请对 AAPL 进行专业技术面分析...",
    "label": "技术面分析-AAPL",
    "mode": "run"
  }
}
```

---

## 🔧 需要修改的代码

### 当前代码（模拟）

```python
def _spawn_subagent(self, task) -> str:
    """启动 subagent（当前使用模拟数据）"""
    # ❌ 这是模拟的
    return "mock_session_key"
```

### 目标代码（真实集成）

```python
def _spawn_subagent(self, task) -> str:
    """启动真实的 OpenClaw subagent"""
    # ✅ 使用 OpenClaw tool 调用
    # 注意：需要在 OpenClaw 主会话环境中调用
    pass
```

---

## 🎯 集成方案

### 方案 A: 在 OpenClaw 主会话中调用（推荐）

**适用场景**: OpenClaw agent 主会话（如 research-analyst）

**实现方式**:

```python
# 在 OpenClaw 会话的 tool 调用中
def analyze_with_multi_agent(self, stock_code: str):
    # 1. 创建编排器
    orchestrator = MultiAgentOrchestrator(stock_code)
    
    # 2. 生成任务
    tasks = orchestrator.generate_tasks()
    
    # 3. 启动 subagents（通过 tool 调用）
    subagent_sessions = []
    for task in tasks:
        # 这里需要调用 OpenClaw 的 sessions_spawn tool
        # 但 analyzer.py 是普通 Python 代码，无法直接调用 tool
        pass
    
    # 4. 等待完成并综合分析
    # ...
```

**问题**: `analyzer.py` 是普通 Python 模块，无法直接调用 OpenClaw tool。

---

### 方案 B: 使用 SKILL.md 提示词触发（可行）

**核心思路**: 在 SKILL.md 中说明多 Agent 流程，让 AI 自动调用 `sessions_spawn`。

**SKILL.md 更新**:

```markdown
## 多 Agent 深度分析模式

当用户请求"深度分析 XXX"时，按以下流程执行：

### 步骤 1: 启动 3 个专业 subagents

使用 `sessions_spawn` tool 启动 3 个并行分析：

```json
{
  "tool": "sessions_spawn",
  "params": {
    "task": "请对 AAPL 进行专业技术面分析，包括...",
    "label": "技术面分析-AAPL",
    "mode": "run"
  }
}
```

启动 3 个：
1. 技术面分析 subagent
2. 舆情面分析 subagent
3. 基本面分析 subagent

### 步骤 2: 等待所有 subagent 完成

每个 subagent 完成后会自动 announce 结果回主会话。

### 步骤 3: 综合分析

收到所有 subagent 结果后：
1. 提取各维度评分
2. 计算综合评分（35% 技术面 + 25% 舆情面 + 40% 基本面）
3. 生成决策仪表盘
4. 输出 HTML 报告
```

**优点**:
- ✅ 无需修改 Python 代码
- ✅ 利用 AI 自动调用 tool
- ✅ 符合 OpenClaw 设计模式

**缺点**:
- ❌ 依赖 AI 正确调用 tool
- ❌ 无法保证流程一致性

---

### 方案 C: 创建 OpenClaw Skill 入口（最佳）

**核心思路**: 创建专门的 OpenClaw skill 处理多 Agent 编排。

**文件结构**:

```
daily-stock-analysis-openclaw-skill/
├── SKILL.md                    # 主技能说明
├── multi_agent_skill.md         # 多 Agent 专用 skill
├── src/
│   ├── multi_agent_orchestrator.py  # 编排核心
│   └── ...
```

**multi_agent_skill.md**:

```markdown
---
name: "stock_multi_agent_analyzer"
description: "多 Agent 编排分析股票。当用户请求深度分析时调用。"
---

# 多 Agent 股票分析器

## 工作流程

### 1. 启动 subagents

使用 `sessions_spawn` 启动 3 个专业分析 subagent：

```
sessions_spawn(
  task="请对 {stock_code} 进行技术面分析...",
  label="技术面分析-{stock_code}",
  mode="run"
)

sessions_spawn(
  task="请对 {stock_code} 进行舆情面分析...",
  label="舆情面分析-{stock_code}",
  mode="run"
)

sessions_spawn(
  task="请对 {stock_code} 进行基本面分析...",
  label="基本面分析-{stock_code}",
  mode="run"
)
```

### 2. 等待完成

每个 subagent 完成后会自动 announce 结果。

### 3. 综合分析

提取结果并调用 `src/multi_agent_orchestrator.py` 进行综合分析。

### 4. 输出报告

生成 HTML 格式决策仪表盘报告。
```

**优点**:
- ✅ 清晰的 tool 调用流程
- ✅ 复用现有编排核心
- ✅ 符合 OpenClaw skill 模式

---

## 📋 实施步骤

### P0: 验证 sessions_spawn 可用性

```bash
# 在 OpenClaw 主会话中测试
openclaw sessions spawn --agent research-analyst --task "回复 OK"
```

### P1: 创建多 Agent Skill 入口

- [ ] 创建 `multi_agent_skill.md`
- [ ] 定义 `sessions_spawn` 调用流程
- [ ] 集成 `multi_agent_orchestrator.py`

### P2: 更新 SKILL.md

- [ ] 添加多 Agent 触发条件
- [ ] 说明使用 `sessions_spawn`
- [ ] 提供使用示例

### P3: 测试完整流程

- [ ] 启动 3 个 subagents
- [ ] 等待完成
- [ ] 综合分析
- [ ] 输出报告

---

## ⚠️ 注意事项

### 1. 权限控制

确保 `research-analyst` agent 允许调用 `sessions_spawn`：

```json5
{
  agents: {
    list: [
      {
        id: "research-analyst",
        subagents: {
          allowAgents: ["research-analyst"]  // 允许启动自己
        }
      }
    ]
  }
}
```

### 2. 并发限制

默认 `maxConcurrent: 8`，3 个 subagents 不会超限。

### 3. 超时设置

建议设置 `runTimeoutSeconds: 300`（5 分钟）防止卡住。

### 4. 结果提取

subagent 完成后 announce 的结果格式：

```
[Inter-session message]
source: subagent
session_key: agent:research-analyst:subagent:uuid
status: completed successfully
Result: {JSON 格式分析结果}
```

需要从 announce 中提取 JSON 结果。

---

## 🎯 推荐方案

**方案 C**（创建多 Agent Skill 入口）是最佳选择：

1. 符合 OpenClaw 设计模式
2. 清晰的 tool 调用流程
3. 复用现有编排核心
4. 易于维护和扩展

**下一步**: 创建 `multi_agent_skill.md` 并测试 `sessions_spawn` 调用。

---

**创建日期**: 2026-03-25  
**最后更新**: 2026-03-25  
**维护者**: WebLeOn
