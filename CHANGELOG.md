# 更新日志

本文档记录项目的所有重要变更。

格式基于 [Keep a Changelog](https://keepachangelog.com/zh-CN/1.0.0/),
版本号遵循 [语义化版本](https://semver.org/lang/zh-CN/)。

## [1.0.0] - 2026-02-04

### 新增
- 添加 `.editorconfig` 统一编辑器配置
- 添加 `pyproject.toml` 配置代码格式化和检查工具
- 添加 `.env.example` 环境变量示例文件
- 添加 `requirements-dev.txt` 开发依赖文件
- 添加 `CHANGELOG.md` 变更日志
- 添加 `CONTRIBUTING.md` 贡献指南
- 添加测试框架 (pytest)
- 配置类新增环境变量支持
- 配置类新增 `validate()` 方法验证配置完整性
- 配置类新增 `reload()` 方法重新加载配置
- 启动脚本新增环境检查功能
- 启动脚本新增优雅退出处理

### 改进
- 完善 `.gitignore` 文件,添加更多忽略规则
- 规范化 `requirements.txt`,添加明确版本号和注释
- 优化 `config.py`,添加完整类型注解
- 优化 `Start.py`,改进错误处理和日志输出
- 改进配置文件加载逻辑,不存在时自动创建默认配置
- 环境变量优先级高于配置文件

### 修复
- 修复配置文件不存在时程序崩溃的问题

## [0.9.0] - 2026-02-03

### 初始版本
- 实现基于 WebSocket 的闲鱼消息监听
- 实现自动回复功能
- 实现 Cookie 自动获取和更新
- 实现心跳保活和断线重连
- 支持付款消息自动回复
- 支持对接外部 API
