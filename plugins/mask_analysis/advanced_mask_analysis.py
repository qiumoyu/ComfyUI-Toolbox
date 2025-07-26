"""
高级遮罩分析节点
提供更详细的遮罩边缘和形状分析
"""

import torch
import numpy as np
import cv2
from scipy import ndimage


class AdvancedMaskAnalysisNode:
    """
    高级遮罩分析节点
    提供边缘检测、形状分析、连通性分析等功能
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
                "analysis_type": (["edge_detection", "shape_analysis", "connectivity", "all"],),
            },
            "optional": {
                "image": ("IMAGE",),
                "min_area": ("INT", {
                    "default": 100, 
                    "min": 1, 
                    "max": 10000, 
                    "step": 1
                }),
            }
        }
    
    RETURN_TYPES = ("BOOLEAN", "STRING", "IMAGE", "FLOAT", "INT")
    RETURN_NAMES = ("has_edge_contact", "analysis_report", "visualization", "coverage_ratio", "num_regions")
    FUNCTION = "analyze_mask"
    CATEGORY = "mask/advanced_analysis"
    
    def analyze_mask(self, mask, threshold=0.1, analysis_type="all", image=None, min_area=100):
        """
        高级遮罩分析
        
        Args:
            mask: 遮罩张量
            threshold: 二值化阈值
            analysis_type: 分析类型
            image: 可选原图像
            min_area: 最小区域面积
            
        Returns:
            has_edge_contact: 是否有边缘接触
            analysis_report: 详细分析报告
            visualization: 可视化结果
            coverage_ratio: 遮罩覆盖率
            num_regions: 连通区域数量
        """
        
        # 预处理遮罩
        binary_mask = self._preprocess_mask(mask, threshold)
        
        # 根据分析类型执行相应分析
        if analysis_type == "edge_detection":
            return self._edge_analysis(binary_mask, image)
        elif analysis_type == "shape_analysis":
            return self._shape_analysis(binary_mask, image, min_area)
        elif analysis_type == "connectivity":
            return self._connectivity_analysis(binary_mask, image, min_area)
        else:  # all
            return self._comprehensive_analysis(binary_mask, image, min_area)
    
    def _preprocess_mask(self, mask, threshold):
        """预处理遮罩"""
        if mask.dim() == 3:
            mask = mask[0]
        
        mask_np = mask.cpu().numpy()
        binary_mask = (mask_np > threshold).astype(np.uint8)
        
        # 形态学操作清理噪声
        kernel = np.ones((3, 3), np.uint8)
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_CLOSE, kernel)
        binary_mask = cv2.morphologyEx(binary_mask, cv2.MORPH_OPEN, kernel)
        
        return binary_mask
    
    def _edge_analysis(self, binary_mask, image):
        """边缘分析"""
        height, width = binary_mask.shape
        
        # 检测边缘接触
        edge_touching = self._detect_edge_contact(binary_mask)
        
        # 计算边缘接触比例
        edge_pixels = self._count_edge_pixels(binary_mask)
        total_pixels = height * width
        edge_ratio = edge_pixels / total_pixels if total_pixels > 0 else 0
        
        # 生成报告
        report = self._generate_edge_report(edge_touching, edge_ratio, height, width)
        
        # 创建可视化
        vis = self._create_edge_visualization(binary_mask, edge_touching, image)
        
        return edge_touching["any_edge"], report, vis, edge_ratio, 1
    
    def _shape_analysis(self, binary_mask, image, min_area):
        """形状分析"""
        # 找到连通区域
        labeled, num_regions = ndimage.label(binary_mask)
        
        # 分析每个区域
        regions_info = []
        for i in range(1, num_regions + 1):
            region_mask = (labeled == i).astype(np.uint8)
            area = np.sum(region_mask)
            
            if area >= min_area:
                # 计算形状特征
                props = self._calculate_shape_properties(region_mask)
                regions_info.append({
                    "id": i,
                    "area": area,
                    "properties": props
                })
        
        # 生成报告
        report = self._generate_shape_report(regions_info, binary_mask.shape)
        
        # 创建可视化
        vis = self._create_shape_visualization(binary_mask, regions_info, image)
        
        # 计算覆盖率
        total_area = np.sum(binary_mask)
        total_pixels = binary_mask.shape[0] * binary_mask.shape[1]
        coverage = total_area / total_pixels if total_pixels > 0 else 0
        
        return len(regions_info) > 0, report, vis, coverage, len(regions_info)
    
    def _connectivity_analysis(self, binary_mask, image, min_area):
        """连通性分析"""
        # 找到连通区域
        labeled, num_regions = ndimage.label(binary_mask)
        
        # 分析连通性
        connectivity_info = self._analyze_connectivity(binary_mask, labeled, num_regions, min_area)
        
        # 生成报告
        report = self._generate_connectivity_report(connectivity_info, binary_mask.shape)
        
        # 创建可视化
        vis = self._create_connectivity_visualization(binary_mask, connectivity_info, image)
        
        # 计算覆盖率
        total_area = np.sum(binary_mask)
        total_pixels = binary_mask.shape[0] * binary_mask.shape[1]
        coverage = total_area / total_pixels if total_pixels > 0 else 0
        
        return connectivity_info["has_large_regions"], report, vis, coverage, connectivity_info["num_large_regions"]
    
    def _comprehensive_analysis(self, binary_mask, image, min_area):
        """综合分析"""
        # 边缘分析
        edge_touching = self._detect_edge_contact(binary_mask)
        
        # 形状分析
        labeled, num_regions = ndimage.label(binary_mask)
        regions_info = []
        for i in range(1, num_regions + 1):
            region_mask = (labeled == i).astype(np.uint8)
            area = np.sum(region_mask)
            
            if area >= min_area:
                props = self._calculate_shape_properties(region_mask)
                regions_info.append({
                    "id": i,
                    "area": area,
                    "properties": props
                })
        
        # 连通性分析
        connectivity_info = self._analyze_connectivity(binary_mask, labeled, num_regions, min_area)
        
        # 生成综合报告
        report = self._generate_comprehensive_report(
            edge_touching, regions_info, connectivity_info, binary_mask.shape
        )
        
        # 创建可视化
        vis = self._create_comprehensive_visualization(
            binary_mask, edge_touching, regions_info, connectivity_info, image
        )
        
        # 计算覆盖率
        total_area = np.sum(binary_mask)
        total_pixels = binary_mask.shape[0] * binary_mask.shape[1]
        coverage = total_area / total_pixels if total_pixels > 0 else 0
        
        return edge_touching["any_edge"], report, vis, coverage, len(regions_info)
    
    def _detect_edge_contact(self, binary_mask):
        """检测边缘接触"""
        height, width = binary_mask.shape
        tolerance = 2
        
        top_edge = np.any(binary_mask[:tolerance, :])
        bottom_edge = np.any(binary_mask[height-tolerance:, :])
        left_edge = np.any(binary_mask[:, :tolerance])
        right_edge = np.any(binary_mask[:, width-tolerance:])
        
        return {
            "any_edge": top_edge or bottom_edge or left_edge or right_edge,
            "top": top_edge,
            "bottom": bottom_edge,
            "left": left_edge,
            "right": right_edge
        }
    
    def _count_edge_pixels(self, binary_mask):
        """计算边缘像素数量"""
        height, width = binary_mask.shape
        tolerance = 2
        
        edge_pixels = 0
        edge_pixels += np.sum(binary_mask[:tolerance, :])
        edge_pixels += np.sum(binary_mask[height-tolerance:, :])
        edge_pixels += np.sum(binary_mask[:, :tolerance])
        edge_pixels += np.sum(binary_mask[:, width-tolerance:])
        
        return edge_pixels
    
    def _calculate_shape_properties(self, region_mask):
        """计算形状属性"""
        # 找到轮廓
        contours, _ = cv2.findContours(region_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        
        if not contours:
            return {}
        
        contour = contours[0]
        
        # 计算各种属性
        area = cv2.contourArea(contour)
        perimeter = cv2.arcLength(contour, True)
        
        # 边界框
        x, y, w, h = cv2.boundingRect(contour)
        
        # 最小外接圆
        (cx, cy), radius = cv2.minEnclosingCircle(contour)
        
        # 椭圆拟合
        if len(contour) >= 5:
            ellipse = cv2.fitEllipse(contour)
        else:
            ellipse = None
        
        # 计算形状因子
        circularity = (4 * np.pi * area) / (perimeter * perimeter) if perimeter > 0 else 0
        aspect_ratio = w / h if h > 0 else 0
        extent = area / (w * h) if w * h > 0 else 0
        
        return {
            "area": area,
            "perimeter": perimeter,
            "circularity": circularity,
            "aspect_ratio": aspect_ratio,
            "extent": extent,
            "bounding_box": (x, y, w, h),
            "center": (cx, cy),
            "radius": radius,
            "ellipse": ellipse
        }
    
    def _analyze_connectivity(self, binary_mask, labeled, num_regions, min_area):
        """分析连通性"""
        large_regions = []
        total_area = 0
        
        for i in range(1, num_regions + 1):
            region_mask = (labeled == i).astype(np.uint8)
            area = np.sum(region_mask)
            total_area += area
            
            if area >= min_area:
                large_regions.append({
                    "id": i,
                    "area": area,
                    "mask": region_mask
                })
        
        return {
            "total_regions": num_regions,
            "num_large_regions": len(large_regions),
            "large_regions": large_regions,
            "total_area": total_area,
            "has_large_regions": len(large_regions) > 0
        }
    
    def _generate_edge_report(self, edge_touching, edge_ratio, height, width):
        """生成边缘分析报告"""
        report = ["=== 边缘分析报告 ==="]
        
        if edge_touching["any_edge"]:
            report.append("✓ 遮罩接触图像边缘")
            edges = []
            if edge_touching["top"]:
                edges.append("上边缘")
            if edge_touching["bottom"]:
                edges.append("下边缘")
            if edge_touching["left"]:
                edges.append("左边缘")
            if edge_touching["right"]:
                edges.append("右边缘")
            report.append(f"接触边缘: {', '.join(edges)}")
        else:
            report.append("✗ 遮罩未接触图像边缘")
        
        report.append(f"边缘像素比例: {edge_ratio:.2%}")
        report.append(f"图像尺寸: {width} x {height}")
        
        return "\n".join(report)
    
    def _generate_shape_report(self, regions_info, image_shape):
        """生成形状分析报告"""
        report = ["=== 形状分析报告 ==="]
        
        if not regions_info:
            report.append("未找到符合条件的区域")
            return "\n".join(report)
        
        report.append(f"发现 {len(regions_info)} 个区域:")
        
        for i, region in enumerate(regions_info):
            props = region["properties"]
            report.append(f"\n区域 {i+1}:")
            report.append(f"  面积: {region['area']} 像素")
            report.append(f"  周长: {props.get('perimeter', 0):.1f}")
            report.append(f"  圆度: {props.get('circularity', 0):.3f}")
            report.append(f"  长宽比: {props.get('aspect_ratio', 0):.2f}")
            report.append(f"  填充度: {props.get('extent', 0):.3f}")
        
        return "\n".join(report)
    
    def _generate_connectivity_report(self, connectivity_info, image_shape):
        """生成连通性分析报告"""
        report = ["=== 连通性分析报告 ==="]
        
        report.append(f"总连通区域数: {connectivity_info['total_regions']}")
        report.append(f"大型区域数: {connectivity_info['num_large_regions']}")
        report.append(f"总遮罩面积: {connectivity_info['total_area']} 像素")
        
        if connectivity_info["large_regions"]:
            report.append("\n大型区域详情:")
            for i, region in enumerate(connectivity_info["large_regions"]):
                report.append(f"  区域 {i+1}: {region['area']} 像素")
        
        return "\n".join(report)
    
    def _generate_comprehensive_report(self, edge_touching, regions_info, connectivity_info, image_shape):
        """生成综合分析报告"""
        report = ["=== 综合分析报告 ==="]
        
        # 边缘信息
        report.append("边缘检测:")
        if edge_touching["any_edge"]:
            report.append("  ✓ 接触图像边缘")
        else:
            report.append("  ✗ 未接触图像边缘")
        
        # 形状信息
        report.append(f"\n形状分析:")
        report.append(f"  有效区域数: {len(regions_info)}")
        if regions_info:
            total_area = sum(r["area"] for r in regions_info)
            report.append(f"  总有效面积: {total_area} 像素")
        
        # 连通性信息
        report.append(f"\n连通性分析:")
        report.append(f"  总连通区域: {connectivity_info['total_regions']}")
        report.append(f"  大型区域: {connectivity_info['num_large_regions']}")
        
        return "\n".join(report)
    
    def _create_edge_visualization(self, binary_mask, edge_touching, image):
        """创建边缘分析可视化"""
        return self._create_basic_visualization(binary_mask, edge_touching, image, "edge")
    
    def _create_shape_visualization(self, binary_mask, regions_info, image):
        """创建形状分析可视化"""
        return self._create_basic_visualization(binary_mask, {}, image, "shape")
    
    def _create_connectivity_visualization(self, binary_mask, connectivity_info, image):
        """创建连通性分析可视化"""
        return self._create_basic_visualization(binary_mask, {}, image, "connectivity")
    
    def _create_comprehensive_visualization(self, binary_mask, edge_touching, regions_info, connectivity_info, image):
        """创建综合分析可视化"""
        return self._create_basic_visualization(binary_mask, edge_touching, image, "comprehensive")
    
    def _create_basic_visualization(self, binary_mask, edge_touching, image, analysis_type):
        """创建基础可视化"""
        height, width = binary_mask.shape
        
        # 创建背景
        if image is not None:
            if image.dim() == 4:
                image = image[0]
            if image.dim() == 3:
                image = image.permute(1, 2, 0)
            
            image_np = (image.cpu().numpy() * 255).astype(np.uint8)
            if image_np.shape[2] == 1:
                image_np = np.repeat(image_np, 3, axis=2)
            
            if image_np.shape[:2] != binary_mask.shape:
                image_np = cv2.resize(image_np, (width, height))
        else:
            image_np = np.ones((height, width, 3), dtype=np.uint8) * 255
        
        # 创建遮罩可视化
        mask_vis = np.zeros((height, width, 3), dtype=np.uint8)
        
        # 遮罩区域用绿色显示
        mask_vis[binary_mask > 0] = [0, 255, 0]
        
        # 根据分析类型添加特殊标记
        if analysis_type == "edge" and edge_touching.get("any_edge", False):
            # 边缘区域用红色标记
            edge_vis = np.zeros_like(binary_mask)
            if edge_touching.get("top", False):
                edge_vis[:2, :] = 1
            if edge_touching.get("bottom", False):
                edge_vis[height-2:, :] = 1
            if edge_touching.get("left", False):
                edge_vis[:, :2] = 1
            if edge_touching.get("right", False):
                edge_vis[:, width-2:] = 1
            
            mask_vis[edge_vis > 0] = [255, 0, 0]
        
        # 混合图像
        alpha = 0.7
        result = cv2.addWeighted(image_np, 1-alpha, mask_vis, alpha, 0)
        
        # 添加边框
        if analysis_type == "edge" and edge_touching.get("any_edge", False):
            cv2.rectangle(result, (0, 0), (width-1, height-1), (0, 0, 255), 3)
        
        # 转换为张量
        result_tensor = torch.from_numpy(result.astype(np.float32) / 255.0)
        result_tensor = result_tensor.permute(2, 0, 1)
        
        return result_tensor