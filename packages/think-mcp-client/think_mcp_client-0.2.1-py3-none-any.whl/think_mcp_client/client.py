"""
MCP 客户端基类
"""
import asyncio
import logging
import os
import urllib.parse
from contextlib import AsyncExitStack
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client
from think_llm_client.utils.logger import logging

from .utils.command import find_command_path

# 获取项目特定的 logger
logger = logging.getLogger("think-mcp-client")


@dataclass
class Prompt:
    """提示词数据类"""
    name: str
    description: str
    arguments: List[Dict[str, Any]]


@dataclass
class Tool:
    """工具数据类"""
    name: str
    description: str
    input_schema: Dict[str, Any]


@dataclass
class Resource:
    """资源数据类"""
    uri: str
    name: str
    description: str
    mime_type: str


class MCPClient:
    """MCP 客户端基类，负责与 MCP 服务器的基础通信"""

    def __init__(self, command: str, args: List[str], env: Optional[Dict[str, str]] = None):
        # 尝试获取命令的完整路径，如果找不到则使用原始命令
        self.command = find_command_path(command)
        self.args = args or []

        # 确保环境变量中包含基本的系统路径
        self.env = env or {}
        if "PATH" in self.env:
            # 如果已经有 PATH，在前面添加系统路径
            self.env["PATH"] = (
                "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:" + self.env["PATH"]
            )
        else:
            # 如果没有 PATH，使用当前环境的 PATH，并确保包含系统路径
            current_path = os.environ.get("PATH", "")
            self.env["PATH"] = (
                "/opt/homebrew/bin:/usr/local/bin:/usr/bin:/bin:/usr/sbin:/sbin:" + current_path
            )

        self.session: Optional[ClientSession] = None
        self.exit_stack = AsyncExitStack()
        self._cleanup_lock = asyncio.Lock()

    async def init_client(self):
        """初始化与服务器的连接"""
        try:
            server_params = StdioServerParameters(
                command=self.command, args=self.args, env=self.env
            )

            stdio_transport = await self.exit_stack.enter_async_context(stdio_client(server_params))
            read, write = stdio_transport
            self.session = await self.exit_stack.enter_async_context(ClientSession(read, write))
            await self.session.initialize()

        except Exception:
            await self.cleanup()
            raise

    async def list_prompts(self) -> List[Prompt]:
        """获取提示词列表"""
        if not self.session:
            await self.init_client()

        response = await self.session.list_prompts()
        prompts = []

        for item in response:
            if isinstance(item, tuple) and len(item) == 2 and item[0] == "prompts":
                for prompt_data in item[1]:
                    # 确保 arguments 是字典列表
                    arguments = []
                    if hasattr(prompt_data, "arguments"):
                        for arg in prompt_data.arguments:
                            arguments.append(
                                {
                                    "name": arg.name,
                                    "description": arg.description
                                    if hasattr(arg, "description")
                                    else "",
                                }
                            )

                    prompt = Prompt(
                        name=prompt_data.name,
                        description=prompt_data.description,
                        arguments=arguments,
                    )
                    prompts.append(prompt)

        return prompts

    async def get_prompt(self, name: str, arguments: Optional[Dict[str, str]] = None) -> str:
        """获取提示词内容"""
        if not self.session:
            await self.init_client()
            
        # 解码名称中的URL编码字符
        decoded_name = urllib.parse.unquote(name)
        
        result = await self.session.get_prompt(decoded_name, arguments)
        # 返回第一条消息的内容
        if hasattr(result, "messages") and result.messages:
            message = result.messages[0]
            if hasattr(message, "content") and hasattr(message.content, "text"):
                return message.content.text
        return ""

    async def list_tools(self) -> List[Tool]:
        """获取工具列表"""
        if not self.session:
            await self.init_client()

        response = await self.session.list_tools()
        tools = []

        for item in response:
            if isinstance(item, tuple) and len(item) == 2 and item[0] == "tools":
                for tool_data in item[1]:
                    tool = Tool(
                        name=tool_data.name,
                        description=tool_data.description,
                        input_schema=tool_data.inputSchema,
                    )
                    tools.append(tool)

        return tools

    async def call_tool(self, name: str, arguments: Optional[Dict[str, Any]] = None) -> Any:
        """调用工具"""
        if not self.session:
            await self.init_client()
            
        # 解码名称中的URL编码字符
        decoded_name = urllib.parse.unquote(name)
        
        return await self.session.call_tool(decoded_name, arguments or {})

    async def list_resources(self) -> List[Resource]:
        """获取资源列表"""
        if not self.session:
            await self.init_client()

        response = await self.session.list_resources()
        resources = []

        for item in response:
            if isinstance(item, tuple) and len(item) == 2 and item[0] == "resources":
                for resource_data in item[1]:
                    resource = Resource(
                        uri=str(resource_data.uri),
                        name=resource_data.name,
                        description=resource_data.description,
                        mime_type=resource_data.mimeType,
                    )
                    resources.append(resource)

        return resources

    async def read_resource(self, uri: str) -> str:
        """读取资源内容"""
        if not self.session:
            await self.init_client()
            
        # 解码URI中的URL编码字符
        decoded_uri = urllib.parse.unquote(uri)
        
        result = await self.session.read_resource(decoded_uri)
        # 从 ReadResourceResult 中提取文本内容
        if hasattr(result, "contents") and result.contents:
            content = result.contents[0]
            if hasattr(content, "text"):
                return content.text
        return ""

    async def cleanup(self):
        """清理资源"""
        async with self._cleanup_lock:
            try:
                await self.exit_stack.aclose()
                self.session = None
            except Exception as e:
                logger.error(f"Error during cleanup: {e}")

    async def close(self):
        """关闭连接"""
        await self.cleanup()
