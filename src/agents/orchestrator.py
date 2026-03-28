#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
多 Agent 编排器
负责 Agent 状态监控、错误恢复、日志记录
"""

import logging
import subprocess
import json
import time
from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
from enum import Enum

logger = logging.getLogger(__name__)


class AgentStatus(Enum):
    """Agent 状态枚举"""
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"


@dataclass
class AgentSession:
    """Agent 会话信息"""
    session_key: str
    task: str
    agent_name: str
    status: AgentStatus = AgentStatus.PENDING
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    error_message: str = ""
    retry_count: int = 0
    logs: List[Dict] = field(default_factory=list)
    result: Optional[Dict] = None


class MultiAgentOrchestrator:
    """多 Agent 编排器"""
    
    # 超时时间（秒）
    TIMEOUT_SECONDS = 300  # 5 分钟
    # 最大重试次数
    MAX_RETRIES = 3
    # 重试间隔（秒）
    RETRY_DELAY = 5
    
    def __init__(self):
        self.agents: Dict[str, AgentSession] = {}
        self.status: Dict[str, str] = {}
        self.errors: Dict[str, List] = {}
        self._setup_logging()
    
    def _setup_logging(self):
        """设置日志"""
        if not logger.handlers:
            handler = logging.StreamHandler()
            handler.setFormatter(logging.Formatter(
                '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
            ))
            logger.addHandler(handler)
            logger.setLevel(logging.INFO)
    
    def _log(self, session_key: str, level: str, message: str, data: Optional[Dict] = None):
        """记录日志"""
        log_entry = {
            "timestamp": datetime.now().isoformat(),
            "level": level,
            "message": message,
            "data": data or {}
        }
        
        if session_key in self.agents:
            self.agents[session_key].logs.append(log_entry)
        
        # 同时记录到 Python logger
        log_func = getattr(logger, level.lower(), logger.info)
        log_func(f"[{session_key}] {message}")
    
    def _generate_session_key(self, task: str, agent_name: str) -> str:
        """生成会话密钥"""
        timestamp = datetime.now().strftime("%Y%m%d%H%M%S")
        name = agent_name or "agent"
        # 简化任务名作为前缀
        task_prefix = task[:20].replace(" ", "_").replace("-", "_")
        return f"{name}_{task_prefix}_{timestamp}"
    
    def spawn_agent(self, task: str, agent_name: str = None) -> str:
        """
        启动子 Agent
        
        Args:
            task: 任务描述
            agent_name: Agent 名称（可选）
            
        Returns:
            session_key: 会话密钥
        """
        session_key = self._generate_session_key(task, agent_name)
        
        # 创建会话
        session = AgentSession(
            session_key=session_key,
            task=task,
            agent_name=agent_name or "default_agent",
            status=AgentStatus.PENDING,
            start_time=datetime.now()
        )
        
        self.agents[session_key] = session
        self.status[session_key] = AgentStatus.PENDING.value
        self.errors[session_key] = []
        
        self._log(session_key, "INFO", f"Agent 启动：{agent_name or 'default_agent'}", {
            "task": task[:100] + "..." if len(task) > 100 else task
        })
        
        # 更新状态为运行中
        session.status = AgentStatus.RUNNING
        self.status[session_key] = AgentStatus.RUNNING.value
        self._log(session_key, "INFO", "Agent 开始执行任务")
        
        return session_key
    
    def _check_process_status(self, session_key: str) -> str:
        """
        检查进程状态（模拟）
        在实际 OpenClaw 环境中，这里应该调用 sessions_poll 或类似 API
        """
        if session_key not in self.agents:
            return AgentStatus.FAILED.value
        
        session = self.agents[session_key]
        
        # 检查超时
        if session.start_time:
            elapsed = (datetime.now() - session.start_time).total_seconds()
            if elapsed > self.TIMEOUT_SECONDS:
                return AgentStatus.TIMEOUT.value
        
        # 默认返回当前状态
        # 在实际实现中，这里应该查询 OpenClaw 的 session 状态
        return session.status.value
    
    def monitor_status(self, session_key: str) -> str:
        """
        监控 Agent 状态
        
        Args:
            session_key: 会话密钥
            
        Returns:
            status: 当前状态 (pending/running/completed/failed/timeout)
        """
        if session_key not in self.agents:
            logger.warning(f"未知的会话密钥：{session_key}")
            return AgentStatus.FAILED.value
        
        session = self.agents[session_key]
        current_status = self._check_process_status(session_key)
        
        # 更新状态
        session.status = AgentStatus(current_status)
        self.status[session_key] = current_status
        
        self._log(session_key, "DEBUG", f"状态检查：{current_status}")
        
        return current_status
    
    def wait_for_completion(self, session_key: str, poll_interval: float = 2.0) -> str:
        """
        等待 Agent 完成
        
        Args:
            session_key: 会话密钥
            poll_interval: 轮询间隔（秒）
            
        Returns:
            final_status: 最终状态
        """
        while True:
            status = self.monitor_status(session_key)
            
            if status in [AgentStatus.COMPLETED.value, AgentStatus.FAILED.value, AgentStatus.TIMEOUT.value]:
                return status
            
            # 检查超时
            session = self.agents.get(session_key)
            if session and session.start_time:
                elapsed = (datetime.now() - session.start_time).total_seconds()
                if elapsed > self.TIMEOUT_SECONDS:
                    session.status = AgentStatus.TIMEOUT
                    self.status[session_key] = AgentStatus.TIMEOUT.value
                    self._log(session_key, "ERROR", f"任务超时（>{self.TIMEOUT_SECONDS}秒）")
                    return AgentStatus.TIMEOUT.value
            
            time.sleep(poll_interval)
    
    def recover_from_error(self, session_key: str, max_retries: int = 3) -> bool:
        """
        错误恢复
        
        Args:
            session_key: 会话密钥
            max_retries: 最大重试次数
            
        Returns:
            success: 是否恢复成功
        """
        if session_key not in self.agents:
            logger.error(f"未知的会话密钥：{session_key}")
            return False
        
        session = self.agents[session_key]
        
        if session.retry_count >= max_retries:
            self._log(session_key, "ERROR", f"达到最大重试次数 ({max_retries})，放弃恢复")
            return False
        
        # 增加重试计数
        session.retry_count += 1
        
        self._log(session_key, "WARNING", f"尝试错误恢复 (第 {session.retry_count}/{max_retries} 次)", {
            "last_error": session.error_message
        })
        
        # 记录错误
        self.errors[session_key].append({
            "timestamp": datetime.now().isoformat(),
            "retry": session.retry_count,
            "error": session.error_message
        })
        
        # 延迟后重试
        time.sleep(self.RETRY_DELAY)
        
        # 重新设置状态为运行中
        session.status = AgentStatus.RUNNING
        session.start_time = datetime.now()
        self.status[session_key] = AgentStatus.RUNNING.value
        
        self._log(session_key, "INFO", f"重试开始 (尝试 {session.retry_count})")
        
        return True
    
    def mark_completed(self, session_key: str, result: Optional[Dict] = None):
        """
        标记任务完成
        
        Args:
            session_key: 会话密钥
            result: 任务结果
        """
        if session_key not in self.agents:
            logger.warning(f"未知的会话密钥：{session_key}")
            return
        
        session = self.agents[session_key]
        session.status = AgentStatus.COMPLETED
        session.end_time = datetime.now()
        session.result = result
        self.status[session_key] = AgentStatus.COMPLETED.value
        
        self._log(session_key, "INFO", "任务完成", {"result": result})
    
    def mark_failed(self, session_key: str, error_message: str):
        """
        标记任务失败
        
        Args:
            session_key: 会话密钥
            error_message: 错误信息
        """
        if session_key not in self.agents:
            logger.warning(f"未知的会话密钥：{session_key}")
            return
        
        session = self.agents[session_key]
        session.status = AgentStatus.FAILED
        session.end_time = datetime.now()
        session.error_message = error_message
        self.status[session_key] = AgentStatus.FAILED.value
        
        self._log(session_key, "ERROR", f"任务失败：{error_message}")
        self.errors[session_key].append({
            "timestamp": datetime.now().isoformat(),
            "error": error_message
        })
    
    def get_logs(self, session_key: str) -> List[Dict]:
        """
        获取日志
        
        Args:
            session_key: 会话密钥
            
        Returns:
            logs: 日志列表
        """
        if session_key not in self.agents:
            logger.warning(f"未知的会话密钥：{session_key}")
            return []
        
        return self.agents[session_key].logs
    
    def get_session_info(self, session_key: str) -> Optional[Dict]:
        """
        获取会话信息
        
        Args:
            session_key: 会话密钥
            
        Returns:
            session_info: 会话信息字典
        """
        if session_key not in self.agents:
            return None
        
        session = self.agents[session_key]
        return {
            "session_key": session.session_key,
            "agent_name": session.agent_name,
            "task": session.task,
            "status": session.status.value,
            "start_time": session.start_time.isoformat() if session.start_time else None,
            "end_time": session.end_time.isoformat() if session.end_time else None,
            "retry_count": session.retry_count,
            "error_message": session.error_message,
            "log_count": len(session.logs),
            "has_result": session.result is not None
        }
    
    def get_all_sessions(self) -> Dict[str, Dict]:
        """
        获取所有会话信息
        
        Returns:
            sessions: 所有会话信息
        """
        return {
            key: self.get_session_info(key)
            for key in self.agents.keys()
        }
    
    def cleanup_old_sessions(self, max_age_hours: int = 24) -> int:
        """
        清理旧会话
        
        Args:
            max_age_hours: 最大保留时间（小时）
            
        Returns:
            cleaned_count: 清理的会话数量
        """
        cleaned = 0
        now = datetime.now()
        
        for key in list(self.agents.keys()):
            session = self.agents[key]
            if session.end_time:
                age = (now - session.end_time).total_seconds() / 3600
                if age > max_age_hours:
                    del self.agents[key]
                    if key in self.status:
                        del self.status[key]
                    if key in self.errors:
                        del self.errors[key]
                    cleaned += 1
        
        if cleaned > 0:
            logger.info(f"清理了 {cleaned} 个旧会话")
        
        return cleaned


# 便捷函数
def create_orchestrator() -> MultiAgentOrchestrator:
    """创建编排器实例"""
    return MultiAgentOrchestrator()


# 测试
if __name__ == "__main__":
    print("=== 多 Agent 编排器测试 ===\n")
    
    # 创建编排器
    orchestrator = create_orchestrator()
    
    # 测试启动 Agent
    print("1. 测试启动 Agent")
    session_key = orchestrator.spawn_agent("分析 AAPL 股票", "technical_analyst")
    print(f"   会话密钥：{session_key}")
    print(f"   当前状态：{orchestrator.monitor_status(session_key)}")
    print()
    
    # 测试状态监控
    print("2. 测试状态监控")
    status = orchestrator.monitor_status(session_key)
    print(f"   状态：{status}")
    print()
    
    # 测试标记完成
    print("3. 测试标记完成")
    orchestrator.mark_completed(session_key, {"score": 85, "conclusion": "看涨"})
    print(f"   最终状态：{orchestrator.monitor_status(session_key)}")
    print()
    
    # 测试获取日志
    print("4. 测试获取日志")
    logs = orchestrator.get_logs(session_key)
    print(f"   日志数量：{len(logs)}")
    for log in logs:
        print(f"   - [{log['level']}] {log['message']}")
    print()
    
    # 测试获取会话信息
    print("5. 测试获取会话信息")
    info = orchestrator.get_session_info(session_key)
    print(f"   会话信息：{json.dumps(info, indent=2, ensure_ascii=False)}")
    print()
    
    # 测试错误恢复
    print("6. 测试错误恢复")
    session_key2 = orchestrator.spawn_agent("失败任务", "test_agent")
    orchestrator.mark_failed(session_key2, "模拟错误")
    print(f"   初始状态：{orchestrator.monitor_status(session_key2)}")
    success = orchestrator.recover_from_error(session_key2)
    print(f"   恢复结果：{success}")
    print(f"   恢复后状态：{orchestrator.monitor_status(session_key2)}")
    print()
    
    print("=== 测试完成 ===")
