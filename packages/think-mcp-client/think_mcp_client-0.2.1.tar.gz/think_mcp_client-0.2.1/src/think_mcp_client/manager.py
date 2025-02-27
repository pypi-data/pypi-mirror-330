"""
MCP 客户端管理器
"""
import json
import os
from enum import Enum
from pathlib import Path
from typing import Dict, List, Optional, Type

from think_llm_client.utils.logger import logging
from think_llm_client.utils.terminal_config import TABLE_STYLE, console, box
from rich.table import Table

from .client import MCPClient
from .cli import MCPClientCLI

# 获取项目特定的 logger
logger = logging.getLogger("think-mcp-client")


class ClientType(Enum):
    """MCP 客户端类型"""
    BASE = "base"  # 基础客户端
    CLI = "cli"    # CLI 客户端


class MCPClientManager:
    """MCP 客户端管理器，用于管理多个 MCP 客户端实例"""

    def __init__(
        self,
        config_path: Optional[Path] = None,
        client_type: ClientType = ClientType.BASE
    ):
        """
        初始化 MCP 客户端管理器

        Args:
            config_path: 配置文件路径，默认为 ~/.think-mcp-client/config/mcp_server_config.json
            client_type: 客户端类型，默认为基础客户端
        """
        if config_path is None:
            config_path = Path.home() / ".think-mcp-client" / \
                "config" / "mcp_server_config.json"
            config_path.parent.mkdir(parents=True, exist_ok=True)

        self.config_path = config_path
        self.client_type = client_type
        self.clients: Dict[str, MCPClient] = {}

        # 创建默认配置
        if not self.config_path.exists():
            default_config = {
                "mcpServers": {
                }
            }
            with open(self.config_path, "w") as f:
                json.dump(default_config, f, indent=4)

        self._load_config()

    def _load_config(self) -> None:
        """加载 MCP 服务器配置"""
        try:
            with open(self.config_path) as f:
                config = json.load(f)

            if "mcpServers" not in config:
                raise ValueError("配置文件缺少 'mcpServers' 字段")

            # 根据客户端类型选择要实例化的类
            client_class = MCPClientCLI if self.client_type == ClientType.CLI else MCPClient

            # 创建所有服务器的客户端实例
            for server_name, server_config in config["mcpServers"].items():
                command = server_config.get("command", "")
                args = server_config.get("args", [])
                env = server_config.get("env", {})

                # 创建客户端实例
                self.clients[server_name] = client_class(
                    command=command,
                    args=args,
                    env=env
                )

        except Exception as e:
            logger.error(f"加载 MCP 配置失败: {e}")
            raise

    def get_client(self, server_name: str) -> Optional[MCPClient]:
        """
        获取指定的 MCP 客户端

        Args:
            server_name: 服务器名称

        Returns:
            对应的 MCP 客户端实例，如果不存在则返回 None
        """
        return self.clients.get(server_name)

    def get_all_clients(self) -> Dict[str, MCPClient]:
        """
        获取所有 MCP 客户端

        Returns:
            所有 MCP 客户端实例的字典，key 为服务器名称，value 为客户端实例
        """
        return self.clients

    async def init_all_clients(self) -> None:
        """初始化所有 MCP 客户端"""
        for server_name, client in self.clients.items():
            try:
                await client.init_client()
                logger.info(f"初始化 MCP 客户端 {server_name} 成功")
            except Exception as e:
                logger.error(f"初始化 MCP 客户端 {server_name} 失败: {e}")
                raise

    async def cleanup_all_clients(self) -> None:
        """清理所有 MCP 客户端"""
        for server_name, client in self.clients.items():
            try:
                await client.cleanup()
                logger.info(f"清理 MCP 客户端 {server_name} 成功")
            except Exception as e:
                logger.error(f"清理 MCP 客户端 {server_name} 失败: {e}")

    # 为了兼容性，保留 close_all_clients 方法
    async def close_all_clients(self) -> None:
        """关闭所有 MCP 客户端（cleanup_all_clients 的别名）"""
        await self.cleanup_all_clients()

    async def select_mcp_client(self, prompt_session) -> Optional[MCPClient]:
        """选择 MCP 客户端

        Args:
            prompt_session: PromptSession 实例，用于用户输入

        Returns:
            选中的 MCP 客户端或 None
        """
        try:
            clients = self.get_all_clients()
            if not clients:
                console.print(f"没有可用的 MCP 客户端，请完善配置文件：{self.config_path}", style="red")
                return None

            table = Table(
                title="🖥️  可用的 MCP 客户端列表",
                caption=f"选择一个 MCP客户端来开始使用（可通过配置文件路径：{self.config_path}修改MCP 服务器配置）",
                caption_style="dim",
                title_style="bold magenta",
                box=box.ROUNDED,
                header_style="bold cyan",
                border_style="blue",
                show_lines=True
            )

            table.add_column("序号", justify="right", style="cyan", no_wrap=True)
            table.add_column("服务器名称", style="green")
            table.add_column("命令", style="yellow")
            table.add_column("参数", style="blue")
            table.add_column("环境变量", style="magenta")

            for i, (name, client) in enumerate(clients.items(), 1):
                # 获取客户端配置
                command = client.command if hasattr(client, 'command') else ""
                args = " ".join(client.args) if hasattr(client, 'args') and client.args else ""
                env = "\n".join([f"{k}={v}" for k, v in client.env.items()]) if hasattr(client, 'env') and client.env else ""
                
                table.add_row(
                    str(i),
                    name,
                    command,
                    args,
                    env
                )

            console.print("\n")
            console.print(table)
            console.print("\n")

            # 选择客户端
            client_index = await prompt_session.prompt_async(
                "\n请选择客户端 (输入序号): "
            )

            try:
                idx = int(client_index) - 1  # 转换为从 0 开始的索引
                client = list(clients.values())[idx]
                return client
            except (ValueError, IndexError):
                console.print("无效的客户端序号", style="red")
                return None

        except Exception as e:
            console.print(f"选择 MCP 客户端时发生错误: {e}", style="red")
        return None
