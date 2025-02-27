# Think MCP Client

MCP (Model Control Protocol) 客户端，用于与 MCP 服务器交互。支持资源管理、提示词处理和工具调用等功能。

## 特性

- ✨ 支持多种 MCP 服务器配置
- 🖥️ 提供命令行界面（CLI）和 Python API
- 🛠️ 支持资源、提示词和工具的交互式操作
- 📝 文本占位符处理功能（如 `->mcp_prompts[client]:name{params}`）
- 🔍 完整的类型注解和异步支持
- 🧪 全面的测试覆盖

## 安装指南

### 1. 创建并激活虚拟环境

```bash
# 创建虚拟环境
python -m venv .venv

# 激活虚拟环境（MacOS/Linux）
source .venv/bin/activate

# 激活虚拟环境（Windows）
.venv\Scripts\activate
```

### 2. 安装 uv

```bash
# 使用 pip 安装 uv
pip install uv
```

### 3. 安装项目依赖

```bash
# 安装基本依赖
uv pip install -e .

# 安装开发依赖（如果需要）
uv pip install -e ".[dev]"
```

## 使用方法

### 1. 配置

首次运行时，会在用户目录下创建配置文件：`~/.think_mcp_client/config/config.json`

配置文件示例：
```json
{
    "servers": {
        "default": {
            "command": "python",
            "args": ["-m", "mcp_server"],
            "env": {
                "MCP_SERVER_HOST": "localhost",
                "MCP_SERVER_PORT": "8000"
            }
        },
        "custom-server": {
            "command": "/path/to/custom/server",
            "args": ["--config", "config.yaml"],
            "env": {
                "CUSTOM_VAR": "value"
            }
        }
    }
}
```

### 2. 命令行使用

```bash
# 启动 CLI
python -m think_mcp_client
```

CLI 支持以下功能：
- 列出和选择可用的 MCP 服务器
- 浏览和使用提示词（Prompts）
- 调用工具（Tools）
- 管理资源（Resources）
- 处理带有 MCP 占位符的文本

命令行快捷键：
- `Tab`: 自动补全
- `Ctrl+C`: 中断当前操作
- `Ctrl+D`: 退出程序
- `↑/↓`: 浏览历史命令

### 3. Python API 使用

#### 基本使用

```python
from think_mcp_client import MCPClientManager, MCPProcessor

# 创建客户端管理器
manager = MCPClientManager()

# 初始化所有配置的服务器
await manager.init_all_clients()

# 获取特定的客户端
client = manager.get_client("default")

# 列出可用的提示词
prompts = await client.list_prompts()
for prompt in prompts:
    print(f"提示词: {prompt.name} - {prompt.description}")

# 列出可用的工具
tools = await client.list_tools()
for tool in tools:
    print(f"工具: {tool.name} - {tool.description}")

# 列出可用的资源
resources = await client.list_resources()
for resource in resources:
    print(f"资源: {resource.name} - {resource.description}")
```

#### 自动初始化 MCP 服务器

1. **配置文件方式**

在 `~/.think_mcp_client/config/config.json` 中配置多个服务器：
```json
{
    "servers": {
        "default": {
            "command": "python",
            "args": ["-m", "mcp_server"],
            "env": {
                "MCP_SERVER_HOST": "localhost",
                "MCP_SERVER_PORT": "8000"
            }
        },
        "custom-server": {
            "command": "/path/to/custom/server",
            "args": ["--config", "config.yaml"],
            "env": {
                "CUSTOM_VAR": "value"
            }
        }
    }
}
```

2. **代码方式**

```python
from think_mcp_client import MCPClientManager
from pathlib import Path

# 使用默认配置路径
manager = MCPClientManager()

# 或者指定自定义配置路径
custom_config = Path("./my_config.json")
manager = MCPClientManager(config_path=custom_config)

# 初始化所有服务器
await manager.init_all_clients()

# 获取所有已初始化的客户端
clients = manager.get_all_clients()
for name, client in clients.items():
    print(f"服务器 {name} 已初始化")

# 清理所有客户端（在程序结束时调用）
await manager.cleanup_all_clients()
```

3. **CLI 方式**

使用命令行时会自动初始化所有配置的服务器：
```bash
python -m think_mcp_client
```

#### 服务器状态管理

```python
from think_mcp_client import MCPClientManager

manager = MCPClientManager()

# 初始化特定的服务器
client = manager.get_client("default")
await client.init_client()

# 检查服务器状态
prompts = await client.list_prompts()  # 如果服务器未初始化会自动初始化

# 清理特定的服务器
await client.cleanup()

# 或者清理所有服务器
await manager.cleanup_all_clients()
```

注意事项：
1. 服务器会在首次使用时自动初始化
2. 可以通过 `init_all_clients()` 预先初始化所有服务器
3. 建议在程序结束时调用 `cleanup_all_clients()` 清理资源
4. 如果服务器初始化失败，会记录错误日志并跳过该服务器

#### 处理带占位符的文本

```python
from think_mcp_client import MCPClientManager, MCPProcessor

# 创建客户端管理器和处理器
manager = MCPClientManager()
processor = MCPProcessor(manager)

# 处理包含提示词占位符的文本
text = "使用提示词生成内容：->mcp_prompts[default]:generate_text{topic:AI,length:short}"
result = await processor.process_text(text)

# 处理包含工具占位符的文本
text = "调用工具：->mcp_tools[default]:analyze_sentiment{text:这是一段测试文本}"
result = await processor.process_text(text)

# 处理包含资源占位符的文本
text = "读取资源：->mcp_resources[default]:example.txt"
result = await processor.process_text(text)

# 处理包含多个占位符的文本
text = """
1. 提示词：->mcp_prompts[default]:prompt1
2. 工具：->mcp_tools[default]:tool1
3. 资源：->mcp_resources[default]:resource1
"""
result = await processor.process_text(text)
```

#### 错误处理

```python
from think_mcp_client import MCPClientManager, MCPProcessor
from think_mcp_client.exceptions import MCPClientError

try:
    manager = MCPClientManager()
    client = manager.get_client("non-existent-server")
except MCPClientError as e:
    print(f"客户端错误: {e}")
```

## 快速开始

### 安装

```bash
pip install think-mcp-client
```

### 基本使用

MCP 客户端支持两种模式：基础模式和 CLI 模式。你可以在初始化时选择使用哪种模式。

#### 1. 配置文件

默认配置文件路径为 `~/.think_mcp_client/config/mcp_server_config.json`：

```json
{
    "mcpServers": {
        "default": {
            "command": "think-mcp-host",
            "args": [],
            "env": {}
        }
    }
}
```

#### 2. 使用基础模式

```python
from think_mcp_client import MCPClientManager, ClientType
import asyncio

async def main():
    # 创建基础模式的客户端管理器（默认模式）
    manager = MCPClientManager(client_type=ClientType.BASE)
    
    # 初始化所有客户端
    await manager.init_all_clients()
    
    try:
        # 获取默认客户端
        client = manager.get_client("default")
        
        # 使用客户端
        prompts = await client.list_prompts()
        tools = await client.list_tools()
        resources = await client.list_resources()
        
        # 调用工具
        result = await client.call_tool("tool_name", {"arg1": "value1"})
        
    finally:
        # 清理所有客户端
        await manager.cleanup_all_clients()

if __name__ == "__main__":
    asyncio.run(main())
```

#### 3. 使用 CLI 模式

```python
from think_mcp_client import MCPClientManager, ClientType
import asyncio

async def main():
    # 创建 CLI 模式的客户端管理器
    manager = MCPClientManager(client_type=ClientType.CLI)
    
    # 初始化所有客户端
    await manager.init_all_clients()
    
    try:
        # 获取默认客户端
        client = manager.get_client("default")
        
        # 启动 CLI
        await client.run()
        
    finally:
        # 清理所有客户端
        await manager.cleanup_all_clients()

if __name__ == "__main__":
    asyncio.run(main())
```

#### 4. 批量管理多个服务器

你可以在配置文件中添加多个服务器：

```json
{
    "mcpServers": {
        "server1": {
            "command": "think-mcp-host",
            "args": ["--config", "config1.json"],
            "env": {"SERVER_ID": "1"}
        },
        "server2": {
            "command": "think-mcp-host",
            "args": ["--config", "config2.json"],
            "env": {"SERVER_ID": "2"}
        }
    }
}
```

然后统一管理它们：

```python
async def main():
    manager = MCPClientManager(client_type=ClientType.CLI)
    await manager.init_all_clients()
    
    try:
        # 获取所有客户端
        clients = manager.get_all_clients()
        
        # 对每个客户端执行操作
        for name, client in clients.items():
            # 使用客户端...
            pass
            
    finally:
        await manager.cleanup_all_clients()
```

### API 文档

#### MCPClientManager

- `__init__(config_path: Optional[Path] = None, client_type: ClientType = ClientType.BASE)`
  - `config_path`: 配置文件路径，默认为 `~/.think_mcp_client/config/mcp_server_config.json`
  - `client_type`: 客户端类型，可选 `ClientType.BASE` 或 `ClientType.CLI`

- `get_client(server_name: str) -> Optional[MCPClient]`: 获取指定服务器的客户端
- `get_all_clients() -> Dict[str, MCPClient]`: 获取所有客户端
- `init_all_clients() -> None`: 初始化所有客户端
- `cleanup_all_clients() -> None`: 清理所有客户端

#### MCPClient

- `list_prompts() -> List[Prompt]`: 获取提示词列表
- `get_prompt(name: str) -> str`: 获取指定提示词
- `list_tools() -> List[Tool]`: 获取工具列表
- `call_tool(name: str, arguments: Dict[str, Any]) -> Any`: 调用工具
- `list_resources() -> List[Resource]`: 获取资源列表
- `read_resource(uri: str) -> bytes`: 读取资源内容

## 开发指南

### 代码格式化

```bash
# 运行 black 格式化代码
black src/think_mcp_client tests

# 运行 isort 整理导入
isort src/think_mcp_client tests
```

### 类型检查

```bash
# 运行 mypy 进行类型检查
mypy src/think_mcp_client
```

### 运行测试

```bash
# 运行所有测试
pytest

# 运行特定测试文件
pytest tests/test_client.py

# 运行带覆盖率报告的测试
pytest --cov=think_mcp_client tests/
```

### 贡献指南

1. Fork 项目
2. 创建功能分支 (`git checkout -b feature/AmazingFeature`)
3. 提交更改 (`git commit -m 'Add some AmazingFeature'`)
4. 推送到分支 (`git push origin feature/AmazingFeature`)
5. 创建 Pull Request

## 依赖项

- Python >= 3.10
- think-llm-client >= 0.2.9
- mcp >= 0.1.0
- prompt-toolkit >= 3.0.0
- rich >= 10.0.0
- pydantic >= 2.0.0
- typing-extensions >= 4.0.0
- pyyaml >= 6.0.2

## 许可证

MIT License

## 联系方式

Think Team - team@think.com
