# 贡献指南

感谢您对闲鱼自动回复系统的关注！我们欢迎任何形式的贡献。

## 开发环境设置

### 1. 克隆仓库

```bash
git clone https://github.com/IAMLZY2018/xianyuapis.git
cd xianyu
```

### 2. 创建虚拟环境

```bash
python -m venv venv
source venv/bin/activate  # Linux/macOS
# 或
venv\Scripts\activate  # Windows
```

### 3. 安装依赖

```bash
# 安装生产依赖
pip install -r requirements.txt

# 安装开发依赖
pip install -r requirements-dev.txt

# 安装 Playwright 浏览器
playwright install chromium
```

### 4. 配置环境

复制 `.env.example` 为 `.env` 并根据需要修改配置:

```bash
cp .env.example .env
```

## 代码规范

### 代码风格

本项目使用以下工具确保代码质量:

- **Black**: 代码格式化
- **isort**: 导入语句排序
- **flake8**: 代码检查
- **mypy**: 类型检查

### 运行代码检查

```bash
# 格式化代码
black .
isort .

# 检查代码
flake8 .
mypy config.py utils/
```

### 代码规范要求

1. **类型注解**: 所有函数都应添加类型注解
2. **文档字符串**: 所有公共函数和类都应有文档字符串
3. **行长度**: 最大 120 字符
4. **命名规范**:
   - 类名: `PascalCase`
   - 函数/变量: `snake_case`
   - 常量: `UPPER_CASE`

## 提交规范

### Commit 消息格式

使用以下格式编写 commit 消息:

```
<类型>: <简短描述>

<详细描述>

<相关 Issue>
```

**类型**:
- `feat`: 新功能
- `fix`: 修复 bug
- `docs`: 文档更新
- `style`: 代码格式调整
- `refactor`: 代码重构
- `test`: 测试相关
- `chore`: 构建/工具相关

**示例**:
```
feat: 添加环境变量支持

- 配置类支持从环境变量读取配置
- 环境变量优先级高于配置文件
- 添加 .env.example 示例文件

Closes #123
```

## 测试

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_config.py

# 查看覆盖率
pytest --cov --cov-report=html
```

### 编写测试

- 所有新功能都应包含测试
- 测试文件放在 `tests/` 目录
- 测试函数以 `test_` 开头
- 使用 pytest fixtures 共享测试数据

## Pull Request 流程

1. **Fork 项目**到您的账号
2. **创建特性分支**: `git checkout -b feature/amazing-feature`
3. **提交更改**: `git commit -m 'feat: add amazing feature'`
4. **推送分支**: `git push origin feature/amazing-feature`
5. **创建 Pull Request**

### PR 检查清单

- [ ] 代码通过所有检查 (black, flake8, mypy)
- [ ] 添加了必要的测试
- [ ] 更新了相关文档
- [ ] Commit 消息符合规范
- [ ] 没有合并冲突

## 报告问题

发现 bug 或有功能建议?请创建 Issue 并包含:

1. **问题描述**: 清晰描述问题或建议
2. **复现步骤**: 如何复现问题 (如果是 bug)
3. **期望行为**: 您期望的结果
4. **环境信息**: 
   - Python 版本
   - 操作系统
   - 相关依赖版本

## 行为准则

- 尊重所有贡献者
- 接受建设性批评
- 关注对项目最有利的事情
- 保持友好和专业

## 许可证

贡献代码即表示您同意将代码以 MIT 许可证发布。

---

再次感谢您的贡献! 🎉
