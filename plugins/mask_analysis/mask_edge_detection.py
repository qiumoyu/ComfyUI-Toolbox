"""
遮罩边缘检测节点
检测遮罩是否接触图像边缘
"""

import torch
import numpy as np


class MaskEdgeDetectionNode:
    """
    遮罩边缘检测节点
    输入：遮罩图像
    输出：是否接触边缘的布尔值
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "threshold": ("FLOAT", {
                    "default": 0.1, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.01,
                    "display": "slider"
                }),
                "edge_tolerance": ("INT", {
                    "default": 2, 
                    "min": 0, 
                    "max": 10, 
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("BOOLEAN",)
    RETURN_NAMES = ("is_edge_touching",)
    FUNCTION = "detect_mask_edge"
    CATEGORY = "mask/analysis"
    
    def detect_mask_edge(self, mask, threshold=0.1, edge_tolerance=2):
        """
        检测遮罩是否接触图像边缘
        
        Args:
            mask: 遮罩张量 (H, W) 或 (B, H, W)
            threshold: 遮罩阈值，用于二值化
            edge_tolerance: 边缘容差像素数
            
        Returns:
            is_edge_touching: 是否接触边缘
        """
        
        # 确保遮罩是2D张量
        if mask.dim() == 3:
            mask = mask[0]  # 取第一个批次
        
        # 转换为numpy数组
        mask_np = mask.cpu().numpy()
        
        # 二值化遮罩
        binary_mask = (mask_np > threshold).astype(np.uint8)
        
        # 检测边缘接触
        is_touching = self._check_edge_touching(binary_mask, edge_tolerance)
        
        return (is_touching,)
    
    def _check_edge_touching(self, binary_mask, edge_tolerance):
        """检查遮罩是否接触图像边缘"""
        height, width = binary_mask.shape
        
        # 检查四个边缘
        top_edge = np.any(binary_mask[:edge_tolerance, :])
        bottom_edge = np.any(binary_mask[height-edge_tolerance:, :])
        left_edge = np.any(binary_mask[:, :edge_tolerance])
        right_edge = np.any(binary_mask[:, width-edge_tolerance:])
        
        # 返回是否有任何边缘接触
        return bool(top_edge or bottom_edge or left_edge or right_edge)