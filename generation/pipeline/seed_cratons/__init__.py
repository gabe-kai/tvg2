# generation/pipeline/seed_cratons/__init__.py

"""
Strategy loader for craton seeding pipeline.
"""

from .base import SeedCratonsStrategy
from .spaced_random import SpacedRandomCratonSeeder


def get_strategy(name: str, **kwargs) -> SeedCratonsStrategy:
    """
    Load a craton seeding strategy by name.

    Args:
        name (str): The strategy name (e.g. "spaced_random")
        **kwargs: Parameters for the strategy constructor

    Returns:
        SeedCratonsStrategy: An instance of the selected strategy
    """
    if name == "spaced_random":
        return SpacedRandomCratonSeeder(**kwargs)
    raise ValueError(f"Unknown craton seeding strategy: {name}")
