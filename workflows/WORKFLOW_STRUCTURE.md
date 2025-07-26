# 工作流目录结构总结

## 重新规划后的目录结构

```
workflows/
├── README.md                           # 主说明文档
├── WORKFLOW_STRUCTURE.md               # 本结构说明文档
├── templates/                          # 工作流模板
│   ├── mask_analysis/                 # 遮罩分析模板
│   │   ├── basic_edge_detection.json  # 基础边缘检测
│   │   ├── advanced_analysis.json     # 高级分析
│   │   └── mask_preprocessing.json    # 遮罩预处理
│   ├── image_processing/              # 图像处理模板 (预留)
│   │   └── README.md
│   ├── ai_tools/                      # AI工具模板 (预留)
│   │   └── README.md
│   └── utils/                         # 工具类模板 (预留)
│       └── README.md
├── examples/                           # 示例工作流
│   ├── mask_analysis/                 # 遮罩分析示例
│   │   └── edge_detection_demo.json   # 边缘检测演示
│   ├── image_processing/              # 图像处理示例 (预留)
│   └── ai_tools/                      # AI工具示例 (预留)
└── user/                              # 用户自定义工作流
    └── README.md
```

## 重新规划的主要改进

### 1. 清晰的分类结构
- **templates/**: 标准化模板，可重复使用
- **examples/**: 功能演示示例
- **user/**: 用户自定义工作流

### 2. 按功能模块组织
- **mask_analysis/**: 遮罩分析相关
- **image_processing/**: 图像处理相关
- **ai_tools/**: AI工具相关
- **utils/**: 通用工具相关

### 3. 完整的文档体系
- 每个目录都有说明文档
- 详细的使用指南
- 命名规范和最佳实践

## 工作流文件说明

### 遮罩分析模板

#### basic_edge_detection.json
- **功能**: 基础边缘检测
- **节点**: LoadImage, MaskEdgeDetection, PreviewImage
- **用途**: 快速检测遮罩是否接触图像边缘

#### advanced_analysis.json
- **功能**: 高级遮罩分析
- **节点**: LoadImage, MaskUtils, AdvancedMaskAnalysis, PreviewImage, SaveText
- **用途**: 完整的遮罩分析流程，包含预处理和详细报告

#### mask_preprocessing.json
- **功能**: 遮罩预处理
- **节点**: LoadImage, MaskUtils (多步), SaveImage
- **用途**: 遮罩质量优化，包含阈值、形态学、平滑处理

### 示例工作流

#### edge_detection_demo.json
- **功能**: 边缘检测演示
- **节点**: LoadImage, MaskEdgeDetection, PreviewImage, SaveText
- **用途**: 展示基础边缘检测功能的使用方法

## 使用流程

### 1. 选择模板
根据需求选择合适的模板：
- 快速检测 → basic_edge_detection.json
- 深度分析 → advanced_analysis.json
- 质量优化 → mask_preprocessing.json

### 2. 导入工作流
1. 在ComfyUI中点击"Load"
2. 选择对应的JSON文件
3. 调整参数设置
4. 运行工作流

### 3. 自定义修改
1. 基于模板创建新工作流
2. 添加或删除节点
3. 调整参数和连接
4. 保存到user/目录

### 4. 保存和分享
1. 使用描述性文件名
2. 添加版本信息
3. 记录参数设置
4. 分享给其他用户

## 扩展计划

### 短期目标
- 完善遮罩分析模板
- 添加更多示例工作流
- 优化现有工作流

### 中期目标
- 开发图像处理模板
- 创建AI工具模板
- 添加批处理功能

### 长期目标
- 建立工作流库
- 支持工作流版本管理
- 实现工作流自动化

## 维护指南

### 模板维护
- 定期更新模板参数
- 优化节点布局
- 添加新功能支持

### 示例维护
- 更新演示数据
- 完善使用说明
- 添加错误处理

### 文档维护
- 更新使用指南
- 添加新功能说明
- 维护最佳实践

## 贡献指南

### 提交新工作流
1. 确保功能完整可运行
2. 使用标准命名规范
3. 添加必要说明文档
4. 经过测试验证

### 改进现有工作流
1. 保持向后兼容
2. 优化性能表现
3. 改进用户体验
4. 更新相关文档 