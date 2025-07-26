"""
图像处理插件
提供图像增强、滤波、分割等功能
"""

# 这里将导入图像处理相关的节点
# from .image_enhancement import ImageEnhancementNode
# from .image_filtering import ImageFilteringNode
# from .image_segmentation import ImageSegmentationNode

NODE_CLASS_MAPPINGS = {
    # "ImageEnhancement": ImageEnhancementNode,
    # "ImageFiltering": ImageFilteringNode,
    # "ImageSegmentation": ImageSegmentationNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # "ImageEnhancement": "图像增强",
    # "ImageFiltering": "图像滤波",
    # "ImageSegmentation": "图像分割"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 