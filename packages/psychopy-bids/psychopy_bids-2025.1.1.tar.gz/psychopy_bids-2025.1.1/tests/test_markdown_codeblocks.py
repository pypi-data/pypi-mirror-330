"""
This file combines the two frameworks doctest and unittest to test various aspects of the
python codeblocks in specified .md files.
"""

import os
import re
import shutil
from pathlib import Path

import pytest

provided_paths = ["README.md", "docs/index.md", "docs/coder.md"]

def extract_code_blocks(file_path):
    """
    Extract Python code blocks from a Markdown file.
    """
    with open(file_path, "r", encoding="utf-8") as file:
        content = file.read()
        return re.findall(r"```(?:py|python)\n(.*?)```", content, re.DOTALL)

base_path = Path(__file__).parent.parent
markdown_files = [base_path / path for path in provided_paths]

log_file_path = Path(__file__).parent / "tested_code_blocks.md"
with open(log_file_path, "w", encoding="utf-8") as log_file:
    log_file.write("# Tested Markdown Files\n\n")
    log_file.writelines(f"- {file.relative_to(base_path)}\n" for file in markdown_files)
    log_file.write("\n---\n\n")

@pytest.mark.parametrize("markdown_file", markdown_files, ids=lambda f: f.name)
def test_markdown_code(markdown_file):
    """
    Test Python code blocks extracted from Markdown files and log them to a new Markdown file.
    """
    code_blocks = extract_code_blocks(markdown_file)

    with open(log_file_path, "a", encoding="utf-8") as log_file:
        log_file.write(
            f"# Tested Code Blocks from {markdown_file.relative_to(base_path)}\n\n"
        )
        if not code_blocks:
            log_file.write("No Python code blocks found.\n\n")
            return

        for index, block in enumerate(code_blocks):
            log_file.write(f"## Code Block {index + 1}\n")
            log_file.write(f"```python\n{block}\n```\n\n")

            try:
                exec(block, {"__file__": str(markdown_file)})  # nosec
            except Exception as e:
                pytest.fail(
                    f"Code block in {markdown_file} failed:\n{block}\n\nError: {e}"
                )
            finally:
                if os.path.exists("example_dataset"):
                    shutil.rmtree("example_dataset")
