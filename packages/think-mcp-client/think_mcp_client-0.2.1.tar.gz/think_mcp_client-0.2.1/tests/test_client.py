"""
MCP 客户端测试
"""
import json
from pathlib import Path
from typing import Dict, Any
from unittest.mock import AsyncMock, MagicMock, patch

import pytest
from mcp import ClientSession

from think_mcp_client import MCPClient, Prompt, Tool, Resource


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


@pytest.mark.asyncio
async def test_client_from_config(config_file: Path):
    """测试从配置文件创建客户端"""
    client = MCPClient.from_config(config_file)
    assert client.command.endswith("echo")
    assert client.args == ["test"]
    assert isinstance(client.env, dict)


@pytest.mark.asyncio
async def test_client_init():
    """测试客户端初始化"""
    client = MCPClient("echo", ["test"])
    assert client.command.endswith("echo")
    assert client.args == ["test"]
    assert isinstance(client.env, dict)
    assert client.session is None


@pytest.mark.asyncio
async def test_client_cleanup():
    """测试客户端清理"""
    client = MCPClient("echo", ["test"])
    await client.cleanup()
    assert client.session is None


@pytest.mark.asyncio
async def test_list_prompts():
    """测试获取提示词列表"""
    client = MCPClient("echo", ["test"])
    
    # 模拟 session 和 list_prompts 响应
    mock_session = AsyncMock()
    mock_prompt = MagicMock()
    mock_prompt.name = "test_prompt"
    mock_prompt.description = "Test prompt"
    mock_prompt.arguments = [MagicMock(name="arg1", description="Test arg")]
    
    mock_session.list_prompts.return_value = [("prompts", [mock_prompt])]
    client.session = mock_session
    
    prompts = await client.list_prompts()
    assert len(prompts) == 1
    assert isinstance(prompts[0], Prompt)
    assert prompts[0].name == "test_prompt"
    assert prompts[0].description == "Test prompt"
    assert len(prompts[0].arguments) == 1


@pytest.mark.asyncio
async def test_list_tools():
    """测试获取工具列表"""
    client = MCPClient("echo", ["test"])
    
    # 模拟 session 和 list_tools 响应
    mock_session = AsyncMock()
    mock_tool = MagicMock()
    mock_tool.name = "test_tool"
    mock_tool.description = "Test tool"
    mock_tool.input_schema = {"type": "object"}
    
    mock_session.list_tools.return_value = [("tools", [mock_tool])]
    client.session = mock_session
    
    tools = await client.list_tools()
    assert len(tools) == 1
    assert isinstance(tools[0], Tool)
    assert tools[0].name == "test_tool"
    assert tools[0].description == "Test tool"
    assert tools[0].input_schema == {"type": "object"}


@pytest.mark.asyncio
async def test_list_resources():
    """测试获取资源列表"""
    client = MCPClient("echo", ["test"])
    
    # 模拟 session 和 list_resources 响应
    mock_session = AsyncMock()
    mock_resource = MagicMock()
    mock_resource.uri = "test://resource"
    mock_resource.name = "test_resource"
    mock_resource.description = "Test resource"
    mock_resource.mime_type = "text/plain"
    
    mock_session.list_resources.return_value = [("resources", [mock_resource])]
    client.session = mock_session
    
    resources = await client.list_resources()
    assert len(resources) == 1
    assert isinstance(resources[0], Resource)
    assert resources[0].uri == "test://resource"
    assert resources[0].name == "test_resource"
    assert resources[0].description == "Test resource"
    assert resources[0].mime_type == "text/plain"


@pytest.mark.asyncio
async def test_init_client():
    """测试客户端初始化连接"""
    client = MCPClient("echo", ["test"])
    
    # 模拟 stdio_client 和 ClientSession
    mock_transport = AsyncMock()
    mock_session = AsyncMock()
    
    with patch("think_mcp_client.client.stdio_client") as mock_stdio_client, \
         patch("think_mcp_client.client.ClientSession") as mock_client_session:
        mock_stdio_client.return_value.__aenter__.return_value = (mock_transport, mock_transport)
        mock_client_session.return_value.__aenter__.return_value = mock_session
        
        await client.init_client()
        assert client.session is not None
        mock_session.initialize.assert_called_once()


@pytest.mark.asyncio
async def test_init_client_error():
    """测试客户端初始化连接失败"""
    client = MCPClient("echo", ["test"])
    
    # 模拟初始化失败
    with patch("think_mcp_client.client.stdio_client") as mock_stdio_client:
        mock_stdio_client.side_effect = Exception("Connection failed")
        
        with pytest.raises(Exception):
            await client.init_client()
        assert client.session is None
