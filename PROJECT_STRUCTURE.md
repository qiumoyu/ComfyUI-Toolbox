# ComfyUI-Toolbox 项目结构

## 目录结构

```
ComfyUI-Toolbox/
├── plugins/                          # 插件目录
│   ├── mask_analysis/               # 遮罩分析插件
│   │   ├── __init__.py             # 插件入口文件
│   │   ├── mask_edge_detection.py  # 遮罩边缘检测节点
│   │   ├── advanced_mask_analysis.py # 高级遮罩分析节点
│   │   └── mask_utils.py           # 遮罩工具节点
│   ├── image_processing/           # 图像处理插件 (预留)
│   │   └── __init__.py
│   ├── ai_tools/                   # AI工具插件 (预留)
│   │   └── __init__.py
│   └── utils/                      # 工具类插件 (预留)
│       └── __init__.py
├── workflows/                       # 工作流文件
│   ├── templates/                  # 工作流模板
│   │   └── mask_analysis_template.json
│   ├── examples/                   # 示例工作流
│   └── user/                       # 用户工作流
├── examples/                        # 示例和演示
│   ├── images/                     # 示例图像
│   ├── masks/                      # 示例遮罩
│   └── scripts/                    # 示例脚本
├── tests/                          # 测试文件
│   ├── unit/                       # 单元测试
│   │   └── test_mask_analysis.py
│   ├── integration/                # 集成测试
│   └── fixtures/                   # 测试数据
├── docs/                           # 文档
│   ├── api/                        # API文档
│   ├── tutorials/                  # 教程
│   └── guides/                     # 使用指南
│       └── mask_analysis_guide.md
├── __init__.py                     # 主插件入口
├── setup.py                        # 安装配置
├── pyproject.toml                  # 项目配置
├── requirements.txt                # 依赖包
├── README.md                       # 项目说明
└── PROJECT_STRUCTURE.md            # 项目结构说明
```

## 插件架构

### 1. 主插件入口 (`__init__.py`)
- 动态加载所有子插件
- 统一管理节点映射
- 提供插件注册机制

### 2. 遮罩分析插件 (`plugins/mask_analysis/`)
- **MaskEdgeDetection**: 基础边缘检测
- **AdvancedMaskAnalysis**: 高级分析功能
- **MaskUtils**: 基础工具操作

### 3. 预留插件目录
- **image_processing**: 图像处理功能
- **ai_tools**: AI相关工具
- **utils**: 通用工具类

## 开发规范

### 插件开发
1. 在 `plugins/` 下创建新的插件目录
2. 实现节点类，继承ComfyUI节点规范
3. 在 `__init__.py` 中注册节点
4. 添加相应的测试和文档

### 节点规范
```python
class MyNode:
    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "input_param": ("TYPE", {"default": value}),
            },
            "optional": {
                "optional_param": ("TYPE", {"default": value}),
            }
        }
    
    RETURN_TYPES = ("TYPE1", "TYPE2")
    RETURN_NAMES = ("output1", "output2")
    FUNCTION = "my_function"
    CATEGORY = "category/subcategory"
    
    def my_function(self, input_param, optional_param=None):
        # 实现逻辑
        return output1, output2
```

### 测试规范
- 单元测试放在 `tests/unit/`
- 集成测试放在 `tests/integration/`
- 使用 pytest 框架
- 测试文件命名：`test_*.py`

### 文档规范
- API文档放在 `docs/api/`
- 使用指南放在 `docs/guides/`
- 教程放在 `docs/tutorials/`
- 使用 Markdown 格式

## 扩展指南

### 添加新插件
1. 创建插件目录：`plugins/new_plugin/`
2. 创建 `__init__.py` 文件
3. 实现节点类
4. 注册节点到映射中
5. 添加测试和文档

### 添加新节点
1. 在对应插件目录下创建节点文件
2. 实现节点类
3. 在插件的 `__init__.py` 中导入和注册
4. 添加测试用例

### 添加工作流模板
1. 在 `workflows/templates/` 下创建 JSON 文件
2. 使用 ComfyUI 工作流格式
3. 添加说明文档

## 部署说明

### 安装到 ComfyUI
1. 将整个项目复制到 `ComfyUI/custom_nodes/`
2. 安装依赖：`pip install -r requirements.txt`
3. 重启 ComfyUI

### 开发环境
1. 克隆项目
2. 安装开发依赖：`pip install -e .[dev]`
3. 运行测试：`pytest tests/`

## 版本管理

### 版本号规范
- 主版本号.次版本号.修订号
- 例如：1.0.0, 1.1.0, 1.1.1

### 发布流程
1. 更新版本号
2. 更新 CHANGELOG
3. 创建发布标签
4. 发布到 PyPI (可选)

## 贡献指南

### 代码贡献
1. Fork 项目
2. 创建功能分支
3. 实现功能
4. 添加测试
5. 提交 Pull Request

### 文档贡献
1. 更新相关文档
2. 添加使用示例
3. 修正错误信息

### 问题报告
1. 使用 GitHub Issues
2. 提供详细的问题描述
3. 包含复现步骤
4. 提供环境信息 