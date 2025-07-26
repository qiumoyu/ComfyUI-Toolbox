"""
遮罩分析插件
提供遮罩边缘检测和形状分析功能
"""

from .mask_edge_detection import MaskEdgeDetectionNode
from .advanced_mask_analysis import AdvancedMaskAnalysisNode
from .mask_utils import MaskUtilsNode

NODE_CLASS_MAPPINGS = {
    "MaskEdgeDetection": MaskEdgeDetectionNode,
    "AdvancedMaskAnalysis": AdvancedMaskAnalysisNode,
    "MaskUtils": MaskUtilsNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskEdgeDetection": "遮罩边缘检测",
    "AdvancedMaskAnalysis": "高级遮罩分析",
    "MaskUtils": "遮罩工具"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 