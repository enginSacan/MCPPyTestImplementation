#!/usr/bin/env python3
"""
Setup verification script for pytest-mcp-server.
Run this script to verify your installation is correct.
"""

import sys
import subprocess
from pathlib import Path


def check_python_version():
    """Check if Python version is 3.10 or higher."""
    version = sys.version_info
    if version.major >= 3 and version.minor >= 10:
        print(f"✅ Python version: {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"❌ Python version {version.major}.{version.minor} is too old. Need 3.10+")
        return False


def check_dependencies():
    """Check if required dependencies are installed."""
    dependencies = ["mcp", "pytest"]
    all_ok = True
    
    for dep in dependencies:
        try:
            __import__(dep)
            print(f"✅ {dep} is installed")
        except ImportError:
            print(f"❌ {dep} is NOT installed")
            all_ok = False
    
    return all_ok


def check_project_structure():
    """Check if project structure is correct."""
    required_paths = [
        "src/calculator_app.py",
        "tests/test_calculator.py",
        "server.py",
        "pyproject.toml"
    ]
    
    all_ok = True
    for path_str in required_paths:
        path = Path(path_str)
        if path.exists():
            print(f"✅ {path_str} exists")
        else:
            print(f"❌ {path_str} is missing")
            all_ok = False
    
    return all_ok


def run_sample_test():
    """Try to run a sample test."""
    try:
        result = subprocess.run(
            ["pytest", "tests/", "--collect-only", "-q"],
            capture_output=True,
            text=True,
            timeout=10
        )
        
        if result.returncode == 0:
            test_count = len([line for line in result.stdout.split('\n') if '::test_' in line])
            print(f"✅ Found {test_count} tests")
            return True
        else:
            print(f"❌ Failed to collect tests: {result.stderr}")
            return False
    except Exception as e:
        print(f"❌ Error running pytest: {e}")
        return False


def main():
    """Run all verification checks."""
    print("=" * 50)
    print("Pytest MCP Server - Setup Verification")
    print("=" * 50)
    print()
    
    checks = [
        ("Python Version", check_python_version),
        ("Dependencies", check_dependencies),
        ("Project Structure", check_project_structure),
        ("Test Discovery", run_sample_test)
    ]
    
    results = []
    for name, check_func in checks:
        print(f"\n{name}:")
        print("-" * 30)
        result = check_func()
        results.append(result)
    
    print("\n" + "=" * 50)
    if all(results):
        print("✅ All checks passed! Your setup is ready.")
        print("\nNext steps:")
        print("1. Run the calculator: python -m src.calculator_app")
        print("2. Run tests: pytest tests/")
        print("3. Configure Claude Desktop with server.py")
    else:
        print("❌ Some checks failed. Please fix the issues above.")
        print("\nTo install dependencies:")
        print("  pip install -e .")
    print("=" * 50)


if __name__ == "__main__":
    main()
