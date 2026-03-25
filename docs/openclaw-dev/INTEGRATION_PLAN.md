# 多 Agent 编排集成实施方案

**版本**: 1.0  
**创建日期**: 2026-03-25  
**状态**: 📋 规划中

---

## 📊 现有代码结构分析

### 核心文件

| 文件 | 作用 | 行数 |
|------|------|------|
| `src/analyzer.py` | AI 分析核心（LLM 调用+ 结果解析） | 2,000+ |
| `src/stock_analyzer.py` | 趋势交易分析器 | 800+ |
| `src/market_analyzer.py` | 市场分析 | 700+ |
| `src/formatters.py` | 格式化输出 | 600+ |
| `src/notification.py` | 通知推送 | 2,000+ |

### 核心类

```python
# analyzer.py
class AnalysisResult:
    """AI 分析结果"""
    code: str
    name: str
    sentiment_score: int  # 综合评分 0-100
    trend_prediction: str  # 趋势预测
    operation_advice: str  # 操作建议
    dashboard: Dict  # 决策仪表盘

class Analyzer:
    """分析器主类"""
    def analyze(self, stock_code: str, ...) -> AnalysisResult:
        """执行分析"""
```

### 当前流程

```
用户请求 → Analyzer.analyze() → LLM 调用 → 解析结果 → 输出报告
```

---

## 🎯 集成目标

### 目标架构

```
用户请求："深度分析 AAPL"
    ↓
Analyzer.analyze() 检测深度分析标记
    ↓
MultiAgentOrchestrator 启动
    ↓
┌─────────────────────────────────────┐
│ sessions_spawn → 技术面 subagent    │
│ sessions_spawn → 舆情面 subagent    │
│ sessions_spawn → 基本面 subagent    │
└─────────────────────────────────────┘
    ↓
等待所有 subagent 完成
    ↓
综合分析 → AnalysisResult
    ↓
生成 HTML 报告 → 保存到 output/
    ↓
发送通知到 Telegram
```

---

## 📋 实施方案

### 方案 A: 最小改动（推荐）

**核心思路**: 在 `Analyzer.analyze()` 中添加多 Agent 分支

#### 步骤 1: 修改 SKILL.md 触发条件

```markdown
## 触发条件

### 普通分析（单 Agent）
- "分析 AAPL"
- "看看 NVDA"
- "600989 怎么样"

### 深度分析（多 Agent）
- "深度分析 AAPL"
- "详细分析 NVDA"
- "用多 Agent 分析 TSLA"
- "全面分析 {股票代码}"
- "professional analysis AAPL"
```

#### 步骤 2: 修改 Analyzer 类

在 `src/analyzer.py` 中添加：

```python
class Analyzer:
    def analyze(
        self,
        stock_code: str,
        multi_agent: bool = False,  # 新增参数
        **kwargs
    ) -> AnalysisResult:
        """
        分析股票（支持多 Agent 模式）
        
        Args:
            stock_code: 股票代码
            multi_agent: 是否启用多 Agent 编排
        """
        if multi_agent:
            return self._analyze_with_multi_agent(stock_code, **kwargs)
        else:
            return self._analyze_single_agent(stock_code, **kwargs)
    
    def _analyze_with_multi_agent(
        self,
        stock_code: str,
        **kwargs
    ) -> AnalysisResult:
        """使用多 Agent 编排分析"""
        from .multi_agent_orchestrator import MultiAgentOrchestrator
        
        # 1. 创建编排器
        orchestrator = MultiAgentOrchestrator(stock_code)
        
        # 2. 生成任务
        tasks = orchestrator.generate_tasks()
        
        # 3. 启动 OpenClaw subagents
        subagent_sessions = []
        for task in tasks:
            session = self._spawn_subagent(task)
            subagent_sessions.append(session)
        
        # 4. 等待所有 subagent 完成
        results = []
        for session in subagent_sessions:
            result = self._wait_for_subagent(session)
            results.append(result)
        
        # 5. 解析 subagent 结果
        for result_text, task in zip(results, tasks):
            parsed = orchestrator.parse_subagent_result(result_text, task.type)
            orchestrator.results.append(parsed)
        
        # 6. 综合分析
        report = orchestrator.synthesize_results()
        
        # 7. 转换为 AnalysisResult
        return self._convert_to_analysis_result(report, stock_code)
    
    def _spawn_subagent(self, task) -> str:
        """启动 subagent（调用 OpenClaw sessions_spawn）"""
        # 这里需要调用 OpenClaw 的 sessions_spawn API
        # 伪代码示例：
        from openclaw import sessions_spawn
        
        session = sessions_spawn(
            runtime="subagent",
            label=task.label,
            task=task.task,
            mode="run"
        )
        return session["childSessionKey"]
    
    def _wait_for_subagent(self, session_key: str) -> str:
        """等待 subagent 完成并返回结果"""
        # 等待 completion event
        # 返回 subagent 的输出文本
        pass
    
    def _convert_to_analysis_result(
        self,
        report: Dict,
        stock_code: str
    ) -> AnalysisResult:
        """将多 Agent 报告转换为 AnalysisResult"""
        dashboard = report["dashboard"]
        
        return AnalysisResult(
            code=stock_code,
            name=report.get("stock_name", ""),
            sentiment_score=int(report["overall_score"]),
            trend_prediction=dashboard["core_conclusion"]["signal_type"],
            operation_advice=dashboard["core_conclusion"]["position_suggestion"],
            dashboard=dashboard,
            decision_type=self._map_decision_type(report["overall_score"]),
            confidence_level=self._map_confidence(report["overall_score"])
        )
```

#### 步骤 3: 修改 SKILL.md 提示词

在 `SKILL.md` 的 prompt 中添加：

```markdown
## 多 Agent 模式

当用户请求中包含以下关键词时，启用多 Agent 编排：

- "深度分析"
- "详细分析"
- "全面分析"
- "professional analysis"
- "deep dive"

在多 Agent 模式下：
1. 启动 3 个专业分析 subagents（技术面/舆情面/基本面）
2. 等待所有 subagent 完成
3. 综合分析生成决策仪表盘
4. 输出 HTML 格式完整报告

多 Agent 分析耗时约 60 秒，但分析深度和准确率显著提升。
```

#### 步骤 4: 添加进度显示

```python
def _analyze_with_multi_agent(self, stock_code: str):
    # 发送进度消息
    self._send_progress("🔄 正在启动 3 个专业分析 Agent...")
    
    # 启动 subagents
    for i, task in enumerate(tasks, 1):
        self._send_progress(f"  - {task.label}... ({i}/3)")
        session = self._spawn_subagent(task)
    
    # 等待完成
    self._send_progress("⏳ 等待分析完成...")
    
    # 综合分析
    self._send_progress("📊 综合分析中...")
    
    # 完成
    self._send_progress("✅ 分析完成！")
```

---

### 方案 B: 独立服务（备选）

**核心思路**: 将多 Agent 编排作为独立服务运行

#### 架构

```
主会话 (stock_analyzer)
    ↓
检测深度分析请求
    ↓
HTTP/gRPC 调用 → Multi-Agent Service
    ↓
等待服务返回
    ↓
接收 AnalysisResult
    ↓
输出报告
```

#### 优点

- 完全解耦
- 可独立扩展
- 不影响现有代码

#### 缺点

- 需要额外部署
- 增加复杂度
- 响应时间更长

---

### 方案 C: 消息队列（高级）

**核心思路**: 使用消息队列异步处理

#### 架构

```
主会话 → 发布消息 → RabbitMQ/Kafka
                              ↓
                    Multi-Agent Worker 1
                    Multi-Agent Worker 2
                    Multi-Agent Worker 3
                              ↓
                       发布结果 → Redis
                              ↓
主会话 ← 订阅结果 ← Redis
```

#### 优点

- 完全异步
- 可处理大量并发
- 可重试机制

#### 缺点

- 架构复杂
- 需要额外基础设施
- 开发周期长

---

## 🎯 推荐方案：方案 A（最小改动）

### 理由

1. **改动最小**: 只需修改 `Analyzer.analyze()` 方法
2. **兼容性好**: 不影响现有单 Agent 流程
3. **快速实现**: 1-2 天可完成
4. **易于测试**: 可独立测试多 Agent 分支

### 实施步骤

#### P0: 核心功能（1-2 天）

- [ ] **修改 `src/analyzer.py`**
  - [ ] 添加 `multi_agent` 参数
  - [ ] 实现 `_analyze_with_multi_agent()` 方法
  - [ ] 实现 `_spawn_subagent()` 方法
  - [ ] 实现 `_wait_for_subagent()` 方法
  - [ ] 实现 `_convert_to_analysis_result()` 方法

- [ ] **修改 `SKILL.md`**
  - [ ] 添加多 Agent 触发条件
  - [ ] 说明深度分析模式

- [ ] **测试**
  - [ ] 单元测试多 Agent 分支
  - [ ] 集成测试完整流程
  - [ ] 性能测试（响应时间）

#### P1: 体验优化（1 天）

- [ ] **进度显示**
  - [ ] 实现 `_send_progress()` 方法
  - [ ] 添加进度消息模板

- [ ] **错误处理**
  - [ ] subagent 失败重试
  - [ ] 超时处理（5 分钟）
  - [ ] 降级到单 Agent 模式

#### P2: 生产就绪（1 天）

- [ ] **日志记录**
  - [ ] 记录 subagent 启动时间
  - [ ] 记录综合分析耗时
  - [ ] 记录错误信息

- [ ] **监控告警**
  - [ ] subagent 失败率监控
  - [ ] 响应时间监控
  - [ ] 异常告警

- [ ] **文档更新**
  - [ ] 更新 README.md
  - [ ] 添加多 Agent 使用示例
  - [ ] 更新 API 文档

---

## 📊 代码对比

### 现有代码（单 Agent）

```python
# 用户调用
result = analyzer.analyze("AAPL")

# 内部流程
def analyze(self, stock_code: str):
    # 1. 获取数据
    data = self.fetch_data(stock_code)
    
    # 2. 调用 LLM
    response = litellm.completion(
        model=self.model,
        messages=[{"role": "user", "content": prompt}]
    )
    
    # 3. 解析结果
    result = self._parse_response(response, stock_code)
    
    return result
```

### 集成后（多 Agent）

```python
# 用户调用
result = analyzer.analyze("AAPL", multi_agent=True)

# 内部流程
def analyze(self, stock_code: str, multi_agent: bool = False):
    if multi_agent:
        return self._analyze_with_multi_agent(stock_code)
    else:
        return self._analyze_single_agent(stock_code)

def _analyze_with_multi_agent(self, stock_code: str):
    # 1. 启动 3 个 subagents
    sessions = [
        self._spawn_subagent(technical_task),
        self._spawn_subagent(sentiment_task),
        self._spawn_subagent(fundamental_task)
    ]
    
    # 2. 等待完成
    results = [self._wait_for_subagent(s) for s in sessions]
    
    # 3. 综合分析
    report = self._synthesize(results)
    
    # 4. 转换为 AnalysisResult
    return self._convert_to_analysis_result(report, stock_code)
```

---

## 🧪 测试计划

### 单元测试

```python
def test_multi_agent_analysis():
    analyzer = Analyzer()
    result = analyzer.analyze("AAPL", multi_agent=True)
    
    assert result is not None
    assert result.sentiment_score > 0
    assert result.dashboard is not None
    assert "core_conclusion" in result.dashboard
```

### 集成测试

```python
def test_full_multi_agent_flow():
    # 模拟完整的 OpenClaw 环境
    # 测试从用户请求到报告生成的完整流程
    pass
```

### 性能测试

```python
def test_response_time():
    import time
    
    start = time.time()
    analyzer.analyze("AAPL", multi_agent=True)
    elapsed = time.time() - start
    
    # 多 Agent 应该在 90 秒内完成
    assert elapsed < 90
```

---

## ⚠️ 注意事项

### 1. Token 消耗

多 Agent 会增加 2-3 倍 token 消耗：
- 单 Agent: ~15,000 tokens
- 多 Agent: ~45,000 tokens

**解决方案**:
- 添加用户提示（"深度分析消耗较多 token"）
- 提供配置选项（是否启用多 Agent）

### 2. 响应时间

多 Agent 响应时间约 60 秒：
- 单 Agent: ~30 秒
- 多 Agent: ~60 秒（并行）

**解决方案**:
- 添加进度显示
- 流式输出中间结果

### 3. OpenClaw 依赖

需要调用 `sessions_spawn` API：
- 确认 API 可用性
- 处理 API 错误
- 添加降级策略

---

## 📚 相关文档

- [多 Agent 编排核心代码](src/multi_agent_orchestrator.py)
- [多 Agent 使用指南](MULTI_AGENT_GUIDE.md)
- [Subagent 任务模板](subagent_tasks.py)

---

**创建日期**: 2026-03-25  
**最后更新**: 2026-03-25  
**维护者**: WebLeOn
