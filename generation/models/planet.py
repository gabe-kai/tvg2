# generation/models/planet.py
# -----------------------------------
# Data structure representing a procedurally generated planet

from dataclasses import dataclass, field
from typing import Optional

from generation.models.mesh import MeshData
from generation.models.tectonics import Craton, Plate, PlateMap
from generation.models.elevation import ElevationMap, DrainageMap
from generation.models.climate import ClimateData
from generation.models.biomes import BiomeMap
from generation.models.regions import RegionMap
from generation.models.politics import Nation, PoliticalMap


@dataclass
class Planet:
    # Core configuration
    radius: float
    subdivision_level: int
    seed: int

    # Mesh data
    mesh: Optional[MeshData] = None

    # Cratons and tectonics
    cratons: list[Craton] = field(default_factory=list)
    plates: list[Plate] = field(default_factory=list)
    plate_map: Optional[PlateMap] = None

    # Elevation and erosion
    elevation: Optional[ElevationMap] = None
    drainage: Optional[DrainageMap] = None

    # Climate
    climate: Optional[ClimateData] = None

    # Biomes
    biomes: Optional[BiomeMap] = None

    # Regions and labeling
    regions: Optional[RegionMap] = None

    # Politics
    political_map: Optional[PoliticalMap] = None
    nations: list[Nation] = field(default_factory=list)

    def summary(self) -> str:
        return (
            f"Planet(radius={self.radius}, subdivision_level={self.subdivision_level}, seed={self.seed})\n"
            f" - Mesh: {'✔' if self.mesh is not None else '✘'}\n"
            f" - Cratons: {len(self.cratons)}\n"
            f" - Plates: {len(self.plates)}\n"
            f" - Elevation: {'✔' if self.elevation is not None else '✘'}\n"
            f" - Climate: {'✔' if self.climate is not None else '✘'}\n"
            f" - Biomes: {'✔' if self.biomes is not None else '✘'}\n"
            f" - Nations: {len(self.nations)}"
        )
