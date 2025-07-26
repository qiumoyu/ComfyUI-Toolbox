"""
ComfyUI Mask Edge Detection Plugin
检测遮罩是否处于图像边缘的插件
"""

from .mask_edge_detection import MaskEdgeDetectionNode
from .advanced_mask_analysis import AdvancedMaskAnalysisNode

NODE_CLASS_MAPPINGS = {
    "MaskEdgeDetection": MaskEdgeDetectionNode,
    "AdvancedMaskAnalysis": AdvancedMaskAnalysisNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "MaskEdgeDetection": "遮罩边缘检测",
    "AdvancedMaskAnalysis": "高级遮罩分析"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 