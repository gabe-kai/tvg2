# shared/project_layout_manager/exporters/ascii_exporter.py

from typing import List
from shared.project_layout_manager.models.node import Node

def export_ascii_tree(nodes: List[Node], include_removed: bool = False) -> str:
    """
    Exports nodes to a classic ASCII tree with vertical pipes.
    Adds a spacer line if a folder's last child is a file, after listing that file.
    Sorts folders first (alphabetically), then files (alphabetically), recursively.
    """
    # Filter out removed nodes if not including them
    top_level = [n for n in nodes if include_removed or n.status != "removed"]

    # Sort: folders first, then files, both alphabetically by name
    top_level.sort(key=lambda n: (not n.is_folder, n.name.lower()))

    lines = []
    for i, node in enumerate(top_level):
        is_last_child = (i == len(top_level) - 1)
        lines.extend(
            _build_subtree(
                node=node,
                ancestors=[],
                is_last_child=is_last_child,
                include_removed=include_removed
            )
        )

    return "\n".join(lines)

def _build_subtree(node: Node,
                   ancestors: List[bool],
                   is_last_child: bool,
                   include_removed: bool) -> List[str]:
    """
    Recursively builds a list of lines for 'node' and its children using a boolean array
    to track vertical pipes. Inserts a spacer line after the last child if it's a file.
    """
    lines = []

    # Build the prefix from ancestors
    prefix = _build_prefix(ancestors)

    # Connector for this node
    connector = "└── " if is_last_child else "├── "

    # Build the label
    label = node.name + ("/" if node.is_folder else "")
    if node.status == "removed":
        label += " (removed)"

    # Combine final text for this node
    current_line = prefix + connector + label

    # If there's a description, put # comment after it
    if node.description:
        current_line += f"  # {node.description}"

    lines.append(current_line)

    # Filter children if ignoring removed
    filtered_children = [c for c in node.children if include_removed or c.status != "removed"]

    # Sort children: folders first, then files, both alphabetically by name
    filtered_children.sort(key=lambda n: (not n.is_folder, n.name.lower()))

    # Recurse for children
    for i, child in enumerate(filtered_children):
        child_is_last = (i == len(filtered_children) - 1)
        lines.extend(
            _build_subtree(
                node=child,
                ancestors=ancestors + [is_last_child],
                is_last_child=child_is_last,
                include_removed=include_removed
            )
        )

    # ---------------------------------------------
    # SPACER LOGIC:
    # If this node is a folder, check its last child.
    # If that last child is a file, insert a spacer line
    # (with pipes from the ancestors).
    # ---------------------------------------------
    if node.is_folder and filtered_children:
        last_child = filtered_children[-1]
        if not last_child.is_folder:
            # That last child is a file, so we append a spacer line
            # Use prefix for *this folder* because we haven't "closed out" the folder's level yet
            spacer_prefix = _build_prefix(ancestors + [is_last_child])
            lines.append(spacer_prefix)  # blank line, just the vertical pipes

    return lines

def _build_prefix(ancestors: List[bool]) -> str:
    """
    Builds a prefix based on the list of booleans:
      - True => ancestor was last child => "    "
      - False => ancestor had more siblings => "│   "
    """
    parts = []
    for was_last in ancestors:
        parts.append("    " if was_last else "│   ")
    return "".join(parts)
