#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多 Agent 编排器测试
测试 orchestrator 模块的所有核心功能
"""

import pytest
import sys
import time
from datetime import datetime
from pathlib import Path

# 添加 src 目录到路径
sys.path.insert(0, str(Path(__file__).parent.parent.parent / "src"))

from agents.orchestrator import (
    MultiAgentOrchestrator,
    AgentStatus,
    AgentSession,
    create_orchestrator
)


class TestMultiAgentOrchestrator:
    """MultiAgentOrchestrator 测试类"""
    
    @pytest.fixture
    def orchestrator(self):
        """创建测试用的编排器实例"""
        return create_orchestrator()
    
    def test_spawn_agent(self, orchestrator):
        """测试 Agent 启动"""
        # 启动 Agent
        session_key = orchestrator.spawn_agent("测试任务", "test_agent")
        
        # 验证会话密钥生成
        assert session_key is not None
        assert "test_agent" in session_key
        assert len(session_key) > 0
        
        # 验证会话已注册
        assert session_key in orchestrator.agents
        assert session_key in orchestrator.status
        
        # 验证初始状态
        session = orchestrator.agents[session_key]
        assert session.task == "测试任务"
        assert session.agent_name == "test_agent"
        assert session.status == AgentStatus.RUNNING
        assert session.start_time is not None
        assert session.retry_count == 0
        
        print(f"✓ Agent 启动测试通过：{session_key}")
    
    def test_spawn_agent_default_name(self, orchestrator):
        """测试使用默认 Agent 名称"""
        session_key = orchestrator.spawn_agent("测试任务")
        
        session = orchestrator.agents[session_key]
        assert session.agent_name == "default_agent"
        
        print("✓ 默认 Agent 名称测试通过")
    
    def test_monitor_status(self, orchestrator):
        """测试状态监控"""
        session_key = orchestrator.spawn_agent("测试任务", "monitor_test")
        
        # 监控状态
        status = orchestrator.monitor_status(session_key)
        assert status == AgentStatus.RUNNING.value
        
        # 验证状态字典已更新
        assert orchestrator.status[session_key] == AgentStatus.RUNNING.value
        
        print("✓ 状态监控测试通过")
    
    def test_monitor_status_unknown_session(self, orchestrator):
        """测试监控未知会话"""
        status = orchestrator.monitor_status("unknown_session")
        assert status == AgentStatus.FAILED.value
        
        print("✓ 未知会话监控测试通过")
    
    def test_mark_completed(self, orchestrator):
        """测试标记完成"""
        session_key = orchestrator.spawn_agent("测试任务", "complete_test")
        
        # 标记完成
        result = {"score": 85, "conclusion": "测试通过"}
        orchestrator.mark_completed(session_key, result)
        
        # 验证状态
        status = orchestrator.monitor_status(session_key)
        assert status == AgentStatus.COMPLETED.value
        
        # 验证结果已保存
        session = orchestrator.agents[session_key]
        assert session.result == result
        assert session.end_time is not None
        
        print("✓ 标记完成测试通过")
    
    def test_mark_failed(self, orchestrator):
        """测试标记失败"""
        session_key = orchestrator.spawn_agent("测试任务", "fail_test")
        
        # 标记失败
        error_message = "模拟错误"
        orchestrator.mark_failed(session_key, error_message)
        
        # 验证状态
        status = orchestrator.monitor_status(session_key)
        assert status == AgentStatus.FAILED.value
        
        # 验证错误信息已保存
        session = orchestrator.agents[session_key]
        assert session.error_message == error_message
        assert session.end_time is not None
        
        # 验证错误已记录
        assert len(orchestrator.errors[session_key]) > 0
        
        print("✓ 标记失败测试通过")
    
    def test_error_recovery(self, orchestrator):
        """测试错误恢复"""
        session_key = orchestrator.spawn_agent("测试任务", "recovery_test")
        
        # 先标记失败
        orchestrator.mark_failed(session_key, "初始错误")
        
        # 尝试恢复
        success = orchestrator.recover_from_error(session_key, max_retries=3)
        
        # 验证恢复成功
        assert success is True
        
        # 验证状态已重置为运行中
        status = orchestrator.monitor_status(session_key)
        assert status == AgentStatus.RUNNING.value
        
        # 验证重试计数
        session = orchestrator.agents[session_key]
        assert session.retry_count == 1
        
        print("✓ 错误恢复测试通过")
    
    def test_error_recovery_max_retries(self, orchestrator):
        """测试达到最大重试次数"""
        session_key = orchestrator.spawn_agent("测试任务", "max_retry_test")
        orchestrator.mark_failed(session_key, "错误")
        
        # 尝试恢复 3 次
        for i in range(3):
            orchestrator.recover_from_error(session_key, max_retries=3)
            orchestrator.mark_failed(session_key, f"错误 {i+1}")
        
        # 第 4 次应该失败
        success = orchestrator.recover_from_error(session_key, max_retries=3)
        assert success is False
        
        print("✓ 最大重试次数测试通过")
    
    def test_timeout_handling(self, orchestrator):
        """测试超时处理"""
        # 临时修改超时时间为 1 秒以便测试
        original_timeout = orchestrator.TIMEOUT_SECONDS
        orchestrator.TIMEOUT_SECONDS = 1
        
        session_key = orchestrator.spawn_agent("长时间任务", "timeout_test")
        
        # 等待超时
        time.sleep(1.5)
        
        # 检查状态
        status = orchestrator.monitor_status(session_key)
        assert status == AgentStatus.TIMEOUT.value
        
        # 恢复原始超时时间
        orchestrator.TIMEOUT_SECONDS = original_timeout
        
        print("✓ 超时处理测试通过")
    
    def test_logging(self, orchestrator):
        """测试日志记录"""
        session_key = orchestrator.spawn_agent("测试任务", "log_test")
        
        # 执行一些操作
        orchestrator.monitor_status(session_key)
        orchestrator.mark_completed(session_key, {"result": "test"})
        
        # 获取日志
        logs = orchestrator.get_logs(session_key)
        
        # 验证日志
        assert len(logs) > 0
        assert all("timestamp" in log for log in logs)
        assert all("level" in log for log in logs)
        assert all("message" in log for log in logs)
        
        # 验证日志级别
        levels = [log["level"] for log in logs]
        assert "INFO" in levels
        
        print(f"✓ 日志记录测试通过（{len(logs)} 条日志）")
    
    def test_get_session_info(self, orchestrator):
        """测试获取会话信息"""
        session_key = orchestrator.spawn_agent("测试任务", "info_test")
        orchestrator.mark_completed(session_key, {"result": "test"})
        
        # 获取会话信息
        info = orchestrator.get_session_info(session_key)
        
        # 验证信息完整
        assert info is not None
        assert info["session_key"] == session_key
        assert info["agent_name"] == "info_test"
        assert info["status"] == AgentStatus.COMPLETED.value
        assert info["has_result"] is True
        assert info["log_count"] > 0
        
        print("✓ 会话信息测试通过")
    
    def test_get_session_info_unknown(self, orchestrator):
        """测试获取未知会话信息"""
        info = orchestrator.get_session_info("unknown")
        assert info is None
        
        print("✓ 未知会话信息测试通过")
    
    def test_get_all_sessions(self, orchestrator):
        """测试获取所有会话"""
        # 创建多个会话
        keys = []
        for i in range(3):
            key = orchestrator.spawn_agent(f"任务{i}", f"agent{i}")
            keys.append(key)
        
        # 获取所有会话
        all_sessions = orchestrator.get_all_sessions()
        
        # 验证
        assert len(all_sessions) == 3
        for key in keys:
            assert key in all_sessions
        
        print("✓ 获取所有会话测试通过")
    
    def test_cleanup_old_sessions(self, orchestrator):
        """测试清理旧会话"""
        # 创建会话并标记完成
        key = orchestrator.spawn_agent("任务", "cleanup_test")
        orchestrator.mark_completed(key)
        
        # 模拟旧会话（修改结束时间）
        from datetime import timedelta
        orchestrator.agents[key].end_time = datetime.now() - timedelta(hours=25)
        
        # 清理
        cleaned = orchestrator.cleanup_old_sessions(max_age_hours=24)
        
        # 验证
        assert cleaned == 1
        assert key not in orchestrator.agents
        
        print("✓ 清理旧会话测试通过")
    
    def test_wait_for_completion(self, orchestrator):
        """测试等待完成"""
        session_key = orchestrator.spawn_agent("任务", "wait_test")
        
        # 在后台标记完成
        import threading
        def complete_later():
            time.sleep(0.5)
            orchestrator.mark_completed(session_key, {"result": "done"})
        
        thread = threading.Thread(target=complete_later)
        thread.start()
        
        # 等待完成
        final_status = orchestrator.wait_for_completion(session_key, poll_interval=0.1)
        
        # 验证
        assert final_status == AgentStatus.COMPLETED.value
        
        thread.join()
        print("✓ 等待完成测试通过")


class TestAgentStatus:
    """AgentStatus 枚举测试"""
    
    def test_status_values(self):
        """测试状态值"""
        assert AgentStatus.PENDING.value == "pending"
        assert AgentStatus.RUNNING.value == "running"
        assert AgentStatus.COMPLETED.value == "completed"
        assert AgentStatus.FAILED.value == "failed"
        assert AgentStatus.TIMEOUT.value == "timeout"
        
        print("✓ 状态值测试通过")
    
    def test_status_from_string(self):
        """测试从字符串创建状态"""
        status = AgentStatus("running")
        assert status == AgentStatus.RUNNING
        
        print("✓ 从字符串创建状态测试通过")


class TestAgentSession:
    """AgentSession 数据类测试"""
    
    def test_session_creation(self):
        """测试会话创建"""
        session = AgentSession(
            session_key="test_key",
            task="测试任务",
            agent_name="test_agent"
        )
        
        assert session.session_key == "test_key"
        assert session.task == "测试任务"
        assert session.agent_name == "test_agent"
        assert session.status == AgentStatus.PENDING
        assert session.retry_count == 0
        assert len(session.logs) == 0
        
        print("✓ 会话创建测试通过")


# 集成测试
class TestOrchestratorIntegration:
    """编排器集成测试"""
    
    def test_full_workflow(self):
        """测试完整工作流程"""
        orchestrator = create_orchestrator()
        
        # 1. 启动 Agent
        session_key = orchestrator.spawn_agent("完整测试任务", "workflow_agent")
        
        # 2. 监控状态
        status = orchestrator.monitor_status(session_key)
        assert status == AgentStatus.RUNNING.value
        
        # 3. 模拟执行
        time.sleep(0.1)
        
        # 4. 标记完成
        orchestrator.mark_completed(session_key, {
            "result": "success",
            "data": {"key": "value"}
        })
        
        # 5. 验证最终状态
        final_status = orchestrator.monitor_status(session_key)
        assert final_status == AgentStatus.COMPLETED.value
        
        # 6. 获取日志
        logs = orchestrator.get_logs(session_key)
        assert len(logs) > 0
        
        # 7. 获取会话信息
        info = orchestrator.get_session_info(session_key)
        assert info["status"] == AgentStatus.COMPLETED.value
        assert info["has_result"] is True
        
        print("✓ 完整工作流程测试通过")
    
    def test_error_recovery_workflow(self):
        """测试错误恢复工作流程"""
        orchestrator = create_orchestrator()
        
        # 1. 启动 Agent
        session_key = orchestrator.spawn_agent("失败任务", "recovery_agent")
        
        # 2. 标记失败
        orchestrator.mark_failed(session_key, "第一次失败")
        
        # 3. 恢复
        success = orchestrator.recover_from_error(session_key)
        assert success is True
        
        # 4. 再次标记完成
        orchestrator.mark_completed(session_key, {"result": "恢复后成功"})
        
        # 5. 验证
        info = orchestrator.get_session_info(session_key)
        assert info["status"] == AgentStatus.COMPLETED.value
        assert info["retry_count"] == 1
        
        print("✓ 错误恢复工作流程测试通过")


# 运行测试
if __name__ == "__main__":
    print("=" * 60)
    print("多 Agent 编排器测试")
    print("=" * 60)
    print()
    
    # 创建测试实例
    test = TestMultiAgentOrchestrator()
    orchestrator = test.orchestrator()
    
    # 运行测试
    tests = [
        ("Agent 启动", lambda: test.test_spawn_agent(orchestrator)),
        ("默认 Agent 名称", lambda: test.test_spawn_agent_default_name(orchestrator)),
        ("状态监控", lambda: test.test_monitor_status(orchestrator)),
        ("未知会话监控", lambda: test.test_monitor_status_unknown_session(orchestrator)),
        ("标记完成", lambda: test.test_mark_completed(orchestrator)),
        ("标记失败", lambda: test.test_mark_failed(orchestrator)),
        ("错误恢复", lambda: test.test_error_recovery(orchestrator)),
        ("最大重试次数", lambda: test.test_error_recovery_max_retries(orchestrator)),
        ("日志记录", lambda: test.test_logging(orchestrator)),
        ("会话信息", lambda: test.test_get_session_info(orchestrator)),
        ("未知会话信息", lambda: test.test_get_session_info_unknown(orchestrator)),
        ("获取所有会话", lambda: test.test_get_all_sessions(orchestrator)),
    ]
    
    passed = 0
    failed = 0
    
    for name, test_func in tests:
        try:
            test_func()
            passed += 1
        except Exception as e:
            print(f"✗ {name} 测试失败：{e}")
            failed += 1
    
    print()
    print("-" * 60)
    print(f"测试结果：{passed} 通过，{failed} 失败")
    print("=" * 60)
    
    sys.exit(0 if failed == 0 else 1)
