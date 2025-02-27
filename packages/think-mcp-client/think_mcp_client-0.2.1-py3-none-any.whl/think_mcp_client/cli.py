"""
MCP 客户端命令行界面
"""
import asyncio
import os
import json
from dataclasses import dataclass
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple
import urllib.parse

from prompt_toolkit import PromptSession
from prompt_toolkit.completion import WordCompleter
from prompt_toolkit.history import FileHistory
from rich.markdown import Markdown
from rich.panel import Panel
from rich.table import Table
from think_llm_client.utils.display import print_markdown
from think_llm_client.utils.logger import logging
from think_llm_client.utils.terminal_config import TABLE_STYLE, console

from .client import MCPClient


# 获取项目特定的 logger
logger = logging.getLogger("think-mcp-client")


@dataclass
class Tool:
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class Prompt:
    name: str
    description: str
    arguments: List[Dict[str, Any]]


@dataclass
class Resource:
    name: str
    description: str
    uri: str
    mime_type: str


class MCPClientCLI(MCPClient):
    """CLI 版本的 MCP 客户端"""

    def __init__(
        self,
        command: str,
        args: List[str],
        env: Optional[Dict[str, str]] = None,
        history_file: Optional[Path] = None,
    ):
        """
        初始化 CLI 版本的 MCP 客户端

        Args:
            command: MCP 服务器命令
            args: 命令参数列表
            env: 环境变量字典
            history_file: 历史记录文件路径
        """
        super().__init__(command, args, env)

        # 设置历史记录文件
        if history_file is None:
            history_file = Path.home() / ".think-mcp-client" / "history" / "cli_history"
            history_file.parent.mkdir(parents=True, exist_ok=True)

        # 初始化命令补全器和提示会话
        self.completer = WordCompleter(
            [" ->mcp "], sentence=True
        )
        self.prompt_session = PromptSession(
            history=FileHistory(str(history_file)),
            completer=self.completer,
            complete_while_typing=True,
        )

    async def collect_prompt_arguments(self, prompt: Prompt) -> Dict[str, Any]:
        """收集提示词参数

        Args:
            prompt: 提示词对象

        Returns:
            参数字典
        """
        arguments = {}
        if prompt.arguments:
            console.print("\n请输入参数值：", style=TABLE_STYLE["green"])
            for arg in prompt.arguments:
                name = arg["name"]
                description = arg.get("description", "")
                prompt_text = f"{name}"
                if description:
                    prompt_text += f" ({description})"
                value = await self.prompt_session.prompt_async(prompt_text + ": ")
                arguments[name] = value
        return arguments

    async def collect_tool_arguments(self, tool: Tool) -> Dict[str, Any]:
        """收集工具参数

        Args:
            tool: 工具对象

        Returns:
            参数字典
        """
        arguments = {}
        if tool.input_schema and "properties" in tool.input_schema:
            console.print("\n请输入参数值：", style=TABLE_STYLE["green"])
            for param_name, param_info in tool.input_schema["properties"].items():
                param_type = param_info.get("type", "string")
                description = param_info.get("description", "")
                default = param_info.get("default")
                required = param_name in tool.input_schema.get("required", [])

                # 构建提示文本
                prompt_text = f"{param_name} ({param_type}"
                if description:
                    prompt_text += f", {description}"
                if required:
                    prompt_text += ", 必填"
                prompt_text += ")"

                # 获取用户输入
                prompt_with_default = f"{prompt_text} [{default}]: " if default is not None else f"{prompt_text}: "
                value = await self.prompt_session.prompt_async(prompt_with_default)

                # 如果输入为空且有默认值，使用默认值
                if not value and default is not None:
                    value = default

                # 根据类型转换值
                try:
                    if param_type == "integer":
                        arguments[param_name] = int(value) if value else default
                    elif param_type == "number":
                        arguments[param_name] = float(value) if value else default
                    elif param_type == "boolean":
                        if not value:
                            arguments[param_name] = default
                        else:
                            value = value.lower()
                            arguments[param_name] = value in ("true", "1", "yes", "y", "t")
                    else:  # string 或其他类型
                        arguments[param_name] = value if value else default
                except (ValueError, TypeError) as e:
                    console.print(f"参数 {param_name} 的值 '{value}' 无法转换为 {param_type} 类型", style="red")
                    if required:
                        raise ValueError(f"参数 {param_name} 是必填项且必须是 {param_type} 类型") from e
                    arguments[param_name] = default if default is not None else value

        return arguments

    async def select_and_run_tool(self, tools: List[Tool]) -> Optional[str]:
        """选择并运行工具"""
        if not tools:
            console.print("\n没有可用的工具", style="yellow")
            return None

        # 显示工具列表
        self.display_tools(tools)

        # 让用户选择工具
        choice = await self.prompt_session.prompt_async("\n请选择要使用的工具 (输入序号): ")
        try:
            index = int(choice) - 1
            if 0 <= index < len(tools):
                selected_tool = tools[index]

                # 收集工具参数
                arguments = await self.collect_tool_arguments(selected_tool)

                # 调用工具
                result = await self.call_tool(selected_tool.name, arguments)
                console.print("\n工具执行结果：")
                console.print(result)
                return result

        except (ValueError, IndexError) as e:
            console.print(f"\n选择无效: {e}", style="red")
        except Exception as e:
            console.print(f"\n执行工具时发生错误: {e}", style="red")

        return None

    def display_prompts(self, prompts: List[Prompt]) -> None:
        """显示提示词列表"""
        if not prompts:
            console.print("没有找到可用的提示词", style=TABLE_STYLE["warning"])
            return

        table = Table(
            title="可用的提示词",
            box=TABLE_STYLE["box"],
            show_lines=TABLE_STYLE["show_lines"],
            header_style=TABLE_STYLE["table.header"],
            border_style=TABLE_STYLE["table.border"],
            title_style=TABLE_STYLE["table.title"],
        )
        table.add_column("序号", justify="right", style=TABLE_STYLE["cyan"], no_wrap=True, width=4)
        table.add_column("名称", style=TABLE_STYLE["green"], min_width=20, max_width=30)
        table.add_column("描述", style=TABLE_STYLE["blue"], ratio=2)
        table.add_column("参数", style=TABLE_STYLE["magenta"])

        for i, prompt in enumerate(prompts, 1):
            # 解码提示词名称中的URL编码字符
            decoded_name = prompt.name
            if '%' in prompt.name:
                decoded_name = urllib.parse.unquote(prompt.name)
                
            # 格式化参数列表
            args_str = ", ".join(arg["name"] for arg in prompt.arguments) if prompt.arguments else ""
            
            table.add_row(
                str(i),
                decoded_name,
                prompt.description or "",
                args_str,
            )

        console.print(table)

    def display_resources(self, resources: List[Resource]) -> None:
        """显示资源列表"""
        if not resources:
            console.print("没有找到可用的资源", style=TABLE_STYLE["warning"])
            return

        table = Table(
            title="可用的资源",
            box=TABLE_STYLE["box"],
            show_lines=TABLE_STYLE["show_lines"],
            header_style=TABLE_STYLE["table.header"],
            border_style=TABLE_STYLE["table.border"],
            title_style=TABLE_STYLE["table.title"],
        )
        table.add_column("序号", justify="right", style=TABLE_STYLE["cyan"], no_wrap=True, width=4)
        table.add_column("名称", style=TABLE_STYLE["green"], min_width=20, max_width=30)
        table.add_column("描述", style=TABLE_STYLE["blue"], ratio=2)
        table.add_column("MIME类型", style=TABLE_STYLE["magenta"], no_wrap=True)

        for i, resource in enumerate(resources, 1):
            # 解码资源名称中的URL编码字符
            decoded_name = resource.name
            if '%' in resource.name:
                decoded_name = urllib.parse.unquote(resource.name)
                
            # 解码URI中的URL编码字符
            decoded_uri = resource.uri
            if '%' in resource.uri:
                decoded_uri = urllib.parse.unquote(resource.uri)
                
            # 从URI中提取文件名作为备用名称
            if decoded_name == resource.name and '/' in decoded_uri:
                filename = decoded_uri.split('/')[-1]
                if filename and filename != decoded_name:
                    decoded_name = filename
                
            table.add_row(
                str(i),
                decoded_name,
                resource.description or "",
                resource.mime_type or "",
            )

        console.print(table)

    def display_tools(self, tools: List[Tool]) -> None:
        """显示工具列表"""
        if not tools:
            console.print("没有找到可用的工具", style=TABLE_STYLE["warning"])
            return

        table = Table(
            title="可用的工具",
            box=TABLE_STYLE["box"],
            show_lines=TABLE_STYLE["show_lines"],
            header_style=TABLE_STYLE["table.header"],
            border_style=TABLE_STYLE["table.border"],
            title_style=TABLE_STYLE["table.title"],
        )
        table.add_column("序号", justify="right", style=TABLE_STYLE["cyan"], no_wrap=True, width=4)
        table.add_column("名称", style=TABLE_STYLE["green"], min_width=20, max_width=30)
        table.add_column("描述", style=TABLE_STYLE["blue"], ratio=2)

        for i, tool in enumerate(tools, 1):
            # 解码工具名称中的URL编码字符
            decoded_name = tool.name
            if '%' in tool.name:
                decoded_name = urllib.parse.unquote(tool.name)
                
            table.add_row(
                str(i),
                decoded_name,
                tool.description or "",
            )

        console.print(table)

    async def select_prompt(self) -> Tuple[Optional[Prompt], Dict[str, Any]]:
        """选择提示词

        Returns:
            提示词对象和参数字典的元组，或 (None, {})
        """
        # 获取提示词列表
        prompts = await self.list_prompts()
        if not prompts:
            console.print("没有可用的提示词", style="red")
            return None, {}

        # 显示提示词列表
        self.display_prompts(prompts)

        # 选择提示词
        prompt_index = await self.prompt_session.prompt_async(
            "请选择提示词 (输入序号): "
        )

        try:
            idx = int(prompt_index) - 1  # 转换为从 0 开始的索引
            prompt = prompts[idx]
            arguments = await self.collect_prompt_arguments(prompt)
            return prompt, arguments
        except (ValueError, IndexError):
            console.print("无效的提示词序号", style="red")
            return None, {}

    async def select_resource(self) -> Optional[Resource]:
        """选择资源

        Returns:
            选中的资源对象或 None
        """
        # 获取资源列表
        resources = await self.list_resources()
        if not resources:
            console.print("没有可用的资源", style="red")
            return None

        # 显示资源列表
        self.display_resources(resources)

        # 选择资源
        resource_index = await self.prompt_session.prompt_async(
            "请选择资源 (输入序号): "
        )

        try:
            idx = int(resource_index) - 1  # 转换为从 0 开始的索引
            return resources[idx]
        except (ValueError, IndexError):
            console.print("无效的资源序号", style="red")
            return None

    async def select_tool(self) -> Tuple[Optional[Tool], Dict[str, Any]]:
        """选择工具

        Returns:
            工具对象和参数字典的元组，或 (None, {})
        """
        # 获取工具列表
        tools = await self.list_tools()
        if not tools:
            console.print("没有可用的工具", style="red")
            return None, {}

        # 显示工具列表
        self.display_tools(tools)

        # 选择工具
        tool_index = await self.prompt_session.prompt_async(
            "请选择工具 (输入序号): "
        )

        try:
            idx = int(tool_index) - 1  # 转换为从 0 开始的索引
            tool = tools[idx]
            console.print(f"\n选择的工具：{tool.name}",style=TABLE_STYLE["green"])
            logger.info(f"选择的工具：{tool.name}")
            arguments = await self.collect_tool_arguments(tool)
            return tool, arguments
        except (ValueError, IndexError):
            console.print("无效的工具序号", style="red")
            return None, {}
