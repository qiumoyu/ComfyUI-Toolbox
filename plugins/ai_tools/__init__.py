"""
AI工具插件
提供文本分析、目标检测、风格迁移等功能
"""

# 这里将导入AI工具相关的节点
# from .text_analysis import TextAnalysisNode
# from .object_detection import ObjectDetectionNode
# from .style_transfer import StyleTransferNode

NODE_CLASS_MAPPINGS = {
    # "TextAnalysis": TextAnalysisNode,
    # "ObjectDetection": ObjectDetectionNode,
    # "StyleTransfer": StyleTransferNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # "TextAnalysis": "文本分析",
    # "ObjectDetection": "目标检测",
    # "StyleTransfer": "风格迁移"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 