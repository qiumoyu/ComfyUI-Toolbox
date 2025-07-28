"""
遮罩分析插件
提供遮罩边缘检测功能
"""

import os
import importlib.util
import sys

# 获取当前目录
current_dir = os.path.dirname(__file__)

# 导入MaskEdgeDetectionNode
try:
    mask_edge_file = os.path.join(current_dir, "mask_edge_detection.py")
    spec = importlib.util.spec_from_file_location("mask_edge_detection", mask_edge_file)
    if spec and spec.loader:
        mask_edge_module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mask_edge_module)
        MaskEdgeDetectionNode = mask_edge_module.MaskEdgeDetectionNode
except Exception as e:
    print(f"导入MaskEdgeDetectionNode失败: {e}")
    MaskEdgeDetectionNode = None

NODE_CLASS_MAPPINGS = {}
NODE_DISPLAY_NAME_MAPPINGS = {}

if MaskEdgeDetectionNode:
    NODE_CLASS_MAPPINGS["MaskEdgeDetection"] = MaskEdgeDetectionNode
    NODE_DISPLAY_NAME_MAPPINGS["MaskEdgeDetection"] = "遮罩边缘检测"

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 