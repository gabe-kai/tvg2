# generation/pipeline/generate_mesh/base.py

from abc import ABC, abstractmethod
from generation.models.planet import Planet


class BaseMeshStrategy(ABC):
    """
    Abstract base class for all mesh generation strategies.
    Each strategy must implement the run method that builds
    the mesh and attaches it to the Planet object.
    """

    @abstractmethod
    def run(self, planet: Planet) -> Planet:
        """
        Generate and attach mesh data to the given planet.

        Args:
            planet (Planet): The planet object to modify.

        Returns:
            Planet: The modified planet with mesh data attached.
        """
        pass
