# Quick Start Guide

Get up and running with pytest-mcp-server in 5 minutes!

## Step 1: Install Dependencies

```bash
cd /Users/303748/Documents/ws/pytest-mcp-server

# Create virtual environment
python3 -m venv venv
source venv/bin/activate

# Install dependencies
pip install -e .
```

## Step 2: Verify Installation

```bash
python verify_setup.py
```

You should see all checks pass ✅

## Step 3: Try the Calculator App

```bash
python -m src.calculator_app
```

A calculator window should open. Try some calculations!

## Step 4: Run the Tests

```bash
# Run all tests
pytest tests/ -v

# Run only UI tests
pytest tests/ -m ui

# Run with coverage
pytest tests/ --cov=src
```

## Step 5: Configure Claude Desktop

1. **Find your config file:**
   - macOS: `~/Library/Application Support/Claude/claude_desktop_config.json`
   - Windows: `%APPDATA%\Claude\claude_desktop_config.json`

2. **Add this configuration:**

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

## Step 6: Test with Claude

Open Claude Desktop and try these prompts:

1. "List all available calculator tests"
2. "Run the calculator UI tests"
3. "Run only the error handling tests"
4. "Show me the last test results"

## Troubleshooting

### "Module not found" errors

```bash
# Make sure you're in the project directory
cd /Users/303748/Documents/ws/pytest-mcp-server

# Make sure virtual environment is activated
source venv/bin/activate

# Reinstall
pip install -e .
```

### MCP server not connecting

1. Check the path in `claude_desktop_config.json` is correct
2. Use absolute path to `server.py`
3. Restart Claude Desktop completely
4. Check logs: `~/Library/Logs/Claude/` (macOS)

### Tests not finding modules

```bash
# Install in editable mode
pip install -e .

# Or set PYTHONPATH
export PYTHONPATH=/Users/303748/Documents/ws/pytest-mcp-server:$PYTHONPATH
```

## What's Next?

- Read the full [README.md](README.md) for detailed documentation
- Explore test files in `tests/test_calculator.py`
- Check out the MCP server code in `server.py`
- Extend with your own tests and features

## Common Commands

```bash
# Activate environment
source venv/bin/activate

# Run specific test class
pytest tests/test_calculator.py::TestBasicOperations -v

# Run with specific marker
pytest tests/ -m "ui and not slow"

# Run single test
pytest tests/test_calculator.py::TestBasicOperations::test_addition -v

# Generate HTML coverage report
pytest tests/ --cov=src --cov-report=html
open htmlcov/index.html
```

## Getting Help

- Check [README.md](README.md) for full documentation
- Review test examples in `tests/test_calculator.py`
- Look at server implementation in `server.py`

Happy testing! 🚀
