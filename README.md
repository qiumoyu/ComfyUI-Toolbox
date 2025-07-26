 # ComfyUI-Toolbox

一个功能丰富的ComfyUI插件工具箱，提供多种图像处理和AI工具节点。

## 项目结构

```
ComfyUI-Toolbox/
├── plugins/                    # 插件目录
│   ├── mask_analysis/         # 遮罩分析插件
│   ├── image_processing/      # 图像处理插件
│   ├── ai_tools/             # AI工具插件
│   └── utils/                # 工具类插件
├── workflows/                 # 工作流文件
│   ├── examples/             # 示例工作流
│   ├── templates/            # 工作流模板
│   └── user/                 # 用户工作流
├── examples/                  # 示例和演示
│   ├── images/               # 示例图像
│   ├── masks/                # 示例遮罩
│   └── scripts/              # 示例脚本
├── tests/                     # 测试文件
│   ├── unit/                 # 单元测试
│   ├── integration/          # 集成测试
│   └── fixtures/             # 测试数据
├── docs/                      # 文档
│   ├── api/                  # API文档
│   ├── tutorials/            # 教程
│   └── guides/               # 使用指南
├── requirements.txt           # 依赖包
├── setup.py                  # 安装脚本
└── README.md                 # 项目说明
```

## 插件列表

### 1. 遮罩分析插件 (mask_analysis)
- **MaskEdgeDetection**: 基础遮罩边缘检测
- **AdvancedMaskAnalysis**: 高级遮罩形状分析

### 2. 图像处理插件 (image_processing)
- **ImageEnhancement**: 图像增强
- **ImageFiltering**: 图像滤波
- **ImageSegmentation**: 图像分割

### 3. AI工具插件 (ai_tools)
- **TextAnalysis**: 文本分析
- **ObjectDetection**: 目标检测
- **StyleTransfer**: 风格迁移

### 4. 工具类插件 (utils)
- **DataConverter**: 数据转换
- **BatchProcessor**: 批处理
- **FileManager**: 文件管理

## 安装方法

1. 克隆仓库到ComfyUI的`custom_nodes`目录：
```bash
cd ComfyUI/custom_nodes
git clone https://github.com/your-repo/ComfyUI-Toolbox.git
```

2. 安装依赖：
```bash
cd ComfyUI-Toolbox
pip install -r requirements.txt
```

3. 重启ComfyUI

## 使用方法

### 基础使用
1. 在ComfyUI中添加相应的节点
2. 连接输入输出
3. 调整参数
4. 运行工作流

### 工作流模板
- 查看`workflows/templates/`目录中的模板
- 导入到ComfyUI中使用
- 根据需要进行修改

## 开发指南

### 添加新插件
1. 在`plugins/`目录下创建新的插件目录
2. 实现节点类
3. 在`__init__.py`中注册节点
4. 添加测试和文档

### 测试
```bash
python -m pytest tests/
```

### 文档
- API文档在`docs/api/`
- 教程在`docs/tutorials/`
- 使用指南在`docs/guides/`

## 贡献

欢迎提交Issue和Pull Request！

## 许可证

MIT License