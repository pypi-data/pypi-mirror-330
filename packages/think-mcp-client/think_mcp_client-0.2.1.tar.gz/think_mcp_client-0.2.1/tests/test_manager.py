"""
测试 MCPClientManager 类
"""
import json
from pathlib import Path
import pytest
from unittest.mock import AsyncMock, MagicMock, patch, mock_open

from think_mcp_client.manager import MCPClientManager
from think_mcp_client.client import MCPClient, Prompt, Resource, Tool


@pytest.fixture
def mock_config():
    """模拟配置文件"""
    return {
        "servers": {
            "test-mcp": {
                "command": "python",
                "args": ["-m", "test_server"],
                "env": {}
            }
        }
    }


@pytest.fixture
def manager(mock_config):
    """创建 MCPClientManager 实例"""
    with patch("builtins.open", mock_open(read_data=json.dumps(mock_config))):
        manager = MCPClientManager()
        return manager


@pytest.mark.asyncio
async def test_get_client(manager):
    """测试获取客户端"""
    # 模拟客户端初始化
    mock_client = AsyncMock(spec=MCPClient)
    mock_client.init_client = AsyncMock()
    mock_client.list_prompts = AsyncMock(return_value=[
        Prompt(name="test_prompt", description="测试提示词", arguments=[])
    ])
    mock_client.list_tools = AsyncMock(return_value=[
        Tool(name="test_tool", description="测试工具", input_schema={})
    ])
    mock_client.list_resources = AsyncMock(return_value=[
        Resource(name="test_resource", description="测试资源", uri="test://uri", mime_type="text/plain")
    ])

    manager.clients["test-mcp"] = mock_client
    client = manager.get_client("test-mcp")
    assert client == mock_client

    # 测试获取不存在的客户端
    assert manager.get_client("non-existent") is None


def test_get_all_clients(manager):
    """测试获取所有客户端"""
    mock_client1 = MagicMock(spec=MCPClient)
    mock_client2 = MagicMock(spec=MCPClient)
    
    manager.clients = {
        "test-mcp-1": mock_client1,
        "test-mcp-2": mock_client2
    }
    
    clients = manager.get_all_clients()
    assert len(clients) == 2
    assert clients["test-mcp-1"] == mock_client1
    assert clients["test-mcp-2"] == mock_client2


@pytest.mark.asyncio
async def test_cleanup_all_clients(manager):
    """测试清理所有客户端"""
    mock_client1 = AsyncMock(spec=MCPClient)
    mock_client1.cleanup = AsyncMock()
    mock_client2 = AsyncMock(spec=MCPClient)
    mock_client2.cleanup = AsyncMock()
    
    manager.clients = {
        "test-mcp-1": mock_client1,
        "test-mcp-2": mock_client2
    }
    
    await manager.cleanup_all_clients()
    mock_client1.cleanup.assert_called_once()
    mock_client2.cleanup.assert_called_once()


@pytest.mark.asyncio
async def test_init_all_clients(manager):
    """测试初始化所有客户端"""
    mock_client = AsyncMock(spec=MCPClient)
    mock_client.init_client = AsyncMock()
    
    manager.clients = {"test-mcp": mock_client}
    
    await manager.init_all_clients()
    mock_client.init_client.assert_called_once()


def test_load_config():
    """测试加载配置"""
    config = {
        "servers": {
            "test-mcp": {
                "command": "python",
                "args": ["-m", "test_server"],
                "env": {}
            }
        }
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(config))):
        manager = MCPClientManager()
        assert len(manager.clients) == 1
        assert isinstance(manager.clients["test-mcp"], MCPClient)


def test_load_config_missing_fields():
    """测试加载缺少必要字段的配置"""
    config = {
        "servers": {
            "test-mcp": {
                "command": "python"
                # 缺少 args 字段
            }
        }
    }
    
    with patch("builtins.open", mock_open(read_data=json.dumps(config))):
        manager = MCPClientManager()
        assert len(manager.clients) == 0


def test_load_config_invalid_json():
    """测试加载无效的 JSON 配置"""
    with patch("builtins.open", mock_open(read_data="invalid json")):
        with pytest.raises(json.JSONDecodeError):
            MCPClientManager()


def test_create_default_config():
    """测试创建默认配置"""
    with patch("builtins.open", mock_open()) as mock_file, \
         patch("pathlib.Path.exists", return_value=False), \
         patch("pathlib.Path.mkdir"):
        # 设置第一次读取时返回空字符串，模拟文件不存在
        mock_file.return_value.read.return_value = ""
        MCPClientManager()
        # 检查是否写入了默认配置
        written_content = "".join(call.args[0] for call in mock_file().write.call_args_list)
        assert '{"servers": {}}' in written_content  # 只要确保写入了正确的内容即可
