# 🔀 AI Git Assistant

AI Git助手，支持Commit生成、PR描述、分支管理。

<p align="center">
  <img src="https://img.shields.io/badge/Python-3.10+-blue?logo=python" />
  <img src="https://img.shields.io/badge/OpenAI-API-green?logo=openai" />
  <img src="https://img.shields.io/badge/License-MIT-yellow" />
</p>

## ✨ 特性

- 📝 Commit消息生成
- 📋 PR描述生成
- 🌿 分支名建议
- 🔍 PR代码审查
- 📊 变更日志生成
- 🔧 冲突解决

## 🚀 快速开始

```bash
pip install openai

python tools.py
```

## 📖 使用

```python
from ai_git_assistant import create_tools

tools = create_tools()

# Commit消息
commit = tools.generate_commit_message(diff, "conventional")

# PR描述
pr = tools.generate_pr_description("添加登录功能", changes, ["123"])

# 分支名
branch = tools.suggest_branch_name("添加用户登录功能")

# PR审查
review = tools.review_pr(diff)

# 变更日志
changelog = tools.generate_changelog(commits, "1.0.0")

# 冲突解决
resolved = tools.resolve_conflict(conflict_text)

# .gitignore
gitignore = tools.generate_gitignore("Python")
```

## 📁 项目结构

```
ai-git-assistant/
├── tools.py       # Git助手工具核心
└── README.md
```

## 📄 许可证

MIT License
