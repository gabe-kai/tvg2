# shared/project_layout_manager/models/comment_manager.py

import datetime
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
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    removal_msg = f"[Removed on {timestamp}]"

    # Avoid duplicating the note if it’s already present
    if removal_msg in existing_comment:
        return existing_comment

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

    for path, parsed_node in parsed_map.items():
        if path in current_map:
            current_node = current_map[path]
            # If the parsed node has a (possibly new) description, override the current description
            if parsed_node.description and parsed_node.description != current_node.description:
                current_node.description = parsed_node.description

            # If the parsed node is marked removed, you could optionally
            # update or append a custom note:
            if parsed_node.status == "removed" and current_node.status != "removed":
                current_node.status = "removed"
                # Append a removal note
                current_node.description = update_comment_for_removal(current_node.description)

        # Optionally handle nodes that are in parsed_map but not in current_map (if you allow
        # the ASCII tree to introduce brand-new items). Most workflows handle that through scanning.
        # else:
        #     pass

def _flatten_nodes(nodes: List[Node]) -> List[Node]:
    """
    Recursively flattens the entire hierarchy into a single list of Node objects.
    """
    result = []

    def traverse(n: Node):
        result.append(n)
        for child in n.children:
            traverse(child)

    for node in nodes:
        traverse(node)

    return result
