from .client import MCPClient, Prompt, Resource, Tool
from .cli import MCPClientCLI
from .manager import ClientType, MCPClientManager
from .mcp_processor import MCPProcessor
from think_llm_client.utils.logger import setup_logger

# 初始化项目特定的日志配置
setup_logger("think-mcp-client")

__all__ = [
    "MCPClientManager",
    "ClientType",
    "MCPClient",
    "MCPClientCLI",
    "Prompt",
    "Tool",
    "Resource"
]
