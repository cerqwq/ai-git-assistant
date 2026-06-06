"""
AI Git Assistant - AI Git助手
支持Commit生成、PR描述、分支管理
"""

import json
import os
from typing import Dict, List, Any
from datetime import datetime

try:
    from openai import OpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False


class AIGitAssistantTools:
    """
    AI Git助手
    支持：Commit、PR、分支
    """

    def __init__(self, model: str = "mimo-v2.5-pro", api_key: str = None, base_url: str = None):
        self.model = model
        if OPENAI_AVAILABLE:
            self.client = OpenAI(
                api_key=api_key or os.environ.get('OPENAI_API_KEY', ''),
                base_url=base_url or os.environ.get('OPENAI_BASE_URL', 'https://api.xiaomimimo.com/v1')
            )
        else:
            self.client = None

    def generate_commit_message(self, diff: str, style: str = "conventional") -> str:
        """生成Commit消息"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请根据以下代码变更生成{style}风格的commit消息：

{diff[:2000]}

要求：
1. 简洁明了
2. 描述变更内容
3. 使用{style}格式"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=200
        )

        return response.choices[0].message.content

    def generate_pr_description(self, title: str, changes: str, issues: List[str] = None) -> str:
        """生成PR描述"""
        if not self.client:
            return "LLM客户端未配置"

        issues_text = ", ".join(f"#{i}" for i in (issues or []))

        prompt = f"""请生成Pull Request描述：

标题：{title}
变更：{changes[:1000]}
{f'相关Issue：{issues_text}' if issues_text else ''}

要求：
1. 变更概述
2. 具体改动
3. 测试说明"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def suggest_branch_name(self, task: str) -> str:
        """建议分支名"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为以下任务建议Git分支名：

{task}

要求：
1. 小写字母和连字符
2. 类型前缀（feature/fix/refactor）
3. 简洁明了

只返回分支名："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=50
        )

        return response.choices[0].message.content

    def review_pr(self, diff: str) -> Dict:
        """审查PR"""
        if not self.client:
            return {"error": "LLM客户端未配置"}

        prompt = f"""请审查以下Pull Request的代码变更：

{diff[:2000]}

请返回JSON格式：
{{
    "summary": "总结",
    "issues": [
        {{"severity": "high/medium/low", "description": "问题", "suggestion": "建议"}}
    ],
    "positive": ["亮点"],
    "approval": "approve/request_changes/comment"
}}"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        try:
            content = response.choices[0].message.content
            import re
            json_match = re.search(r'\{.*\}', content, re.DOTALL)
            if json_match:
                return json.loads(json_match.group())
        except:
            pass

        return {"review": content}

    def generate_changelog(self, commits: List[str], version: str) -> str:
        """生成变更日志"""
        if not self.client:
            return "LLM客户端未配置"

        commits_text = "\n".join(f"- {c}" for c in commits[:20])

        prompt = f"""请根据以下commits生成CHANGELOG：

版本：{version}
Commits：
{commits_text}

使用Keep a Changelog格式："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content

    def resolve_conflict(self, conflict: str) -> str:
        """解决冲突"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请帮助解决以下Git冲突：

{conflict[:2000]}

请提供解决后的代码："""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=2000
        )

        return response.choices[0].message.content

    def generate_gitignore(self, project_type: str) -> str:
        """生成.gitignore"""
        if not self.client:
            return "LLM客户端未配置"

        prompt = f"""请为{project_type}项目生成.gitignore文件：

要求：
1. 通用忽略
2. IDE文件
3. 依赖目录
4. 构建产物"""

        response = self.client.chat.completions.create(
            model=self.model,
            messages=[{"role": "user", "content": prompt}],
            max_tokens=1000
        )

        return response.choices[0].message.content


def create_tools(**kwargs) -> AIGitAssistantTools:
    """创建Git助手工具"""
    return AIGitAssistantTools(**kwargs)


if __name__ == "__main__":
    tools = create_tools()

    print("AI Git Assistant Tools")
    print()

    # 测试
    branch = tools.suggest_branch_name("添加用户登录功能")
    print(f"Branch: {branch}")
