"""
遮罩工具节点
提供遮罩处理的基础工具功能
"""

import torch
import numpy as np
import cv2


class MaskUtilsNode:
    """
    遮罩工具节点
    提供遮罩的预处理、后处理等基础功能
    """
    
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "mask": ("MASK",),
                "operation": (["threshold", "morphology", "smooth", "resize", "invert"],),
                "threshold": ("FLOAT", {
                    "default": 0.5, 
                    "min": 0.0, 
                    "max": 1.0, 
                    "step": 0.01,
                    "display": "slider"
                }),
            },
            "optional": {
                "kernel_size": ("INT", {
                    "default": 3, 
                    "min": 1, 
                    "max": 21, 
                    "step": 2
                }),
                "iterations": ("INT", {
                    "default": 1, 
                    "min": 1, 
                    "max": 10, 
                    "step": 1
                }),
                "target_size": ("STRING", {
                    "default": "512,512",
                    "multiline": False
                }),
            }
        }
    
    RETURN_TYPES = ("MASK", "IMAGE")
    RETURN_NAMES = ("processed_mask", "visualization")
    FUNCTION = "process_mask"
    CATEGORY = "mask/utils"
    
    def process_mask(self, mask, operation, threshold=0.5, kernel_size=3, iterations=1, target_size="512,512"):
        """处理遮罩"""
        # 确保遮罩是2D张量
        if mask.dim() == 3:
            mask = mask[0]
        
        # 转换为numpy数组
        mask_np = mask.cpu().numpy()
        
        # 根据操作类型处理遮罩
        if operation == "threshold":
            processed_mask = self._apply_threshold(mask_np, threshold)
        elif operation == "morphology":
            processed_mask = self._apply_morphology(mask_np, kernel_size, iterations)
        elif operation == "smooth":
            processed_mask = self._apply_smoothing(mask_np, kernel_size)
        elif operation == "resize":
            processed_mask = self._apply_resize(mask_np, target_size)
        elif operation == "invert":
            processed_mask = self._apply_invert(mask_np)
        else:
            processed_mask = mask_np
        
        # 创建可视化
        visualization = self._create_visualization(processed_mask)
        
        # 转换回张量
        processed_tensor = torch.from_numpy(processed_mask.astype(np.float32))
        
        return processed_tensor, visualization
    
    def _apply_threshold(self, mask, threshold):
        """应用阈值"""
        return (mask > threshold).astype(np.float32)
    
    def _apply_morphology(self, mask, kernel_size, iterations):
        """应用形态学操作"""
        # 二值化
        binary_mask = (mask > 0.5).astype(np.uint8)
        
        # 创建核
        kernel = np.ones((kernel_size, kernel_size), np.uint8)
        
        # 开运算和闭运算
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel, iterations=iterations)
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel, iterations=iterations)
        
        return binary_mask.astype(np.float32)
    
    def _apply_smoothing(self, mask, kernel_size):
        """应用平滑"""
        # 高斯模糊
        smoothed = cv2.GaussianBlur(mask, (kernel_size, kernel_size), 0)
        return smoothed.astype(np.float32)
    
    def _apply_resize(self, mask, target_size):
        """应用尺寸调整"""
        try:
            # 解析目标尺寸
            width, height = map(int, target_size.split(','))
            
            # 调整尺寸
            resized = cv2.resize(mask, (width, height), interpolation=cv2.INTER_LINEAR)
            return resized.astype(np.float32)
        except:
            # 如果解析失败，返回原尺寸
            return mask.astype(np.float32)
    
    def _apply_invert(self, mask):
        """应用反转"""
        return (1.0 - mask).astype(np.float32)
    
    def _create_visualization(self, mask):
        """创建可视化"""
        height, width = mask.shape
        
        # 创建彩色可视化
        vis = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 遮罩区域用绿色显示
        vis[mask > 0.5] = [0, 255, 0]
        
        # 转换为张量
        vis_tensor = torch.from_numpy(vis.astype(np.float32) / 255.0)
        vis_tensor = vis_tensor.permute(2, 0, 1)  # HWC -> CHW
        
        return vis_tensor 