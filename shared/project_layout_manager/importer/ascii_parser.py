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
      - Removed nodes are marked with ' (removed)'.
      - Inline comments follow '#'.

    Example line:
        '├── file.py (removed)  # user-supplied comment'

    Returns:
        List[Node]: A list of top-level nodes, each potentially having children.
    """
    lines = markdown_text.splitlines()
    root_nodes: List[Node] = []
    node_stack: List[(int, Node)] = []

    for line in lines:
        if not line.strip():
            continue
        if '── ' not in line:
            continue

        indent_level, name, is_folder, is_removed, description = _parse_line(line)

        node = Node(
            name=name,
            path="",
            is_folder=is_folder,
            description=description,
            status="removed" if is_removed else "active"
        )

        while node_stack and node_stack[-1][0] >= indent_level:
            node_stack.pop()

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

        node_stack.append((indent_level, node))

    return root_nodes

def _parse_line(line: str):
    """
    Extracts the indentation level, name, folder flag, removed flag, and description from a line.
    """
    line_for_indent = line.replace('│   ', '    ')
    space_match = re.match(r"^(\s+)", line_for_indent)
    leading_spaces = len(space_match.group(1)) if space_match else 0
    indent_level = leading_spaces // 4

    line_stripped = line.strip()
    line_stripped = re.sub(r"^[\s│]*[├└]──\s*", "", line_stripped)

    is_removed = False
    description = ""

    comment_match = re.search(r"\s#(.*)$", line_stripped)
    if comment_match:
        description = comment_match.group(1).strip()
        line_stripped = re.sub(r"\s#(.*)$", "", line_stripped).strip()
        if "[Removed on" in description:
            is_removed = True

    name = line_stripped
    is_folder = name.endswith('/')
    if is_folder:
        name = name[:-1]

    return indent_level, name, is_folder, is_removed, description
