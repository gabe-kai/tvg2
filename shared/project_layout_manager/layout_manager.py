# shared/project_layout_manager/layout_manager.py

import os

# Import config values
from config.layout_config import (
    PROJECT_ROOT,
    JSON_STATE_PATH,
    MARKDOWN_FILE_PATH,
    IGNORE_LIST
)

# Import the JSON storage utilities
from storage.json_storage import load_state, save_state

# Import the file scanning functions
from scanner.file_scanner import scan_directory, update_state_with_changes

def run_manager():
    """
    Main function to integrate file scanning with JSON state loading.
    """
    # 1. Load the existing JSON state
    saved_nodes = load_state(JSON_STATE_PATH)
    print(f"Loaded {len(saved_nodes)} top-level nodes from JSON state.")

    # 2. Scan the project directory
    #    Here, we assume 'PROJECT_ROOT' is the path we want to scan,
    #    but you could specify a subfolder if needed.
    scanned_nodes = scan_directory(PROJECT_ROOT, ignore_list=IGNORE_LIST)
    print(f"Scanned directory: {PROJECT_ROOT}")

    # 3. Merge scanned nodes with the saved state
    updated_nodes = update_state_with_changes(scanned_nodes, saved_nodes)
    print(f"Merged state has {len(updated_nodes)} top-level nodes after reconciliation.")

    # 4. Save the updated state
    save_state(updated_nodes, JSON_STATE_PATH)
    print(f"Updated JSON state saved to {JSON_STATE_PATH}.")

    # Optionally, you could also export to Markdown or do other tasks here
    # e.g., ascii_exporter, flat_exporter, etc.

if __name__ == "__main__":
    run_manager()
