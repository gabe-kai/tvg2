# shared/project_layout_manager/scanner/file_scanner.py

import os
from pathlib import Path
from typing import List, Optional

from shared.project_layout_manager.models.node import Node
from shared.project_layout_manager.models.comment_manager import update_comment_for_removal


def scan_directory(base_path: str, ignore_list: Optional[List[str]] = None) -> List[Node]:
    """
    Recursively scans the given directory path and returns a list of top-level Node objects.
    Each Node may contain child Nodes if it is a folder.

    Args:
        base_path (str): The path to the directory you want to scan.
        ignore_list (Optional[List[str]]): A list of folder or file names to ignore.

    Returns:
        List[Node]: A list of Node objects representing the top-level contents of 'base_path'.
    """
    if ignore_list is None:
        ignore_list = []

    base_path_obj = Path(base_path)
    if not base_path_obj.is_dir():
        raise NotADirectoryError(f"{base_path} is not a valid directory.")

    top_level_nodes = []

    for entry in sorted(base_path_obj.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        if entry.name in ignore_list:
            continue

        if entry.is_dir():
            folder_node = Node(
                name=entry.name,
                path=str(entry.relative_to(base_path_obj.parent)),
                is_folder=True,
                description="",  # No description for new nodes
                status="active"  # New or existing; will reconcile in update_state_with_changes
            )
            # Recursively gather child nodes
            folder_node.children = _scan_subdirectory(entry, ignore_list, base_path_obj.parent)
            top_level_nodes.append(folder_node)

        else:
            file_node = Node(
                name=entry.name,
                path=str(entry.relative_to(base_path_obj.parent)),
                is_folder=False,
                description="",
                status="active"
            )
            top_level_nodes.append(file_node)

    return top_level_nodes


def _scan_subdirectory(dir_path: Path, ignore_list: List[str], base_parent: Path) -> List[Node]:
    """
    Helper function that recursively scans the subdirectory to build Node objects.
    """
    children = []
    for entry in sorted(dir_path.iterdir(), key=lambda x: (x.is_file(), x.name.lower())):
        if entry.name in ignore_list:
            continue

        if entry.is_dir():
            folder_node = Node(
                name=entry.name,
                path=str(entry.relative_to(base_parent)),
                is_folder=True,
                description="",
                status="active"
            )
            folder_node.children = _scan_subdirectory(entry, ignore_list, base_parent)
            children.append(folder_node)
        else:
            file_node = Node(
                name=entry.name,
                path=str(entry.relative_to(base_parent)),
                is_folder=False,
                description="",
                status="active"
            )
            children.append(file_node)

    return children


def update_state_with_changes(scanned_nodes: List[Node], saved_nodes: List[Node]) -> List[Node]:
    """
    Compares the freshly scanned list of Node objects with the previously saved state (Nodes),
    and returns a new list that merges them. Changes handled:

      - New entries in 'scanned_nodes' that aren't in 'saved_nodes' are added as 'active'.
      - Entries in 'saved_nodes' that aren't in 'scanned_nodes' remain in the list but
        are marked 'removed' (if not already).
      - Existing entries keep their descriptions and status (unless newly scanned as removed).

    Args:
        scanned_nodes (List[Node]): Nodes obtained from scanning the filesystem.
        saved_nodes (List[Node]): Nodes previously saved in JSON state.

    Returns:
        List[Node]: A merged list of Node objects representing the updated state.
    """
    # Convert saved_nodes into a dictionary keyed by path for quick lookups.
    saved_dict = {node.path: node for node in _flatten_nodes(saved_nodes)}
    scanned_dict = {node.path: node for node in _flatten_nodes(scanned_nodes)}

    # Build a merged set of all paths we need to consider
    all_paths = set(saved_dict.keys()).union(scanned_dict.keys())

    updated_list = []

    for path in all_paths:
        scanned_node = scanned_dict.get(path)
        saved_node = saved_dict.get(path)

        if scanned_node and saved_node:
            # Already existed before; preserve existing node’s description and status if not removed
            # or update if scanned is active but saved is removed, etc.

            if saved_node.status == "removed" and scanned_node.status == "active":
                # Means it was previously removed, but has reappeared; treat it as active again
                saved_node.status = "active"

            # Merge child nodes recursively
            if saved_node.is_folder and scanned_node.is_folder:
                # Reconcile children
                saved_node.children = update_state_with_changes(scanned_node.children, saved_node.children)
            # Keep existing metadata (e.g., description) from saved_node, but path, is_folder, name stay the same
            updated_list.append(saved_node)

        elif scanned_node and not saved_node:
            # It's a new entry
            updated_list.append(scanned_node)

        else:
            # scanned_node is None; it means it wasn't found in the current scan
            # so we have an old node that might be removed
            if saved_node.status != "removed":
                saved_node.status = "removed"
            saved_node.description = update_comment_for_removal(saved_node.description)
            updated_list.append(saved_node)

    # Re-group the merged nodes into a hierarchy
    # For a top-level list, filter out nodes that have no parent in the updated_list
    # or re-build the hierarchy from scratch if you prefer a single root node approach.
    return _rebuild_hierarchy(updated_list)


def _flatten_nodes(nodes: List[Node]) -> List[Node]:
    """
    Returns a flat list of all nodes in the hierarchy, including children.
    """
    flat_list = []

    def _traverse(node: Node):
        flat_list.append(node)
        for child in node.children:
            _traverse(child)

    for n in nodes:
        _traverse(n)
    return flat_list


def _rebuild_hierarchy(all_nodes: List[Node]) -> List[Node]:
    """
    Rebuilds the hierarchy from a flat list of nodes by linking parents and children.
    Returns only the top-level nodes.

    For simplicity, let's assume 'path' has enough information to figure out parent/child
    relationships. If not, you may keep them in a flat list or handle differently.
    """
    # Convert to dict keyed by path for quick lookups
    node_by_path = {n.path: n for n in all_nodes}

    # We’ll gather children by direct path relationship:
    #   A node's parent path is everything except the last component in path
    #   Folder names typically end with a slash, but depends on how you manage them.
    #   Adjust logic as needed for your scenario.

    for n in all_nodes:
        if not n.is_folder:
            continue
        # The children are already in n.children, but they might be stale
        # or incomplete if we changed them above. Here, you could re-derive them
        # from the path if you prefer. For many projects, it may be enough
        # to trust the merges we did above.
        pass

    # Identify top-level nodes (those whose parent is not in the dictionary)
    # We'll define "parent path" as the immediate directory containing this node.
    # E.g., if path="project_layout_manager/scanner/file_scanner.py", the parent
    # might be "project_layout_manager/scanner" if we are consistent with path usage.
    top_level = []
    for n in all_nodes:
        parent_path = os.path.dirname(n.path) if n.path else ""
        if parent_path not in node_by_path or not parent_path:
            # It's top-level
            top_level.append(n)

    return top_level
