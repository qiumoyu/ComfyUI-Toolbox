"""
遮罩分析插件的单元测试
"""

import pytest
import torch
import numpy as np
import sys
import os

# 添加项目根目录到路径
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..', '..'))

from plugins.mask_analysis.mask_edge_detection import MaskEdgeDetectionNode
from plugins.mask_analysis.advanced_mask_analysis import AdvancedMaskAnalysisNode
from plugins.mask_analysis.mask_utils import MaskUtilsNode


class TestMaskEdgeDetection:
    """测试遮罩边缘检测节点"""
    
    def setup_method(self):
        """设置测试环境"""
        self.node = MaskEdgeDetectionNode()
    
    def test_edge_detection_touching(self):
        """测试接触边缘的遮罩"""
        # 创建接触边缘的遮罩
        mask = torch.zeros((512, 512))
        mask[:10, :] = 1.0  # 上边缘
        mask[:, :10] = 1.0  # 左边缘
        
        result = self.node.detect_mask_edge(mask, threshold=0.1, edge_tolerance=2)
        
        assert result[0] == True  # 应该检测到边缘接触
        assert "遮罩接触图像边缘" in result[1]
        assert "上边缘" in result[1]
        assert "左边缘" in result[1]
    
    def test_edge_detection_not_touching(self):
        """测试不接触边缘的遮罩"""
        # 创建不接触边缘的遮罩
        mask = torch.zeros((512, 512))
        mask[100:200, 100:200] = 1.0  # 中心区域
        
        result = self.node.detect_mask_edge(mask, threshold=0.1, edge_tolerance=2)
        
        assert result[0] == False  # 不应该检测到边缘接触
        assert "遮罩未接触图像边缘" in result[1]
    
    def test_visualization(self):
        """测试可视化功能"""
        mask = torch.zeros((100, 100))
        mask[10:90, 10:90] = 1.0
        
        result = self.node.detect_mask_edge(mask, threshold=0.1, edge_tolerance=2)
        
        # 检查可视化输出
        vis = result[2]
        assert vis.shape == (3, 100, 100)  # CHW格式
        assert vis.dtype == torch.float32


class TestAdvancedMaskAnalysis:
    """测试高级遮罩分析节点"""
    
    def setup_method(self):
        """设置测试环境"""
        self.node = AdvancedMaskAnalysisNode()
    
    def test_edge_analysis(self):
        """测试边缘分析"""
        mask = torch.zeros((100, 100))
        mask[:5, :] = 1.0  # 上边缘
        
        result = self.node.analyze_mask(
            mask, 
            threshold=0.1, 
            analysis_type="edge_detection"
        )
        
        assert result[0] == True  # 有边缘接触
        assert "边缘分析报告" in result[1]
        assert result[3] > 0  # 覆盖率大于0
    
    def test_shape_analysis(self):
        """测试形状分析"""
        mask = torch.zeros((100, 100))
        mask[20:80, 20:80] = 1.0  # 方形区域
        
        result = self.node.analyze_mask(
            mask, 
            threshold=0.1, 
            analysis_type="shape_analysis",
            min_area=100
        )
        
        assert result[0] == True  # 有有效区域
        assert "形状分析报告" in result[1]
        assert result[4] == 1  # 一个区域
    
    def test_connectivity_analysis(self):
        """测试连通性分析"""
        mask = torch.zeros((100, 100))
        mask[20:80, 20:80] = 1.0  # 一个连通区域
        
        result = self.node.analyze_mask(
            mask, 
            threshold=0.1, 
            analysis_type="connectivity",
            min_area=100
        )
        
        assert result[0] == True  # 有大型区域
        assert "连通性分析报告" in result[1]


class TestMaskUtils:
    """测试遮罩工具节点"""
    
    def setup_method(self):
        """设置测试环境"""
        self.node = MaskUtilsNode()
    
    def test_threshold_operation(self):
        """测试阈值操作"""
        mask = torch.rand((100, 100))
        
        result = self.node.process_mask(
            mask, 
            operation="threshold", 
            threshold=0.5
        )
        
        processed_mask = result[0]
        assert processed_mask.shape == (100, 100)
        assert torch.all(processed_mask >= 0) and torch.all(processed_mask <= 1)
    
    def test_invert_operation(self):
        """测试反转操作"""
        mask = torch.ones((100, 100))
        
        result = self.node.process_mask(
            mask, 
            operation="invert"
        )
        
        processed_mask = result[0]
        assert torch.all(processed_mask == 0)  # 全1反转后应该全0
    
    def test_smooth_operation(self):
        """测试平滑操作"""
        mask = torch.rand((100, 100))
        
        result = self.node.process_mask(
            mask, 
            operation="smooth", 
            kernel_size=5
        )
        
        processed_mask = result[0]
        assert processed_mask.shape == (100, 100)


def create_test_mask(size=(100, 100), edge_touching=True):
    """创建测试遮罩"""
    mask = torch.zeros(size)
    
    if edge_touching:
        # 创建接触边缘的遮罩
        mask[:5, :] = 1.0  # 上边缘
        mask[:, :5] = 1.0  # 左边缘
    else:
        # 创建不接触边缘的遮罩
        mask[20:80, 20:80] = 1.0
    
    return mask


if __name__ == "__main__":
    # 运行测试
    pytest.main([__file__, "-v"]) 