# shared/project_layout_manager/config/layout_config.py

import os

# NOTE: Adjust this if you'd like to specify a particular folder.
# For now, we'll assume the project root is 2 levels up from this config file's directory.
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "..", ".."))

# Default location for the JSON state file
JSON_STATE_PATH = os.path.join(PROJECT_ROOT, "shared", "project_layout_manager", "project_state.json")

# Default location for the Markdown ASCII tree file
MARKDOWN_FILE_PATH = os.path.join(PROJECT_ROOT, "shared", "project_layout_manager", "PROJECT_LAYOUT_TREE.md")

# Default location for the flat tree file
FLAT_FILE_PATH = os.path.join(PROJECT_ROOT, "shared", "project_layout_manager", "PROJECT_LAYOUT_FLAT.txt")

# Example ignore list to skip certain directories or file types during scanning
IGNORE_LIST = [
    ".git",
    ".venv",
    "__pycache__",
    ".pytest_cache",
    ".idea",
    ".DS_Store",
    # Add more entries as needed
]

# Add any other configuration values or constants you need below
# e.g., scanning depth limit, export formatting preferences, etc.
