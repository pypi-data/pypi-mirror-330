"""
MCP 客户端 CLI 测试
"""
import json
from pathlib import Path
from typing import Dict, Any
from unittest.mock import patch

import pytest
from prompt_toolkit import PromptSession
from prompt_toolkit.input import create_pipe_input
from prompt_toolkit.output import DummyOutput

from think_mcp_client import MCPClientCLI, Prompt, Tool, Resource


@pytest.fixture
def config_file(tmp_path: Path) -> Path:
    """创建测试配置文件"""
    config = {
        "servers": {
            "default": {
                "command": "echo",
                "args": ["test"],
                "env": {}
            }
        }
    }
    config_path = tmp_path / "config.json"
    with open(config_path, "w") as f:
        json.dump(config, f)
    return config_path


@pytest.fixture
def prompt_session():
    """创建测试用的 PromptSession"""
    pipe_input = create_pipe_input()
    return PromptSession(
        input=pipe_input,
        output=DummyOutput()
    )


@pytest.mark.asyncio
async def test_cli_init(config_file: Path, prompt_session: PromptSession):
    """测试 CLI 初始化"""
    cli = MCPClientCLI(config_file, prompt_session)
    assert cli.command.endswith("echo")  # 使用 endswith 来检查命令名称
    assert cli.args == ["test"]
    assert isinstance(cli.env, dict)
    assert cli.prompt_session == prompt_session


@pytest.mark.asyncio
async def test_cli_display_help(config_file: Path, prompt_session: PromptSession):
    """测试帮助显示"""
    # 模拟 TABLE_STYLE
    with patch("think_mcp_client.cli.TABLE_STYLE", {"panel": "bold"}):
        cli = MCPClientCLI(config_file, prompt_session)
        cli.display_help()  # 不应该抛出异常
