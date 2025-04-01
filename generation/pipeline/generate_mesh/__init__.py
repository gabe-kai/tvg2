# generation/pipeline/generate_mesh/__init__.py

from .base import BaseMeshStrategy
from .icosphere import IcosphereMeshStrategy


def get_strategy(name: str) -> BaseMeshStrategy:
    """
    Factory function to retrieve a mesh generation strategy by name.

    Args:
        name (str): The name of the mesh strategy (e.g., 'icosphere').

    Returns:
        BaseMeshStrategy: An instance of the selected strategy.
    """
    if name == "icosphere":
        return IcosphereMeshStrategy()

    raise ValueError(f"Unknown mesh strategy: {name}")
