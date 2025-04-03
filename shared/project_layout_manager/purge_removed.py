# shared/project_layout_manager/purge_removed.py

import os
from shared.project_layout_manager.config.layout_config import JSON_STATE_PATH
from shared.project_layout_manager.storage.json_storage import load_state, save_state
from shared.project_layout_manager.models.node import Node

def purge_removed_nodes(nodes):
    """
    Recursively removes any nodes marked as 'removed'.
    Returns a new list of active nodes.
    """
    cleaned = []
    for node in nodes:
        if node.status != "removed":
            # Recursively clean children
            node.children = purge_removed_nodes(node.children)
            cleaned.append(node)
    return cleaned

def main():
    print(f"Loading project state from: {JSON_STATE_PATH}")
    nodes = load_state(JSON_STATE_PATH)
    print(f"Loaded {len(nodes)} top-level nodes.")

    cleaned_nodes = purge_removed_nodes(nodes)
    print(f"Purged removed nodes. {len(cleaned_nodes)} top-level nodes remain.")

    save_state(cleaned_nodes, JSON_STATE_PATH)
    print(f"Cleaned state saved to: {JSON_STATE_PATH}")
    print(f"Don't forget to run layout_manager.py again if you want them removed from the Markdown and Flat files immediately.")

if __name__ == "__main__":
    main()
