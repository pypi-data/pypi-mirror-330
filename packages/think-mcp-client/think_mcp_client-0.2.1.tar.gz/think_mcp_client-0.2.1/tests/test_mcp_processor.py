"""
测试 MCPProcessor 类
"""
import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from prompt_toolkit import prompt
from think_mcp_client.mcp_processor import MCPProcessor
from think_mcp_client.client import MCPClient, Prompt, Resource, Tool


@pytest.fixture
def mock_manager():
    """创建模拟的 MCPClientManager"""
    manager = MagicMock()
    mock_client = AsyncMock(spec=MCPClient)
    mock_client.name = "test-mcp"
    mock_client.list_prompts = AsyncMock(return_value=[
        Prompt(name="test_prompt", description="测试提示词", arguments=[])
    ])
    mock_client.list_tools = AsyncMock(return_value=[
        Tool(name="test_tool", description="测试工具", input_schema={})
    ])
    mock_client.list_resources = AsyncMock(return_value=[
        Resource(name="test_resource", description="测试资源", uri="test://uri", mime_type="text/plain")
    ])
    mock_client.display_prompts = AsyncMock()
    mock_client.display_tools = AsyncMock()
    mock_client.display_resources = AsyncMock()
    manager.get_client.return_value = mock_client
    manager.get_all_clients.return_value = {"test-mcp": mock_client}
    return manager


@pytest.fixture
def processor(mock_manager):
    """创建 MCPProcessor 实例"""
    return MCPProcessor(mock_manager)


@pytest.mark.asyncio
async def test_select_mcp_client(processor, mock_manager):
    """测试选择 MCP 客户端"""
    # 模拟用户输入选择客户端
    processor.session.prompt_async = AsyncMock(return_value="1")
    client = await processor.select_mcp_client()
    assert client == mock_manager.get_all_clients()["test-mcp"]


@pytest.mark.asyncio
async def test_select_prompt(processor, mock_manager):
    """测试选择提示词"""
    mock_client = mock_manager.get_client.return_value
    prompt = Prompt(name="test_prompt", description="测试提示词", arguments=[])
    mock_client.list_prompts = AsyncMock(return_value=[prompt])
    
    # 模拟用户输入选择提示词
    processor.session.prompt_async = AsyncMock(return_value="1")
    prompt_obj, params = await processor.select_prompt(mock_client)
    assert prompt_obj == prompt
    assert params == {}


@pytest.mark.asyncio
async def test_select_tool(processor, mock_manager):
    """测试选择工具"""
    mock_client = mock_manager.get_client.return_value
    tool = Tool(name="test_tool", description="测试工具", input_schema={})
    mock_client.list_tools = AsyncMock(return_value=[tool])
    
    # 模拟用户输入选择工具
    processor.session.prompt_async = AsyncMock(return_value="1")
    tool_obj, params = await processor.select_tool(mock_client)
    assert tool_obj == tool
    assert params == {}


@pytest.mark.asyncio
async def test_select_resource(processor, mock_manager):
    """测试选择资源"""
    mock_client = mock_manager.get_client.return_value
    resource = Resource(name="test_resource", description="测试资源", uri="test://uri", mime_type="text/plain")
    mock_client.list_resources = AsyncMock(return_value=[resource])
    
    # 模拟用户输入选择资源
    processor.session.prompt_async = AsyncMock(return_value="1")
    resource_obj = await processor.select_resource(mock_client)
    assert resource_obj == resource


@pytest.mark.asyncio
async def test_format_parameters(processor):
    """测试参数格式化"""
    params = {"key1": "value1", "key2": "value2"}
    result = processor.format_parameters(params)
    assert result == "key1:value1,key2:value2"

    # 测试空参数
    assert processor.format_parameters({}) == ""

    # 测试特殊字符
    params = {"key:1": "value:1", "key,2": "value,2"}
    result = processor.format_parameters(params)
    assert result == "key:1:value:1,key,2:value,2"


def test_parse_parameters(processor):
    """测试参数解析"""
    # 测试基本参数解析
    param_str = "key1:value1,key2:value2"
    result = processor.parse_parameters(param_str)
    assert result == {"key1": "value1", "key2": "value2"}

    # 测试空参数
    assert processor.parse_parameters("") == {}
    assert processor.parse_parameters(None) == {}
    assert processor.parse_parameters("{}") == {}

    # 测试空格处理
    param_str = " key1 : value1 , key2 : value2 "
    result = processor.parse_parameters(param_str)
    assert result == {"key1": "value1", "key2": "value2"}


@pytest.mark.asyncio
async def test_process_mcp_command(processor, mock_manager):
    """测试处理 MCP 命令"""
    mock_client = mock_manager.get_client.return_value
    prompt = Prompt(name="test_prompt", description="测试提示词", arguments=[])
    mock_client.list_prompts = AsyncMock(return_value=[prompt])
    mock_client.get_prompt = AsyncMock(return_value=prompt)
    
    # 测试选择提示词
    prompt_responses = ["1", "2", "1"]  # 选择客户端、选择 Prompts、选择提示词
    processor.session.prompt_async = AsyncMock(side_effect=prompt_responses)
    result = await processor.process_mcp_command()
    assert result == "->mcp_prompts[test-mcp]:test_prompt"

    # 测试选择工具
    tool_responses = ["1", "3", "1"]  # 选择客户端、选择 Tools、选择工具
    processor.session.prompt_async = AsyncMock(side_effect=tool_responses)
    result = await processor.process_mcp_command()
    assert result == "->mcp_tools[test-mcp]:test_tool"

    # 测试选择资源
    resource_responses = ["1", "1", "1"]  # 选择客户端、选择 Resources、选择资源
    processor.session.prompt_async = AsyncMock(side_effect=resource_responses)
    result = await processor.process_mcp_command()
    assert result == "->mcp_resources[test-mcp]:test://uri"

    # 测试无效选择
    invalid_responses = ["1", "4"]  # 选择客户端、无效选择
    processor.session.prompt_async = AsyncMock(side_effect=invalid_responses)
    result = await processor.process_mcp_command()
    assert result is None


@pytest.mark.asyncio
async def test_process_text(processor, mock_manager):
    """测试文本处理"""
    # 设置模拟客户端
    mock_client = mock_manager.get_client.return_value
    
    # 设置提示词
    prompt = Prompt(name="test_prompt", description="测试提示词", arguments=[])
    mock_client.list_prompts = AsyncMock(return_value=[prompt])
    mock_client.get_prompt = AsyncMock(return_value="处理后的提示词")
    
    # 设置工具
    tool = Tool(name="test_tool", description="测试工具", input_schema={})
    mock_client.list_tools = AsyncMock(return_value=[tool])
    mock_client.call_tool = AsyncMock(return_value="工具执行结果")
    
    # 设置资源
    resource = Resource(name="test_resource", description="测试资源", uri="test://uri", mime_type="text/plain")
    mock_client.list_resources = AsyncMock(return_value=[resource])
    mock_client.read_resource = AsyncMock(return_value="资源内容")
    
    # 测试提示词占位符
    text = "测试 ->mcp_prompts[test-mcp]:test_prompt"
    result = await processor.process_text(text)
    assert result == "测试 处理后的提示词"
    
    # 测试工具占位符
    text = "测试 ->mcp_tools[test-mcp]:test_tool"
    result = await processor.process_text(text)
    assert result == "测试 工具执行结果"
    
    # 测试资源占位符
    text = "测试 ->mcp_resources[test-mcp]:test://uri"
    result = await processor.process_text(text)
    assert result == "测试 资源内容"

    # 测试带参数的占位符
    text = "测试 ->mcp_prompts[test-mcp]:test_prompt{key1:value1,key2:value2}"
    result = await processor.process_text(text)
    assert result == "测试 处理后的提示词"

    # 测试多个占位符
    text = """测试多个占位符：
    1. ->mcp_prompts[test-mcp]:test_prompt
    2. ->mcp_tools[test-mcp]:test_tool
    3. ->mcp_resources[test-mcp]:test://uri"""
    result = await processor.process_text(text)
    assert "处理后的提示词" in result
    assert "工具执行结果" in result
    assert "资源内容" in result

    # 测试无效的占位符
    text = "测试 ->mcp_invalid[test-mcp]:test_invalid"
    result = await processor.process_text(text)
    assert result == text

    # 测试纯 ->mcp 命令
    text = "->mcp"
    result = await processor.process_text(text)
    assert result == text


@pytest.mark.asyncio
async def test_collect_prompt_arguments(processor):
    """测试收集提示词参数"""
    # 创建带参数的提示词
    prompt = Prompt(
        name="test_prompt",
        description="测试提示词",
        arguments=[
            {"name": "arg1", "description": "参数1"},
            {"name": "arg2", "description": "参数2"}
        ]
    )

    # 模拟用户输入
    processor.session.prompt_async = AsyncMock(side_effect=["value1", "value2"])
    
    # 收集参数
    params = await processor.collect_prompt_arguments(prompt)
    assert params == {"arg1": "value1", "arg2": "value2"}


@pytest.mark.asyncio
async def test_collect_tool_arguments(processor):
    """测试收集工具参数"""
    # 创建带参数的工具
    tool = Tool(
        name="test_tool",
        description="测试工具",
        input_schema={
            "properties": {
                "param1": {"description": "参数1"},
                "param2": {"description": "参数2"}
            }
        }
    )

    # 模拟用户输入
    processor.session.prompt_async = AsyncMock(side_effect=["value1", "value2"])
    
    # 收集参数
    params = await processor.collect_tool_arguments(tool)
    assert params == {"param1": "value1", "param2": "value2"}


@pytest.mark.asyncio
async def test_error_handling(processor, mock_manager):
    """测试错误处理"""
    mock_client = mock_manager.get_client.return_value

    # 测试客户端列表为空
    mock_manager.get_all_clients.return_value = {}
    result = await processor.select_mcp_client()
    assert result is None

    # 测试提示词列表为空
    mock_client.list_prompts = AsyncMock(return_value=[])
    prompt, params = await processor.select_prompt(mock_client)
    assert prompt is None
    assert params == {}

    # 测试工具列表为空
    mock_client.list_tools = AsyncMock(return_value=[])
    tool, params = await processor.select_tool(mock_client)
    assert tool is None
    assert params == {}

    # 测试资源列表为空
    mock_client.list_resources = AsyncMock(return_value=[])
    resource = await processor.select_resource(mock_client)
    assert resource is None

    # 测试客户端不存在
    text = "测试 ->mcp_prompts[invalid-client]:test_prompt"
    mock_manager.get_client.return_value = None
    result = await processor.process_text(text)
    assert result == text
