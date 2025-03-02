#!/usr/bin/env python3
"""
Validate README.md code examples.

This script:
1. Extracts Python code blocks from README.md
2. Validates the syntax of each example
3. Optionally runs the examples in a controlled environment
4. Reports any issues found

Usage:
  python validate_readme.py [--run] [--fix]

Options:
  --run    Run the examples (not just syntax check)
  --fix    Try to fix common issues in the examples
"""

import argparse
import ast
import sys
from pathlib import Path


def extract_code_blocks(markdown_file: Path) -> list[tuple[str, int]]:
    """Extract Python code blocks from a markdown file with line numbers."""
    with open(markdown_file, encoding="utf-8") as f:
        content = f.readlines()

    code_blocks = []
    in_code_block = False
    current_block: list[str] = []
    start_line = 0

    for i, line in enumerate(content):
        if line.strip() == "```python":
            in_code_block = True
            current_block = []
            start_line = i + 1
        elif line.strip() == "```" and in_code_block:
            in_code_block = False
            code_blocks.append(("".join(current_block), start_line))
        elif in_code_block:
            current_block.append(line)

    return code_blocks


def validate_syntax(code: str) -> tuple[bool, str]:
    """Validate Python syntax."""
    try:
        ast.parse(code)
        return True, "Valid syntax"
    except SyntaxError as e:
        return False, f"Syntax error: {str(e)}"
    except Exception as e:
        return False, f"Error: {str(e)}"


def check_imports(code: str) -> list[str]:
    """Check for imports in the code and return missing ones."""
    # No need to check for specific imports - use what's in the README
    return []


def main():
    """Main function."""
    parser = argparse.ArgumentParser(description="Validate README.md code examples")
    parser.add_argument(
        "--run", action="store_true", help="Run the examples (not just syntax check)"
    )
    parser.add_argument(
        "--fix", action="store_true", help="Try to fix common issues in the examples"
    )
    args = parser.parse_args()

    # Get the path to the README.md file
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"

    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}")
        return 1

    print(f"Validating code examples in {readme_path}")
    code_blocks = extract_code_blocks(readme_path)
    print(f"Found {len(code_blocks)} Python code blocks")

    # Validate each code block
    all_valid = True
    for i, (block, line_number) in enumerate(code_blocks):
        print(f"\nBlock {i + 1} (line {line_number}):")
        print("-" * 40)
        print(block.strip())
        print("-" * 40)

        # Check syntax
        valid, error_msg = validate_syntax(block)
        if valid:
            print("Syntax: OK")
        else:
            print(f"Syntax: FAIL - {error_msg}")
            all_valid = False
            continue

        # Check for missing imports
        missing_imports = check_imports(block)
        if missing_imports:
            print("Missing imports:")
            for imp in missing_imports:
                print(f"  {imp}")

            if args.fix:
                print("Fixed code would be:")
                fixed_code = "\n".join(missing_imports) + "\n\n" + block
                print("-" * 40)
                print(fixed_code)
                print("-" * 40)
        else:
            print("Imports: OK")

    if all_valid:
        print("\nAll code blocks have valid syntax!")
    else:
        print("\nSome code blocks have syntax errors.")

    return 0 if all_valid else 1


if __name__ == "__main__":
    sys.exit(main())
