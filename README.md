# Pytest MCP Server

A Model Context Protocol (MCP) server that enables AI assistants like Claude to run and analyze pytest tests for desktop applications.

## Overview

This project demonstrates how to integrate pytest with AI assistants through MCP. It includes:

- **Real Desktop Application**: A fully functional calculator app built with tkinter
- **Comprehensive Test Suite**: pytest tests covering UI, functionality, and edge cases
- **MCP Server**: Connects pytest to AI assistants for interactive testing

## Project Structure

```
pytest-mcp-server/
├── src/
│   ├── __init__.py
│   └── calculator_app.py      # Desktop calculator application
├── tests/
│   ├── __init__.py
│   └── test_calculator.py     # Pytest test suite
├── server.py                   # MCP server implementation
├── pyproject.toml             # Project configuration
└── README.md
```

## Installation

### Prerequisites

- Python 3.10 or higher
- pip package manager

### Setup

1. **Clone or navigate to the project directory:**

```bash
cd /Users/303748/Documents/ws/pytest-mcp-server
```

2. **Create a virtual environment:**

```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

3. **Install dependencies:**

```bash
pip install -e .
```

Or install with development dependencies:

```bash
pip install -e ".[dev]"
```

## Running the Calculator App

To run the desktop calculator application:

```bash
python -m src.calculator_app
```

Or use the installed script:

```bash
calculator-app
```

## Running Tests Manually

Run all tests:

```bash
pytest tests/
```

Run with verbose output:

```bash
pytest tests/ -v
```

Run only UI tests:

```bash
pytest tests/ -m ui
```

Run tests excluding fast ones:

```bash
pytest tests/ -m "not slow"
```

Run specific test class:

```bash
pytest tests/test_calculator.py::TestBasicOperations
```

## Using the MCP Server

### Configuration

1. **Find your Claude Desktop config file:**

   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add the MCP server configuration:**

**IMPORTANT NOTICE:** You need to give execution rights to the run_server.sh file

```json
{
  "mcpServers": {
    "pytest": {
      "command": "/Users/303748/Documents/ws/pytest-mcp-server/run_server.sh",
      "args": []
    }
  }
}
```

3. **Restart Claude Desktop**

### Using with Claude

Once configured, you can interact with your tests through Claude:

**Example conversations:**

> **You:** "List all available tests in the calculator project"

> **You:** "Run the UI tests for the calculator"

> **You:** "Run only the error handling tests"

> **You:** "Show me the results of the last test run"

> **You:** "The addition test is failing, can you help me debug it?"

## MCP Server Tools

The server provides three main tools:

### 1. run_tests

Executes pytest tests with specified options.

**Parameters:**
- `test_path` (required): Path to test file or directory
- `markers` (optional): Pytest markers to filter tests
- `verbose` (optional): Show detailed output (default: true)
- `capture` (optional): Output capture method (default: "no")

### 2. list_tests

Lists all available tests without running them.

**Parameters:**
- `test_path` (optional): Path to scan for tests (default: "tests/")

### 3. get_test_results

Retrieves and formats the last test run results.

**Parameters:** None

## Test Markers

The test suite uses these markers:

- `@pytest.mark.ui` - UI-related tests
- `@pytest.mark.error_handling` - Error handling tests
- `@pytest.mark.slow` - Slow-running tests

## Development

### Running Tests with Coverage

```bash
pytest tests/ --cov=src --cov-report=html
```

View coverage report:

```bash
open htmlcov/index.html  # macOS
```

### Code Formatting

Format code with Black:

```bash
black src/ tests/ server.py
```

Lint code with Ruff:

```bash
ruff check src/ tests/ server.py
```

## Calculator Features

The calculator application supports:

- **Basic operations**: Addition, subtraction, multiplication, division
- **Advanced operations**: Square root
- **UI controls**: Clear (C), Clear Entry (CE), Backspace (←)
- **Decimal numbers**: Full decimal support
- **Error handling**: Division by zero, negative square roots, invalid expressions

## Test Coverage

The test suite includes:

### Basic Operations
- Addition
- Subtraction
- Multiplication
- Division
- Division by zero handling

### Advanced Operations
- Square root calculations
- Square root of negative numbers
- Decimal number operations

### UI Functions
- Clear button functionality
- Clear entry functionality
- Backspace operation
- Chaining multiple operations

### Edge Cases
- Very large numbers
- Operations with zero
- Invalid expressions

## Troubleshooting

### Tests not running

Make sure you're in the project directory and have activated the virtual environment:

```bash
cd /Users/303748/Documents/ws/pytest-mcp-server
source venv/bin/activate
pytest tests/
```

### MCP server not connecting

1. Check that the path in `claude_desktop_config.json` is correct
2. Ensure Python is in your PATH
3. Restart Claude Desktop after configuration changes
4. Check Claude Desktop logs for error messages

### Import errors

Make sure the package is installed in editable mode:

```bash
pip install -e .
```

## Contributing

Contributions are welcome! Areas for improvement:

- Add more calculator features (memory, history)
- Implement screenshot capture on test failures
- Add performance benchmarking tools
- Create more test scenarios
- Improve error messages

## Resources

- [MCP Documentation](https://modelcontextprotocol.io/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Claude Desktop](https://claude.ai/download)

## Author

Created as an example project for the LinkedIn article "Building an MCP Server for Pytest: Automating Desktop Application Testing"
