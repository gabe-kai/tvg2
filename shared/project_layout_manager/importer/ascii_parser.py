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
      - Inline comments follow '//'.

    Example line:
        '├── file.py (removed) // user-supplied comment'

    Returns:
        List[Node]: A list of top-level nodes, each potentially having children.
    """
    lines = markdown_text.splitlines()
    root_nodes: List[Node] = []
    # We'll keep track of the current "path" up the tree using a stack.
    # Each entry is (indent_level, node). When we parse a new line,
    # we pop from the stack until we find a parent whose indent_level < new_line_indent.
    node_stack: List[(int, Node)] = []

    for line in lines:
        # Skip completely empty lines or lines that don't seem to have tree connectors
        if not line.strip():
            continue
        if '── ' not in line:  # crude check for lines containing '├──' or '└──'
            continue

        indent_level, name, is_folder, is_removed, description = _parse_line(line)

        # Create a new node for this line
        node = Node(
            name=name,
            path="",  # We'll leave path empty or reconstruct later if desired
            is_folder=is_folder,
            description=description,
            status="removed" if is_removed else "active"
        )

        # Find the correct parent by comparing indent levels
        while node_stack and node_stack[-1][0] >= indent_level:
            node_stack.pop()

        if node_stack:
            # The top of the stack is our parent
            parent_node = node_stack[-1][1]
            if parent_node.is_folder:
                parent_node.children.append(node)
            else:
                # If parent isn't a folder, we can't attach children to it
                # but let's attach anyway or raise an error (depending on your preference).
                parent_node.children.append(node)
        else:
            # This is a top-level node
            root_nodes.append(node)

        # Push this node onto the stack
        node_stack.append((indent_level, node))

    return root_nodes


def _parse_line(line: str):
    """
    Extracts the indentation level, name, folder flag, removed flag, and description from a line.
    A sample line might look like:
       '    ├── some_file.py (removed) // This is a comment'

    We:
      1. Count how many leading spaces or vertical bars + spaces to estimate indent level.
      2. Identify '(removed)' if present.
      3. Identify '// <comment>' if present.
      4. Check if the name ends with '/' to decide if it's a folder.

    Returns:
       indent_level (int)
       name (str)
       is_folder (bool)
       is_removed (bool)
       description (str)
    """
    # A rough approach: replace '│   ' with '    ' so it’s consistent in terms of spaces
    # for indent counting. This ensures each "level" of tree = 4 spaces in indentation.
    # If you have more complex spacing, you might refine this.
    line_for_indent = line.replace('│   ', '    ')

    # Count leading spaces to determine indentation level.
    # We'll treat every 4 leading spaces as 1 level.
    space_match = re.match(r"^(\s+)", line_for_indent)
    leading_spaces = len(space_match.group(1)) if space_match else 0
    indent_level = leading_spaces // 4

    # Now strip off leading/trailing whitespace to simplify matching
    line_stripped = line.strip()

    # Remove the connectors like '├──' or '└──' (and potential extra spaces)
    # This should leave us with "filename (removed) // comment" or "folder/ // comment" etc.
    line_stripped = re.sub(r"^[├└]──\s*", "", line_stripped)

    # Detect and separate '(removed)'
    is_removed = '(removed)' in line_stripped
    if is_removed:
        line_stripped = line_stripped.replace('(removed)', '').strip()

    # Detect and separate the comment
    description = ""
    if '//' in line_stripped:
        parts = line_stripped.split('//', maxsplit=1)
        line_stripped = parts[0].strip()
        description = parts[1].strip()

    # The name is whatever remains in line_stripped
    name = line_stripped

    # Check if it ends with '/'
    is_folder = False
    if name.endswith('/'):
        is_folder = True
        # remove the trailing slash for the name if you prefer
        name = name[:-1]

    return indent_level, name, is_folder, is_removed, description
