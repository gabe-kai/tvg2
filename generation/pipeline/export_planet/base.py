# generation/pipeline/export_planet/base.py

from abc import ABC, abstractmethod
from generation.models.planet import Planet


class BaseExportPlanetStrategy(ABC):
    @abstractmethod
    def run(self, planet: Planet) -> Planet:
        """Serialize the planet to disk and return it unchanged."""
        pass
