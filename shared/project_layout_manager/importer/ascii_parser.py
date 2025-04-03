# shared/project_layout_manager/importers/ascii_parser.py

import re
from typing import List
from shared.project_layout_manager.models.node import Node


def parse_ascii_tree(markdown_text: str) -> List[Node]:
    """
    Parses an ASCII tree from Markdown (or any text) and returns a list of top-level Node objects.
    The parser assumes:
      - Lines containing nodes use symbols like '├──', '└──', and '│   ' (or '    ').
      - Folders end with '/'.
      - Comments (descriptions) follow '#'.
      - *Removal status is NOT assigned here.* The scanner determines removal.

    Example line:
        '├── file.py  # some comment'

    Returns:
        List[Node]: A list of top-level nodes, each potentially having children.
    """
    lines = markdown_text.splitlines()
    root_nodes: List[Node] = []
    node_stack: List[(int, Node)] = []

    for line in lines:
        # Skip empty lines or lines without the '── ' connector
        if not line.strip():
            continue
        if '── ' not in line:
            continue

        indent_level, name, is_folder, description = _parse_line(line)

        # Always treat as active here
        node = Node(
            name=name,
            path="",  # We'll set it below
            is_folder=is_folder,
            description=description,
            status="active"  # This parser never marks anything as removed
        )

        # Pop from node_stack while our indent_level is not deeper
        while node_stack and node_stack[-1][0] >= indent_level:
            node_stack.pop()

        # Append to parent's children or top-level
        if node_stack:
            parent_node = node_stack[-1][1]
            parent_node.children.append(node)
        else:
            root_nodes.append(node)

        # Build full path from parent (before adding to stack)
        if node_stack:
            parent_path = node_stack[-1][1].path
            node.path = f"{parent_path}/{node.name}"
        else:
            node.path = node.name

        # Push (indent_level, node) to the stack
        node_stack.append((indent_level, node))

    return root_nodes


def _parse_line(line: str):
    """
    Extracts the indentation level, name, folder flag, and description from a single ASCII tree line.
    This parser does NOT interpret '(removed)' or '[Removed on ...]' as removal.
    The scanner logic decides if files are missing or removed.
    """
    # Normalize indentation by replacing '│   ' with '    '
    line_for_indent = line.replace('│   ', '    ')
    space_match = re.match(r"^(\s+)", line_for_indent)
    leading_spaces = len(space_match.group(1)) if space_match else 0
    indent_level = leading_spaces // 4

    # Strip the leading tree connector like '├── ' or '└── '
    line_stripped = line.strip()
    line_stripped = re.sub(r"^[\s│]*[├└]──\s*", "", line_stripped)

    # Extract description from anything after '#'
    description = ""
    comment_match = re.search(r"\s#(.*)$", line_stripped)
    if comment_match:
        description = comment_match.group(1).strip()
        # Remove the comment portion from the main line
        line_stripped = re.sub(r"\s#(.*)$", "", line_stripped).strip()

    # Determine if it's a folder by trailing slash
    is_folder = line_stripped.endswith('/')
    if is_folder:
        line_stripped = line_stripped[:-1]

    name = line_stripped

    return indent_level, name, is_folder, description
