"""
插件基类
所有插件必须继承此类
"""


class BasePlugin:
    """插件基类"""
    
    name = "base_plugin"
    version = "1.0.0"
    description = "基础插件"
    plugin_type = "base"
    
    def __init__(self, config=None):
        self.config = config or {}
    
    def initialize(self):
        """初始化插件"""
        return True
    
    def validate(self):
        """验证配置"""
        return True
    
    def get_info(self):
        """获取插件信息"""
        return {
            "name": self.name,
            "version": self.version,
            "description": self.description,
            "type": self.plugin_type
        }
