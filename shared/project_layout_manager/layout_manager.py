# shared/project_layout_manager/layout_manager.py

import os

# Import config values
from shared.project_layout_manager.config.layout_config import (
    PROJECT_ROOT,
    JSON_STATE_PATH,
    MARKDOWN_FILE_PATH,
    IGNORE_LIST
)

# Import the JSON storage utilities
from shared.project_layout_manager.storage.json_storage import load_state, save_state

# Import the file scanning functions
from shared.project_layout_manager.scanner.file_scanner import scan_directory, update_state_with_changes

# Import the ASCII parser and comment manager
from shared.project_layout_manager.importer.ascii_parser import parse_ascii_tree
from shared.project_layout_manager.models.comment_manager import merge_manual_comments

def run_manager():
    """
    Main function to integrate file scanning with JSON state loading,
    manual comment merging, and final saving of the updated layout.
    """
    # 1. Load the existing JSON state
    saved_nodes = load_state(JSON_STATE_PATH)
    print(f"Loaded {len(saved_nodes)} top-level nodes from JSON state.")

    # 2. Attempt to parse the user-edited ASCII tree (if it exists) and merge new comments
    try:
        with open(MARKDOWN_FILE_PATH, 'r', encoding='utf-8') as f:
            ascii_content = f.read()
        parsed_nodes = parse_ascii_tree(ascii_content)
        merge_manual_comments(saved_nodes, parsed_nodes)
        print("Merged manual comments from ASCII tree.")
    except FileNotFoundError:
        print("No ASCII Markdown file found; skipping manual comment merge.")

    # 3. Scan the project directory
    scanned_nodes = scan_directory(PROJECT_ROOT, ignore_list=IGNORE_LIST)
    print(f"Scanned directory: {PROJECT_ROOT}")

    # 4. Reconcile scanned nodes with the (potentially updated) saved state
    updated_nodes = update_state_with_changes(scanned_nodes, saved_nodes)
    print(f"Merged state now has {len(updated_nodes)} top-level nodes after reconciliation.")

    # 5. Save the updated state to JSON
    save_state(updated_nodes, JSON_STATE_PATH)
    print(f"Updated JSON state saved to {JSON_STATE_PATH}.")

    # Optionally, export to ASCII tree or flat list here if desired
    # e.g., ascii_exporter, flat_exporter

if __name__ == "__main__":
    run_manager()
