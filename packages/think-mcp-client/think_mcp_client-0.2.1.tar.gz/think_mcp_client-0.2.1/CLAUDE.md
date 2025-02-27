# Think MCP Client Development Guide

## Commands
* Install dependencies: `uv pip install -e .` (regular) or `uv pip install -e ".[dev]"` (development)
* Run tests: `pytest` (all tests) or `pytest tests/test_client.py` (single file)
* Run specific test: `pytest tests/test_client.py::test_list_prompts -v`
* Type checking: `mypy src/think_mcp_client`
* Code formatting: `black src/think_mcp_client tests`
* Sort imports: `isort src/think_mcp_client tests`
* Linting: `flake8 src/think_mcp_client tests`

## Code Style Guidelines
* Python: 3.12+ with typing annotations 
* Line length: 100 characters maximum
* Imports: Use isort with black profile (alphabetical, grouped stdlib/third-party/local)
* Classes: Use dataclasses where appropriate, document with docstrings
* Error handling: Use try/except with specific exceptions, log errors with logger
* Async: Use asyncio, proper async context management with AsyncExitStack
* Naming: snake_case for functions/variables, PascalCase for classes
* Documentation: Docstrings in Chinese, describe parameters and return values
* Testing: Write pytest fixtures and tests for all core functionality