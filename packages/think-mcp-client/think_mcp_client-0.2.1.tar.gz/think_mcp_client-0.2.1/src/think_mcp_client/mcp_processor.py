"""
MCP 命令处理器，用于处理文本中的 MCP 占位符
"""
import re
import urllib.parse
from typing import Any, Dict, Optional

from prompt_toolkit import PromptSession
from rich.console import Console
from think_llm_client.utils.logger import logging

from .client import MCPClient
from .manager import MCPClientManager

# 获取项目特定的 logger
logger = logging.getLogger("think-mcp-client")
console = Console()


class MCPProcessor:
    """MCP 命令处理器，用于处理文本中的 MCP 占位符"""

    def __init__(
        self, mcp_manager: MCPClientManager, session: Optional[PromptSession] = None
    ) -> None:
        """初始化 MCP 处理器

        Args:
            mcp_manager: MCP 客户端管理器
            session: 提示会话，如果不传入则自动创建一个
        """
        self.mcp_manager = mcp_manager
        self.session = session if session is not None else PromptSession()

    def format_parameters(self, params: dict) -> str:
        """格式化参数为字符串

        Args:
            params: 参数字典

        Returns:
            格式化后的参数字符串
        """
        if not params:
            return ""
        return "{" + ",".join(f"{k}:{v}" for k, v in params.items()) + "}"

    def parse_parameters(self, params_str: Optional[str]) -> Dict[str, str]:
        """解析参数字符串

        Args:
            params_str: 参数字符串

        Returns:
            参数字典
        """
        if not params_str:
            return {}

        # 去掉首尾的花括号
        params_str = params_str.strip("{ }")
        if not params_str:
            return {}

        # 分割参数对
        params = {}
        for pair in params_str.split(","):
            if ":" not in pair:
                continue
            key, value = pair.split(":", 1)
            params[key.strip()] = value.strip()

        return params

    async def _process_pattern(self, text: str, pattern: str, mcp_type: str) -> str:
        """处理文本中的MCP占位符

        Args:
            text: 输入文本
            pattern: 正则表达式模式
            mcp_type: MCP类型

        Returns:
            处理后的文本
        """
        # 查找匹配的占位符
        matches = re.finditer(pattern, text)
        result = text

        for match in matches:
            try:
                # 获取占位符的组成部分
                groups = match.groups()
                client_name = groups[0]
                full_name = groups[1]  # 包含名字和参数的完整字符串

                # 分离名字和参数
                name = full_name
                params = {}
                if "{" in full_name:
                    name = full_name[: full_name.index("{")]
                    params_str = full_name[full_name.index("{") :]
                    params = self.parse_parameters(params_str)

                # 解码名称中的URL编码字符
                decoded_name = urllib.parse.unquote(name)

                # 获取指定的客户端
                client = self.mcp_manager.get_client(client_name)
                if not client:
                    console.print(f"找不到指定的MCP客户端: {client_name}", style="red")
                    continue

                if mcp_type == "resource":
                    content = await client.read_resource(decoded_name)
                    if content:
                        result = result.replace(match.group(), str(content), 1)
                elif mcp_type == "prompt":
                    # 获取prompt列表
                    prompts = await client.list_prompts()
                    prompt = next((p for p in prompts if p.name == decoded_name or p.name == name), None)
                    if prompt:
                        content = await client.get_prompt(decoded_name, params)
                        if content:
                            result = result.replace(match.group(), str(content), 1)
                    else:
                        console.print(f"找不到提示词: {decoded_name}", style="red")
                elif mcp_type == "tool":
                    # 获取tool列表
                    tools = await client.list_tools()
                    tool = next((t for t in tools if t.name == decoded_name or t.name == name), None)
                    if tool:
                        tool_result = await client.call_tool(decoded_name, params)
                        console.print("\n工具原始执行结果：")
                        console.print(tool_result)
                        if tool_result:
                            result = result.replace(
                                match.group(),
                                str(
                                    tool_result.content
                                    if hasattr(tool_result, "content")
                                    else str(tool_result)
                                ),
                                1,
                            )
                    else:
                        console.print(f"找不到工具: {decoded_name}", style="red")

            except Exception as e:
                console.print(f"处理MCP占位符时发生错误: {e}", style="red")
                import traceback

                console.print(traceback.format_exc(), style="red")

        return result

    async def process_text(self, text: str) -> str:
        """处理文本中的MCP占位符

        Args:
            text: 输入文本

        Returns:
            处理后的文本
        """
        # 检查是否包含独立的->mcp（前后有空格）
        mcp_match = re.search(r"(?<=\s)->mcp(?=\s)", text)
        if mcp_match:
            return text

        # 更灵活的占位符匹配
        result = text

        # 处理资源占位符
        resource_pattern = r"->mcp_resources\s*\[([^\]]+)\]\s*:\s*(\S+)"
        result = await self._process_pattern(result, resource_pattern, "resource")

        # 处理提示词占位符
        prompt_pattern = r"->mcp_prompts\s*\[([^\]]+)\]\s*:\s*(\S+)(?:\s*\{([^}]+)\})?"
        result = await self._process_pattern(result, prompt_pattern, "prompt")

        # 处理工具占位符
        tool_pattern = r"->mcp_tools\s*\[([^\]]+)\]\s*:\s*(\S+)(?:\s*\{([^}]+)\})?"
        result = await self._process_pattern(result, tool_pattern, "tool")

        # 如果内容有变化，打印预览
        if result != text:
            # 查找并解码预览中的URL编码字符
            preview_result = result
            
            # 解码所有类型的占位符
            patterns = [resource_pattern, prompt_pattern, tool_pattern]
            for pattern in patterns:
                for match in re.finditer(pattern, result):
                    encoded_name = match.group(2)
                    if '%' in encoded_name:  # 只有当名称包含编码字符时才解码
                        decoded_name = urllib.parse.unquote(encoded_name)
                        # 获取完整的占位符文本
                        full_match = match.group(0)
                        # 构建解码后的占位符
                        decoded_placeholder = full_match.replace(encoded_name, decoded_name)
                        # 替换预览中的占位符（仅用于显示）
                        preview_result = preview_result.replace(full_match, decoded_placeholder)
            
            console.print("\n处理后的内容预览:", style="bold green")
            console.print(preview_result)

        return result

    async def process_mcp_command(self) -> Optional[str]:
        """处理 MCP 命令，返回占位符

        Args:
            session: PromptSession 实例

        Returns:
            格式化的占位符字符串
        """
        try:
            # 选择客户端
            client = await self.mcp_manager.select_mcp_client(self.session)
            if not client:
                return None

            # 获取客户端名称
            clients = self.mcp_manager.get_all_clients()
            client_name = list(clients.keys())[list(clients.values()).index(client)]

            # 选择类型
            choice = await self.session.prompt_async(
                "\n请选择 MCP 类型 (1.Resources 2.Prompts 3.Tools): "
            )

            try:
                choice_num = int(choice)
                if choice_num == 1:  # Resources
                    resource = await client.select_resource()
                    if resource:
                        # 解码URI并用于显示和返回
                        decoded_uri = urllib.parse.unquote(resource.uri)
                        console.print(f"已选择资源: {decoded_uri}", style="green")
                        # 返回解码后的URI，而不是编码的URI
                        return f"->mcp_resources[{client_name}]:{decoded_uri}"
                elif choice_num == 2:  # Prompts
                    prompt, params = await client.select_prompt()
                    if prompt:
                        # 解码名称
                        decoded_name = urllib.parse.unquote(prompt.name)
                        param_str = self.format_parameters(params)
                        console.print(f"已选择提示词: {decoded_name}", style="green")
                        return f"->mcp_prompts[{client_name}]:{decoded_name}{param_str}"
                elif choice_num == 3:  # Tools
                    tool, params = await client.select_tool()
                    if tool:
                        # 解码名称
                        decoded_name = urllib.parse.unquote(tool.name)
                        param_str = self.format_parameters(params)
                        console.print(f"已选择工具: {decoded_name}", style="green")
                        return f"->mcp_tools[{client_name}]:{decoded_name}{param_str}"
                else:
                    console.print("\n无效的选择", style="red")
            except ValueError:
                console.print("\n无效的选择", style="red")

        except Exception as e:
            console.print(f"处理 MCP 命令时发生错误: {e}", style="red")
            import traceback
            console.print(traceback.format_exc(), style="red")
        return None
