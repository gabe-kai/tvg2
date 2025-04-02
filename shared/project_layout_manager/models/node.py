# shared/project_layout_manager/models/node.py

from typing import List, Optional

class Node:
    """
    Represents a file or folder in the project layout.

    Attributes:
        name (str): The name of the file or folder.
        path (str): The relative or absolute path to this node.
        is_folder (bool): True if this node represents a folder, False otherwise.
        description (str): User-supplied comments about this node.
        status (str): 'active' if the file/folder currently exists, 'removed' otherwise.
        children (List['Node']): Child nodes if this node is a folder.
    """
    def __init__(self,
                 name: str,
                 path: str,
                 is_folder: bool = False,
                 description: str = "",
                 status: str = "active"):
        self.name = name
        self.path = path
        self.is_folder = is_folder
        self.description = description
        self.status = status  # Could be 'active' or 'removed'
        self.children: List['Node'] = []

    def add_child(self, child: 'Node') -> None:
        """
        Adds a new child node to this node's children list.
        """
        if not self.is_folder:
            raise ValueError(f"Cannot add a child to a non-folder node: {self.name}")
        self.children.append(child)

    def remove_child(self, child_name: str) -> None:
        """
        Removes (or marks as removed) a child node with the given name.
        """
        for child in self.children:
            if child.name == child_name:
                child.status = "removed"
                return
        raise ValueError(f"No child with the name {child_name} found under {self.name}")

    def mark_as_removed(self) -> None:
        """
        Marks this node as removed.
        """
        self.status = "removed"

    def find_child(self, child_name: str) -> Optional['Node']:
        """
        Finds and returns a child node by name, or None if not found.
        """
        return next((child for child in self.children if child.name == child_name), None)

    def __repr__(self) -> str:
        """
        String representation for debugging.
        """
        return (f"Node(name='{self.name}', path='{self.path}', is_folder={self.is_folder}, "
                f"description='{self.description}', status='{self.status}', "
                f"children={len(self.children)})")
