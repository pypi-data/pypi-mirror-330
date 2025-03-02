#!/usr/bin/env python3
"""
A more advanced script to extract and test code examples from README.md.

This script:
1. Extracts Python code blocks from README.md
2. Identifies distinct examples (separated by comments or blank lines)
3. Tests each example individually
4. Provides detailed error reporting
5. Can fix common import issues automatically
"""

import argparse
import ast
import os
import re
import subprocess
import sys
import tempfile
from pathlib import Path


class CodeExample:
    """Represents a single code example extracted from README.md."""

    def __init__(self, code: str, line_number: int, block_index: int, header: str = ""):
        self.code = code.strip()
        self.line_number = line_number
        self.block_index = block_index
        self.imports = self._extract_imports()
        self.header = header

    def _extract_imports(self) -> list[str]:
        """Extract import statements from the code."""
        imports = []
        try:
            tree = ast.parse(self.code)
            for node in ast.walk(tree):
                if isinstance(node, (ast.Import | ast.ImportFrom)):
                    imports.append(ast.unparse(node))
        except SyntaxError:
            # If there's a syntax error, we can't parse the imports
            pass
        return imports

    def with_extra_imports(self, extra_imports: list[str]) -> str:
        """Return the code with extra import statements added."""
        return "\n".join(extra_imports + [self.code])

    def __str__(self) -> str:
        return f"Example at line {self.line_number} in block {self.block_index + 1}"


def extract_code_blocks(markdown_file: Path) -> list[tuple[str, int, str]]:
    """Extract Python code blocks from a markdown file with line numbers and headers."""
    code_blocks = []
    current_block: list[str] = []
    in_code_block = False
    start_line = 0
    current_header = ""

    with open(markdown_file, encoding="utf-8") as f:
        lines = f.readlines()

    i = 0
    while i < len(lines):
        line = lines[i].rstrip()

        # Capture markdown headers (### section titles)
        if line.startswith("###"):
            current_header = line.strip("# ")

        # Start of a Python code block
        elif line.strip() == "```python":
            in_code_block = True
            current_block = []
            start_line = i + 1  # +1 to skip the ```python line
            i += 1  # Move to the next line
            continue

        # End of a code block
        elif line.strip() == "```" and in_code_block:
            in_code_block = False
            code_blocks.append(("".join(current_block), start_line, current_header))

        # Inside a code block
        elif in_code_block:
            current_block.append(line)

        i += 1

    return code_blocks


def split_into_examples(code_block: str) -> list[tuple[str, str]]:
    """Split a code block into individual examples based on comments or blank lines."""
    examples = []
    lines = code_block.split("\n")

    # First, identify all the comment lines that look like headers
    header_indices = []
    for i, line in enumerate(lines):
        if re.match(r"^#\s*[A-Z]", line):
            header_indices.append(i)

    # If no headers found, return the whole block as one example
    if not header_indices:
        return [("", code_block)]

    # Process each section between headers
    for i in range(len(header_indices)):
        start_idx = header_indices[i]
        header = lines[start_idx]

        # Determine the end index (either the next header or the end of the block)
        if i < len(header_indices) - 1:
            end_idx = header_indices[i + 1]
        else:
            end_idx = len(lines)

        # Extract the example code (including the header)
        example_code = "\n".join(lines[start_idx:end_idx])

        # Skip empty examples or examples that are just comments
        if example_code.strip() and not all(
            line.strip().startswith("#") for line in example_code.strip().split("\n")
        ):
            examples.append((header, example_code))

    return examples


def test_example(example: CodeExample, extra_imports: list[str] | None = None) -> tuple[bool, str]:
    """Test a single code example by executing it."""
    if extra_imports is None:
        extra_imports = []

    # Set up encoding for UTF-8 output (for icons) and add path to find the charstyle module
    setup_code = [
        "import io",
        "import sys",
        "import os",
        "sys.path.insert(0, os.path.abspath('.'))",
        "sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')",
    ]

    # Don't add default imports - use the ones in the README examples
    charstyle_imports: list[str] = []

    # Create a temporary file
    with tempfile.NamedTemporaryFile(
        suffix=".py", delete=False, mode="w", encoding="utf-8"
    ) as temp_file:
        temp_file_path = temp_file.name

        # Write setup code and imports
        temp_file.write("\n".join(setup_code + charstyle_imports + extra_imports) + "\n\n")

        # Write the example code
        temp_file.write(example.code)

    try:
        # Run the example with UTF-8 encoding
        env = os.environ.copy()
        env["PYTHONIOENCODING"] = "utf-8"

        result = subprocess.run(
            [sys.executable, temp_file_path],
            capture_output=True,
            text=True,
            check=False,
            timeout=5,  # Add a timeout to prevent hanging
            env=env,
        )

        if result.returncode == 0:
            return True, "Success"
        else:
            return False, result.stderr.strip()
    except subprocess.TimeoutExpired:
        return False, "Execution timed out after 5 seconds"
    except Exception as e:
        return False, f"Exception: {str(e)}"
    finally:
        # Clean up the temporary file
        os.unlink(temp_file_path)


def main() -> int:
    """Main function to extract and test code examples."""
    parser = argparse.ArgumentParser(description="Test code examples in README.md")
    parser.add_argument("--fix", action="store_true", help="Try to fix common issues")

    readme_path = Path("README.md")
    if not readme_path.exists():
        print(f"Error: {readme_path} not found")
        return 1

    print(f"Extracting code blocks from {readme_path.absolute()}")
    code_blocks = extract_code_blocks(readme_path)
    print(f"Found {len(code_blocks)} Python code blocks")

    # First, test each block as a complete unit
    print("\nTesting each code block as a complete unit:")
    all_blocks_success = True

    for i, (code_block, line_number, section_header) in enumerate(code_blocks):
        block_example = CodeExample(code_block, line_number, i)
        print(
            f"Testing block {i + 1} (starting at line {line_number}) [{section_header}]... ", end=""
        )
        success, error = test_example(block_example)

        if success:
            print("OK Success")
        else:
            all_blocks_success = False
            print("FAIL")
            print(f"FAIL Block {i + 1} (starting at line {line_number}) failed with error:")
            print(error)

    # Now also test individual examples for more detailed feedback
    examples = []

    # First, add each complete code block as an example with its section header
    for i, (code_block, line_number, section_header) in enumerate(code_blocks):
        examples.append(CodeExample(code_block, line_number, i, f"# {section_header}"))

    # Then try to extract sub-examples from each block
    sub_examples = []
    for i, (code_block, line_number, section_header) in enumerate(code_blocks):
        # First try to split by comment headers
        block_examples = split_into_examples(code_block)

        # If we only got one example and it doesn't have a header, try to find logical chunks
        if len(block_examples) == 1 and not block_examples[0][0]:
            # Look for logical chunks separated by blank lines or comments
            logical_chunks = []
            current_chunk: list[str] = []
            current_header = ""

            for line in code_block.split("\n"):
                # If this is a comment that looks like a description, treat it as a header
                if re.match(r"^#\s*[A-Za-z]", line) and not line.strip().startswith("# Import"):
                    if current_chunk:
                        logical_chunks.append((current_header, "\n".join(current_chunk)))
                        current_chunk = []
                    current_header = line

                current_chunk.append(line)

            if current_chunk:
                logical_chunks.append((current_header, "\n".join(current_chunk)))

            # If we found logical chunks, use them instead
            if len(logical_chunks) > 1:
                block_examples = logical_chunks

        # Only add sub-examples if we found more than one
        if len(block_examples) > 1:
            for j, (header, example_code) in enumerate(block_examples):
                # Calculate approximate line number
                example_line = line_number
                if j > 0:
                    # Estimate the line number based on the number of lines in previous examples
                    for _, prev_example in block_examples[:j]:
                        example_line += prev_example.count("\n") + 1

                # If no specific header in the code, use the section header
                if not header:
                    header = f"# {section_header} (part {j + 1})"

                sub_examples.append(CodeExample(example_code, example_line, i, header))

    # Add sub-examples if we found any
    if sub_examples:
        examples.extend(sub_examples)

    print(f"\nExtracted {len(examples)} individual code examples")

    success_count = 0
    for i, example in enumerate(examples, 1):
        # Extract a clean header label by removing the # and trimming whitespace
        header_label = ""
        if example.header:
            header_label = example.header.lstrip("#").strip()
            # Limit the length of the header to avoid overly long lines
            if len(header_label) > 50:
                header_label = header_label[:47] + "..."

        header_display = f" [{header_label}]" if header_label else ""
        print(f"Testing example {i}{header_display}... ", end="")
        success, error = test_example(example)

        if success:
            print("OK Success")
            success_count += 1
        else:
            print("FAIL")
            print(f"FAIL Example {i} ({example}) failed with error:")
            print(error)

    print(f"\nSummary: {success_count}/{len(examples)} examples executed successfully")
    print(f"Complete blocks: {'All successful' if all_blocks_success else 'Some failed'}")

    return 0 if all_blocks_success else 1


if __name__ == "__main__":
    sys.exit(main())
