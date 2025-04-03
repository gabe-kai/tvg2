# shared/project_layout_manager/exporters/flat_exporter.py

from typing import List
from shared.project_layout_manager.models.node import Node


def export_flat_list(nodes: List[Node], include_removed: bool = False) -> str:
    """
    Returns a simple, newline-separated list of all file/folder paths in the given nodes.

    Args:
        nodes (List[Node]): A list of top-level Node objects.
        include_removed (bool): Whether to include nodes marked as 'removed'.

    Returns:
        str: A list of paths, one path per line.
    """
    # Gather all nodes (including children)
    all_nodes = _flatten_nodes(nodes, include_removed)

    # Create a sorted list of paths for consistent output (optional)
    all_nodes.sort(key=lambda n: n.path)

    # Build output lines.
    # You could also include a "(removed)" tag if you like, or skip them entirely
    lines = []
    for node in all_nodes:
        path_line = node.path
        if node.status == "removed":
            path_line += " (removed)"
        if node.description:
            path_line += f"  // {node.description}"
        lines.append(path_line)

    return "\n".join(lines)


def _flatten_nodes(nodes: List[Node], include_removed: bool) -> List[Node]:
    """
    Recursively flattens the node hierarchy into a single list.
    """
    result = []

    def _traverse(n: Node):
        if include_removed or n.status != "removed":
            result.append(n)
        for child in n.children:
            _traverse(child)

    for node in nodes:
        _traverse(node)

    return result
