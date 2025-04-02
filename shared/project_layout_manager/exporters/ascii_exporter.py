# shared/project_layout_manager/exporters/ascii_exporter.py

from typing import List
from shared.project_layout_manager.models.node import Node


def export_ascii_tree(nodes: List[Node], include_removed: bool = False) -> str:
    """
    Generates a multi-line ASCII tree representation of the given nodes and their children.

    Args:
        nodes (List[Node]): A list of top-level Node objects.
        include_removed (bool): Whether to include nodes marked as 'removed'.

    Returns:
        str: The ASCII tree as a single string, with newlines included.
    """
    lines = []
    # Filter out removed nodes if include_removed=False
    filtered_nodes = [n for n in nodes if include_removed or n.status != "removed"]

    for i, node in enumerate(filtered_nodes):
        is_last = (i == len(filtered_nodes) - 1)
        lines.extend(_build_ascii_subtree(node, prefix="", is_last=is_last, include_removed=include_removed))

    return "\n".join(lines)


def _build_ascii_subtree(node: Node,
                         prefix: str,
                         is_last: bool,
                         include_removed: bool) -> List[str]:
    """
    Recursively builds a list of lines for a single node and its children.
    """
    connector = "└── " if is_last else "├── "
    node_indicator = node.name + ("/" if node.is_folder else "")

    # Format the line for the current node
    line = f"{prefix}{connector}{node_indicator}"
    if node.status == "removed":
        line += " (removed)"
    if node.description:
        line += f"  // {node.description}"

    lines = [line]

    # Determine the new prefix for child nodes
    child_prefix = prefix + ("    " if is_last else "│   ")

    # Filter children if not including removed nodes
    filtered_children = [c for c in node.children if include_removed or c.status != "removed"]

    # Recurse for each child
    for i, child in enumerate(filtered_children):
        child_is_last = (i == len(filtered_children) - 1)
        lines.extend(_build_ascii_subtree(child, child_prefix, child_is_last, include_removed))

    return lines
