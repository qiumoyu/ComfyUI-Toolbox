"""
ComfyUI-Toolbox 主插件入口
统一管理所有子插件
"""

import os
import importlib.util
import sys
from typing import Dict, Any

# 全局节点映射
NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

def load_plugin_modules():
    """动态加载所有插件模块"""
    current_dir = os.path.dirname(__file__)
    plugins_dir = os.path.join(current_dir, "plugins")
    
    if not os.path.exists(plugins_dir):
        print(f"插件目录不存在: {plugins_dir}")
        return
    
    # 遍历plugins目录下的所有子目录
    for plugin_name in os.listdir(plugins_dir):
        plugin_path = os.path.join(plugins_dir, plugin_name)
        
        if os.path.isdir(plugin_path):
            # 检查是否有__init__.py文件
            init_file = os.path.join(plugin_path, "__init__.py")
            if os.path.exists(init_file):
                try:
                    # 使用spec方式导入模块
                    spec = importlib.util.spec_from_file_location(
                        f"plugins_{plugin_name}", init_file
                    )
                    if spec and spec.loader:
                        module = importlib.util.module_from_spec(spec)
                        sys.modules[f"plugins_{plugin_name}"] = module
                        spec.loader.exec_module(module)
                        
                        # 获取节点映射
                        if hasattr(module, 'NODE_CLASS_MAPPINGS'):
                            NODE_CLASS_MAPPINGS.update(module.NODE_CLASS_MAPPINGS)
                        
                        if hasattr(module, 'NODE_DISPLAY_NAME_MAPPINGS'):
                            NODE_DISPLAY_NAME_MAPPINGS.update(module.NODE_DISPLAY_NAME_MAPPINGS)
                            
                        print(f"✓ 已加载插件: {plugin_name}")
                        
                except Exception as e:
                    print(f"✗ 加载插件 {plugin_name} 失败: {e}")
                    import traceback
                    traceback.print_exc()

# 加载所有插件
load_plugin_modules()

print(f"已注册节点: {list(NODE_CLASS_MAPPINGS.keys())}")
WEB_DIRECTORY = os.path.join(os.path.dirname(__file__), "web", "js")

# 导出节点映射 - 这是ComfyUI需要的
__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 