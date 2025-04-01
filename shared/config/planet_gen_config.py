# shared/config/planet_gen_config.py

from dataclasses import dataclass


@dataclass
class PlanetGenConfig:
    """
    Configuration schema for generating a procedural planet.
    This config can be loaded from CLI, JSON, or UI input.
    """
    radius: float = 6371.0
    subdivision_level: int = 6
    seed: int = 42
    mesh_strategy: str = "icosphere"

    def to_dict(self) -> dict:
        return {
            "radius": self.radius,
            "subdivision_level": self.subdivision_level,
            "seed": self.seed,
            "mesh_strategy": self.mesh_strategy,
        }

    @staticmethod
    def from_dict(data: dict) -> "PlanetGenConfig":
        return PlanetGenConfig(
            radius=data.get("radius", 6371.0),
            subdivision_level=data.get("subdivision_level", 6),
            seed=data.get("seed", 42),
            mesh_strategy=data.get("mesh_strategy", "icosphere"),
        )
