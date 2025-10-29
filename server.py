#!/usr/bin/env python3
import asyncio
import json
import subprocess
import sys
from pathlib import Path
from typing import Any

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent


class PytestMCPServer:
    def __init__(self):
        self.server = Server("pytest-mcp-server")
        self.setup_handlers()
    
    def setup_handlers(self):
        @self.server.list_tools()
        async def list_tools() -> list[Tool]:
            """List available pytest tools."""
            return [
                Tool(
                    name="run_tests",
                    description="Run pytest tests with specified options. "
                               "You can target specific test files or run all tests.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_path": {
                                "type": "string",
                                "description": "Path to test file or directory "
                                             "(e.g., 'tests/' or 'tests/test_calculator.py')"
                            },
                            "markers": {
                                "type": "string",
                                "description": "Pytest markers to filter tests "
                                             "(e.g., 'ui' or 'ui and not slow')"
                            },
                            "verbose": {
                                "type": "boolean",
                                "description": "Show detailed test output",
                                "default": True
                            },
                            "capture": {
                                "type": "string",
                                "description": "Output capture method: 'no', 'sys', or 'fd'",
                                "default": "no"
                            }
                        },
                        "required": ["test_path"]
                    }
                ),
                Tool(
                    name="list_tests",
                    description="List all available tests without running them. "
                               "Useful for discovering what tests exist.",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "test_path": {
                                "type": "string",
                                "description": "Path to scan for tests",
                                "default": "tests/"
                            }
                        }
                    }
                ),
                Tool(
                    name="get_test_results",
                    description="Get the last test run results in JSON format. "
                               "Shows detailed information about passes and failures.",
                    inputSchema={
                        "type": "object",
                        "properties": {}
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Any) -> list[TextContent]:
            """Handle tool calls."""
            if name == "run_tests":
                return await self.run_tests(arguments)
            elif name == "list_tests":
                return await self.list_tests(arguments)
            elif name == "get_test_results":
                return await self.get_test_results()
            else:
                raise ValueError(f"Unknown tool: {name}")
    
    async def run_tests(self, args: dict) -> list[TextContent]:
        """Execute pytest with specified parameters."""
        test_path = args.get("test_path", "tests/")
        markers = args.get("markers")
        verbose = args.get("verbose", True)
        capture = args.get("capture", "no")
        
        # Build pytest command
        cmd = ["pytest", test_path]
        
        if verbose:
            cmd.append("-v")
        
        cmd.append(f"--capture={capture}")
        
        if markers:
            cmd.extend(["-m", markers])
        
        # Add JSON report
        cmd.extend(["--json-report", "--json-report-file=test_results.json"])
        
        try:
            # Run pytest
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=300  # 5 minutes timeout
            )
            
            output = f"**Command:** `{' '.join(cmd)}`\n\n"
            output += f"**Exit Code:** {result.returncode}\n\n"
            output += "**Output:**\n```\n"
            output += result.stdout
            if result.stderr:
                output += f"\n\n**Errors:**\n{result.stderr}"
            output += "\n```"
            
            return [TextContent(type="text", text=output)]
            
        except subprocess.TimeoutExpired:
            return [TextContent(
                type="text",
                text="❌ Test execution timed out after 5 minutes."
            )]
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error running tests: {str(e)}"
            )]
    
    async def list_tests(self, args: dict) -> list[TextContent]:
        """List all available tests."""
        test_path = args.get("test_path", "tests/")
        
        cmd = ["pytest", "--collect-only", "-q", test_path]
        
        try:
            result = subprocess.run(
                cmd,
                capture_output=True,
                text=True,
                timeout=30
            )
            
            output = f"**Available Tests in {test_path}:**\n\n"
            output += "```\n"
            output += result.stdout
            output += "\n```"
            
            return [TextContent(type="text", text=output)]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error listing tests: {str(e)}"
            )]
    
    async def get_test_results(self) -> list[TextContent]:
        """Read and format the last test results."""
        results_file = Path("test_results.json")
        
        if not results_file.exists():
            return [TextContent(
                type="text",
                text="⚠️ No test results found. Run tests first using 'run_tests'."
            )]
        
        try:
            with open(results_file, "r") as f:
                data = json.load(f)
            
            summary = data.get("summary", {})
            
            output = "**Test Results Summary:**\n\n"
            output += f"✅ Passed: {summary.get('passed', 0)}\n"
            output += f"❌ Failed: {summary.get('failed', 0)}\n"
            output += f"⏭️ Skipped: {summary.get('skipped', 0)}\n"
            output += f"⏱️ Duration: {summary.get('duration', 0):.2f}s\n\n"
            
            # Show failed tests
            tests = data.get("tests", [])
            failed_tests = [t for t in tests if t.get("outcome") == "failed"]
            
            if failed_tests:
                output += "**Failed Tests:**\n\n"
                for test in failed_tests:
                    output += f"- `{test.get('nodeid')}`\n"
                    if "call" in test:
                        longrepr = test["call"].get("longrepr", "")
                        output += f"  ```\n  {longrepr[:200]}...\n  ```\n"
            
            return [TextContent(type="text", text=output)]
            
        except Exception as e:
            return [TextContent(
                type="text",
                text=f"❌ Error reading results: {str(e)}"
            )]
    
    async def run(self):
        """Start the MCP server."""
        # Print startup message to stderr (won't interfere with MCP protocol)
        print("Pytest MCP Server starting...", file=sys.stderr)
        print("Waiting for MCP client connection...", file=sys.stderr)
        
        async with stdio_server() as (read_stream, write_stream):
            await self.server.run(
                read_stream,
                write_stream,
                self.server.create_initialization_options()
            )


async def main():
    """Main entry point."""
    # Check if running in a terminal without a client
    if sys.stdin.isatty():
        print("=" * 60)
        print("⚠️  Pytest MCP Server")
        print("=" * 60)
        print()
        print("This server is designed to be run by an MCP client like Claude Desktop.")
        print("It should NOT be run directly from the command line.")
        print()
        print("To test the server, use: python test_server.py")
        print()
        print("To configure with Claude Desktop:")
        print("1. Edit: ~/Library/Application Support/Claude/claude_desktop_config.json")
        print("2. Add the server configuration from claude_desktop_config.example.json")
        print("3. Restart Claude Desktop")
        print()
        print("=" * 60)
        sys.exit(1)
    
    server = PytestMCPServer()
    await server.run()


if __name__ == "__main__":
    asyncio.run(main())
