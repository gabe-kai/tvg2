# shared/project_layout_manager/models/comment_manager.py

import datetime
import re
from typing import List
from shared.project_layout_manager.models.node import Node

def update_comment_for_removal(existing_comment: str) -> str:
    """
    Appends a 'removed' note (with a timestamp) to the existing comment (description).
    This can be used when a file/folder transitions from 'active' to 'removed'.

    Args:
        existing_comment (str): The current description/comment for the node.

    Returns:
        str: Updated comment including a removal note.
    """
    # If *any* [Removed on YYYY-MM-DD ...] line is present, skip adding a new one
    pattern = r"\[Removed on \d{4}-\d{2}-\d{2}"
    if re.search(pattern, existing_comment):
        return existing_comment

    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    removal_msg = f"[Removed on {timestamp}]"

    if existing_comment.strip():
        return f"{existing_comment}\n{removal_msg}"
    else:
        return removal_msg
def merge_manual_comments(current_nodes: List[Node], parsed_nodes: List[Node]) -> None:
    """
    Merges manual changes from the ASCII tree (parsed_nodes) into the existing node list (current_nodes).
    - If a node appears in both sets, its description is updated to match whatever is in parsed_nodes
      (assuming the manual ASCII tree is the "source of truth" for new comments).
    - If you want to handle newly introduced or removed nodes, you could reconcile them too, but usually
      this is handled by scanning and the standard update_state_with_changes. Here we focus on merging
      comments/annotations, particularly for removed items.

    Note: This function mutates the nodes in 'current_nodes' directly; it doesn't return anything.

    Args:
        current_nodes (List[Node]): The current node list (active + removed) from JSON state.
        parsed_nodes (List[Node]): The node list parsed from the ASCII tree, which may have updated descriptions.
    """
    current_map = {n.path: n for n in _flatten_nodes(current_nodes)}
    parsed_map = {n.path: n for n in _flatten_nodes(parsed_nodes)}

    print(f"[DEBUG] Parsed paths: {list(parsed_map.keys())}")
    print(f"[DEBUG] Current JSON paths: {list(current_map.keys())}")

    for path, parsed_node in parsed_map.items():
        if path in current_map:
            current_node = current_map[path]
            # If the parsed node has a (possibly new) description, override the current description
            if parsed_node.description and parsed_node.description != current_node.description:
                print(f"[MERGE] Updating description for: {path}")
                print(f"    Old: {current_node.description!r}")
                print(f"    New: {parsed_node.description!r}")
                current_node.description = parsed_node.description

            # Only add the removal note if both nodes are marked removed
            if parsed_node.status == "removed" and current_node.status == "removed":
                current_node.description = update_comment_for_removal(current_node.description)


def _flatten_nodes(nodes: List[Node]) -> List[Node]:
    """
    Recursively flattens the node tree into a list and normalizes paths to use '/' separators,
    removing any leading prefixes like 'tvg2/'.
    """
    result = []

    def traverse(n: Node):
        # Normalize path to Unix-style and strip leading project root (e.g., 'tvg2/')
        if n.path:
            normalized = n.path.replace("\\", "/").removeprefix("tvg2/").strip("/")
            n.path = normalized
        result.append(n)
        for child in n.children:
            traverse(child)

    for node in nodes:
        traverse(node)

    return result
