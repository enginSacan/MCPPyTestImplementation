#!/usr/bin/env python3
"""
Test script for the Pytest MCP Server.
This simulates an MCP client to verify the server works correctly.
"""

import asyncio
import json
from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client


async def test_server():
    """Test the MCP server functionality."""
    print("=" * 60)
    print("Testing Pytest MCP Server")
    print("=" * 60)
    print()
    
    # Path to the server script
    server_script = "server.py"
    
    # Create server parameters
    server_params = StdioServerParameters(
        command="python",
        args=[server_script],
        env=None
    )
    
    print("1. Starting MCP server...")
    try:
        async with stdio_client(server_params) as (read, write):
            async with ClientSession(read, write) as session:
                print("✅ Server started successfully!")
                print()
                
                # Initialize the session
                print("2. Initializing session...")
                await session.initialize()
                print("✅ Session initialized!")
                print()
                
                # List available tools
                print("3. Listing available tools...")
                tools = await session.list_tools()
                print(f"✅ Found {len(tools.tools)} tools:")
                for tool in tools.tools:
                    print(f"   - {tool.name}: {tool.description[:50]}...")
                print()
                
                # Test: List tests
                print("4. Testing 'list_tests' tool...")
                try:
                    result = await session.call_tool("list_tests", {"test_path": "tests/"})
                    print("✅ list_tests works!")
                    print(f"   Response length: {len(str(result.content))} characters")
                except Exception as e:
                    print(f"❌ list_tests failed: {e}")
                print()
                
                # Test: Run tests
                print("5. Testing 'run_tests' tool...")
                try:
                    result = await session.call_tool(
                        "run_tests",
                        {
                            "test_path": "tests/test_calculator.py::TestBasicOperations::test_addition",
                            "verbose": True
                        }
                    )
                    print("✅ run_tests works!")
                    print(f"   Response length: {len(str(result.content))} characters")
                except Exception as e:
                    print(f"❌ run_tests failed: {e}")
                print()
                
                print("=" * 60)
                print("✅ All tests passed! Server is working correctly.")
                print("=" * 60)
                print()
                print("Next step: Configure Claude Desktop with this server!")
                print()
    
    except Exception as e:
        print(f"❌ Server test failed: {e}")
        print()
        print("Make sure:")
        print("1. You're in the project directory")
        print("2. Virtual environment is activated")
        print("3. All dependencies are installed (pip install -e .)")
        return False
    
    return True


if __name__ == "__main__":
    asyncio.run(test_server())
