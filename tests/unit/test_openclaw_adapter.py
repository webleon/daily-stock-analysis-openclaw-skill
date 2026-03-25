"""
OpenClaw 适配器单元测试
"""

import pytest
from src.openclaw.adapter import OpenClawAdapter


class TestOpenClawAdapter:
    """OpenClawAdapter 测试"""
    
    def test_init(self):
        """测试初始化"""
        adapter = OpenClawAdapter()
        assert adapter.api_version in ["1.0", "1.5", "2.0"]
    
    def test_detect_api_version(self):
        """测试版本检测"""
        adapter = OpenClawAdapter()
        version = adapter._detect_api_version()
        assert isinstance(version, str)
        assert version in ["1.0", "1.5", "2.0"]
    
    def test_spawn_subagent(self):
        """测试 subagent 启动"""
        adapter = OpenClawAdapter()
        # 注意：实际测试需要 mock sessions_spawn
        # 这里只测试接口存在
        assert hasattr(adapter, 'spawn_subagent')
    
    def test_register_tool(self):
        """测试 tool 注册"""
        adapter = OpenClawAdapter()
        # 注意：实际测试需要 mock register_tool
        assert hasattr(adapter, 'register_tool')
