"""
工具类插件
提供数据转换、批处理、文件管理等功能
"""

# 这里将导入工具类相关的节点
# from .data_converter import DataConverterNode
# from .batch_processor import BatchProcessorNode
# from .file_manager import FileManagerNode

NODE_CLASS_MAPPINGS = {
    # "DataConverter": DataConverterNode,
    # "BatchProcessor": BatchProcessorNode,
    # "FileManager": FileManagerNode
}

NODE_DISPLAY_NAME_MAPPINGS = {
    # "DataConverter": "数据转换",
    # "BatchProcessor": "批处理",
    # "FileManager": "文件管理"
}

__all__ = ['NODE_CLASS_MAPPINGS', 'NODE_DISPLAY_NAME_MAPPINGS'] 