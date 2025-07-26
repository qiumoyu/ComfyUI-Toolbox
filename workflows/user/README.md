# 用户自定义工作流

这个目录用于存储用户自定义的工作流文件。

## 使用说明

1. **保存工作流**: 将您在ComfyUI中创建的工作流保存到这个目录
2. **组织管理**: 建议按功能或项目创建子目录进行组织
3. **命名规范**: 使用描述性的文件名，建议包含日期和功能描述
4. **版本控制**: 重要的工作流建议添加版本信息

## 目录组织建议

```
user/
├── project_name/              # 按项目组织
│   ├── workflow_v1.json
│   └── workflow_v2.json
├── feature_name/              # 按功能组织
│   ├── basic_workflow.json
│   └── advanced_workflow.json
└── personal/                  # 个人工作流
    ├── quick_test.json
    └── experiment.json
```

## 最佳实践

- 定期备份重要工作流
- 添加工作流说明文档
- 记录参数设置和预期结果
- 使用版本控制管理重要工作流 