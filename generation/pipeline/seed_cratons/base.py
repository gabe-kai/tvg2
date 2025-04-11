# generation/pipeline/seed_cratons/base.py

"""
Base interface for craton seeding strategies.
Each strategy should take a Planet and return a modified version with cratons assigned.
"""

from abc import ABC, abstractmethod
from generation.models.planet import Planet

class SeedCratonsStrategy(ABC):
    """
    Abstract base class for craton seeding strategies.

    Subclasses must implement the `run()` method, which takes a Planet
    and returns a modified Planet with cratons assigned to it.
    """

    @abstractmethod
    def run(self, planet: Planet) -> Planet:
        """
        Apply craton seeding logic to the provided Planet instance.

        Args:
            planet (Planet): The planet to modify.

        Returns:
            Planet: The modified planet with craton data populated.
        """
        pass
