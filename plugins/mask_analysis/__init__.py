"""
遮罩分析插件
提供遮罩边缘检测功能
"""

from .mask_edge_detection import MaskEdgeDetectionNode

NODE_CLASS_MAPPINGS = {
    "MaskEdgeDetection": MaskEdgeDetectionNode,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskEdgeDetection": "遮罩边缘检测",
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 