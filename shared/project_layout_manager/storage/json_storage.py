# shared/project_layout_manager/storage/json_storage.py

import json
from pathlib import Path
from typing import List, Dict, Any

from shared.project_layout_manager.models.node import Node

def load_state(json_file: str) -> List[Node]:
    """
    Loads the project layout from the specified JSON file and returns a list of Node objects.
    If the file doesn't exist or is empty, returns an empty list.
    """
    file_path = Path(json_file)
    if not file_path.is_file():
        # File does not exist; return an empty list
        return []

    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            data = json.load(f)
        except json.JSONDecodeError:
            # If file is corrupted or empty, treat as no state
            return []

    # If data is empty or not a list, return an empty list
    if not isinstance(data, list):
        return []

    # Convert each dict in the list back into a Node object
    return [dict_to_node(item) for item in data]

def save_state(nodes: List[Node], json_file: str) -> None:
    """
    Saves the given list of Node objects to the specified JSON file.
    Overwrites any existing content in the file.
    """
    file_path = Path(json_file)
    file_path.parent.mkdir(parents=True, exist_ok=True)  # Ensure directory exists

    # Convert each Node object into a serializable dict
    data = [node_to_dict(node) for node in nodes]

    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4)

def dict_to_node(data: Dict[str, Any]) -> Node:
    """
    Recursively converts a dict structure into a Node object and its children.
    """
    node = Node(
        name=data.get("name", ""),
        path=data.get("path", ""),
        is_folder=data.get("is_folder", False),
        description=data.get("description", ""),
        status=data.get("status", "active")
    )

    children_data = data.get("children", [])
    for child_dict in children_data:
        child_node = dict_to_node(child_dict)
        node.children.append(child_node)

    return node

def node_to_dict(node: Node) -> Dict[str, Any]:
    """
    Recursively converts a Node object (and its children) into a dict
    that can be serialized to JSON.
    """
    return {
        "name": node.name,
        "path": node.path,
        "is_folder": node.is_folder,
        "description": node.description,
        "status": node.status,
        "children": [node_to_dict(child) for child in node.children]
    }
