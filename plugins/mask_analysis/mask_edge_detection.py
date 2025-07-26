 """
遮罩边缘检测节点
检测遮罩是否接触图像边缘
"""

import torch
import numpy as np
from PIL import Image
import cv2


class MaskEdgeDetectionNode:
    """
    遮罩边缘检测节点
    输入：遮罩图像
    输出：是否接触边缘的布尔值、边缘接触信息、可视化结果
    """
    
    def __init__(self):
        self.output_dir = "output"
        self.type = "output"
        self.output_node = True
    
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
            },
            "optional": {
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("BOOLEAN", "STRING", "IMAGE")
    RETURN_NAMES = ("is_edge_touching", "edge_info", "visualization")
    FUNCTION = "detect_mask_edge"
    CATEGORY = "mask/analysis"
    
    def detect_mask_edge(self, mask, threshold=0.1, edge_tolerance=2, image=None):
        """
        检测遮罩是否接触图像边缘
        
        Args:
            mask: 遮罩张量 (H, W) 或 (B, H, W)
            threshold: 遮罩阈值，用于二值化
            edge_tolerance: 边缘容差像素数
            image: 可选的原图像，用于可视化
            
        Returns:
            is_edge_touching: 是否接触边缘
            edge_info: 边缘接触详细信息
            visualization: 可视化结果图像
        """
        
        # 确保遮罩是2D张量
        if mask.dim() == 3:
            mask = mask[0]  # 取第一个批次
        
        # 转换为numpy数组
        mask_np = mask.cpu().numpy()
        
        # 二值化遮罩
        binary_mask = (mask_np > threshold).astype(np.uint8)
        
        # 获取图像尺寸
        height, width = binary_mask.shape
        
        # 检测边缘接触
        edge_touching = self._check_edge_touching(binary_mask, edge_tolerance)
        
        # 生成详细信息
        edge_info = self._generate_edge_info(edge_touching, height, width)
        
        # 创建可视化
        visualization = self._create_visualization(binary_mask, edge_touching, image)
        
        return edge_touching["any_edge"], edge_info, visualization
    
    def _check_edge_touching(self, binary_mask, edge_tolerance):
        """
        检查遮罩是否接触图像边缘
        
        Args:
            binary_mask: 二值化遮罩
            edge_tolerance: 边缘容差
            
        Returns:
            边缘接触信息字典
        """
        height, width = binary_mask.shape
        
        # 检查四个边缘
        top_edge = np.any(binary_mask[:edge_tolerance, :])
        bottom_edge = np.any(binary_mask[height-edge_tolerance:, :])
        left_edge = np.any(binary_mask[:, :edge_tolerance])
        right_edge = np.any(binary_mask[:, width-edge_tolerance:])
        
        # 检查角落
        top_left = np.any(binary_mask[:edge_tolerance, :edge_tolerance])
        top_right = np.any(binary_mask[:edge_tolerance, width-edge_tolerance:])
        bottom_left = np.any(binary_mask[height-edge_tolerance:, :edge_tolerance])
        bottom_right = np.any(binary_mask[height-edge_tolerance:, width-edge_tolerance:])
        
        return {
            "any_edge": top_edge or bottom_edge or left_edge or right_edge,
            "top": top_edge,
            "bottom": bottom_edge,
            "left": left_edge,
            "right": right_edge,
            "corners": {
                "top_left": top_left,
                "top_right": top_right,
                "bottom_left": bottom_left,
                "bottom_right": bottom_right
            }
        }
    
    def _generate_edge_info(self, edge_touching, height, width):
        """
        生成边缘接触的详细信息
        
        Args:
            edge_touching: 边缘接触信息
            height: 图像高度
            width: 图像宽度
            
        Returns:
            格式化的信息字符串
        """
        info_parts = []
        
        if edge_touching["any_edge"]:
            info_parts.append("遮罩接触图像边缘")
            
            # 具体边缘信息
            edges = []
            if edge_touching["top"]:
                edges.append("上边缘")
            if edge_touching["bottom"]:
                edges.append("下边缘")
            if edge_touching["left"]:
                edges.append("左边缘")
            if edge_touching["right"]:
                edges.append("右边缘")
            
            if edges:
                info_parts.append(f"接触的边缘: {', '.join(edges)}")
            
            # 角落信息
            corner_edges = []
            corners = edge_touching["corners"]
            if corners["top_left"]:
                corner_edges.append("左上角")
            if corners["top_right"]:
                corner_edges.append("右上角")
            if corners["bottom_left"]:
                corner_edges.append("左下角")
            if corners["bottom_right"]:
                corner_edges.append("右下角")
            
            if corner_edges:
                info_parts.append(f"接触的角落: {', '.join(corner_edges)}")
        else:
            info_parts.append("遮罩未接触图像边缘")
        
        info_parts.append(f"图像尺寸: {width} x {height}")
        
        return "\n".join(info_parts)
    
    def _create_visualization(self, binary_mask, edge_touching, image=None):
        """
        创建可视化结果
        
        Args:
            binary_mask: 二值化遮罩
            edge_touching: 边缘接触信息
            image: 可选的原图像
            
        Returns:
            可视化图像张量
        """
        height, width = binary_mask.shape
        
        # 创建彩色可视化
        if image is not None:
            # 使用原图像作为背景
            if image.dim() == 4:
                image = image[0]  # 取第一个批次
            if image.dim() == 3:
                image = image.permute(1, 2, 0)  # CHW -> HWC
            
            # 转换为numpy并归一化到0-255
            image_np = (image.cpu().numpy() * 255).astype(np.uint8)
            if image_np.shape[2] == 1:  # 灰度图转RGB
                image_np = np.repeat(image_np, 3, axis=2)
            
            # 确保尺寸匹配
            if image_np.shape[:2] != binary_mask.shape:
                image_np = cv2.resize(image_np, (width, height))
        else:
            # 创建白色背景
            image_np = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # 创建遮罩可视化
        mask_vis = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 遮罩区域用绿色显示
        mask_vis[binary_mask > 0] = [0, 255, 0]  # 绿色
        
        # 边缘区域用红色高亮
        edge_vis = np.zeros_like(binary_mask)
        if edge_touching["top"]:
            edge_vis[:2, :] = 1
        if edge_touching["bottom"]:
            edge_vis[height-2:, :] = 1
        if edge_touching["left"]:
            edge_vis[:, :2] = 1
        if edge_touching["right"]:
            edge_vis[:, width-2:] = 1
        
        # 边缘区域用红色显示
        mask_vis[edge_vis > 0] = [255, 0, 0]  # 红色
        
        # 混合原图像和遮罩
        alpha = 0.7
        result = cv2.addWeighted(image_np, 1-alpha, mask_vis, alpha, 0)
        
        # 添加边框
        if edge_touching["any_edge"]:
            cv2.rectangle(result, (0, 0), (width-1, height-1), (0, 0, 255), 3)
        
        # 转换为张量
        result_tensor = torch.from_numpy(result.astype(np.float32) / 255.0)
        result_tensor = result_tensor.permute(2, 0, 1)  # HWC -> CHW
        
        return result_tensor