"""
ComfyUI-Toolbox 主插件入口
统一管理所有子插件
"""

import os
import importlib
import pkgutil
from typing import Dict, Any

# 全局节点映射
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def load_plugin_modules():
    """动态加载所有插件模块"""
    plugins_dir = os.path.join(os.path.dirname(__file__), "plugins")
    
    if not os.path.exists(plugins_dir):
        return
    
    # 遍历plugins目录下的所有子目录
    for plugin_name in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_name)
        
        if os.path.isdir(plugin_path):
            # 检查是否有__init__.py文件
            init_file = os.path.join(plugin_path, "__init__.py")
            if os.path.exists(init_file):
                try:
                    # 导入插件模块
                    module_name = f"plugins.{plugin_name}"
                    module = importlib.import_module(module_name, package=__package__)
                    
                    # 获取节点映射
                    if hasattr(module, 'NODE_CLASS_MAPPINGS'):
                        NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                    
                    if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
                        NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
                        
                    print(f"✓ 已加载插件: {plugin_name}")
                    
                except Exception as e:
                    print(f"✗ 加载插件 {plugin_name} 失败: {e}")

# 加载所有插件
load_plugin_modules()

# 导出节点映射
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 