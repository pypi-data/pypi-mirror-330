#!/usr/bin/env python3
"""
This script extracts code blocks from the README.md file and tests them
to ensure they work correctly.
"""

import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


def extract_code_blocks(markdown_file):
    """Extract Python code blocks from a markdown file."""
    with open(markdown_file, encoding="utf-8") as f:
        content = f.read()

    # Regular expression to find Python code blocks
    # This matches ```python ... ``` blocks
    pattern = r"```python\n(.*?)```"
    code_blocks = re.findall(pattern, content, re.DOTALL)

    return code_blocks


def test_code_block(code_block, block_index):
    """Test a single code block by executing it."""
    # Create a temporary file
    with tempfile.NamedTemporaryFile(
        suffix=".py", delete=False, mode="w", encoding="utf-8"
    ) as temp_file:
        temp_file_path = temp_file.name

        # Add import for charstyle package
        temp_file.write("import sys\n")
        temp_file.write("import os\n")
        temp_file.write("sys.path.insert(0, os.path.abspath('.'))\n\n")

        # Write the code block to the file
        temp_file.write(code_block)

    try:
        # Run the code block
        result = subprocess.run(
            [sys.executable, temp_file_path], capture_output=True, text=True, check=False
        )

        if result.returncode == 0:
            print(f"OK Code block {block_index + 1} executed successfully")
            return True
        else:
            print(f"FAIL Code block {block_index + 1} failed with error:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"FAIL Code block {block_index + 1} failed with exception: {e}")
        return False
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def main():
    """Main function to extract and test code blocks."""
    # Get the path to the README.md file
    repo_root = Path(__file__).parent.parent
    readme_path = repo_root / "README.md"

    if not readme_path.exists():
        print(f"Error: README.md not found at {readme_path}")
        return 1

    print(f"Extracting code blocks from {readme_path}")
    code_blocks = extract_code_blocks(readme_path)
    print(f"Found {len(code_blocks)} Python code blocks")

    # Test each code block
    success_count = 0
    for i, block in enumerate(code_blocks):
        print(f"\nTesting code block {i + 1}:")
        print("-" * 40)
        print(block.strip())
        print("-" * 40)

        if test_code_block(block, i):
            success_count += 1

    # Print summary
    print(f"\nSummary: {success_count}/{len(code_blocks)} code blocks executed successfully")

    return 0 if success_count == len(code_blocks) else 1


if __name__ == "__main__":
    sys.exit(main())
