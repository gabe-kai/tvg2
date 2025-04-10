# generation/models/planet.py
# Data structure representing a procedurally generated planet

from dataclasses import dataclass, field
from typing import Optional
import h5py
import numpy as np

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
        mesh_info = "✘"
        if self.mesh:
            num_faces = self.mesh.faces.shape[0]
            face_ids = '✔' if self.mesh.face_ids is not None else '✘'
            adjacency = '✔' if self.mesh.adjacency else '✘'
            mesh_info = f"✔ ({num_faces} faces, face_ids: {face_ids}, adjacency: {adjacency})"

        return (
            f"Planet(radius={self.radius}, subdivision_level={self.subdivision_level}, seed={self.seed})\n"
            f" - Mesh: {mesh_info}\n"
            f" - Cratons: {len(self.cratons)}\n"
            f" - Plates: {len(self.plates)}\n"
            f" - Elevation: {'✔' if self.elevation is not None else '✘'}\n"
            f" - Climate: {'✔' if self.climate is not None else '✘'}\n"
            f" - Biomes: {'✔' if self.biomes is not None else '✘'}\n"
            f" - Nations: {len(self.nations)}"
        )

    def save(self, path: str):
        """Save the current planet to a .planetbin HDF5 file."""
        with h5py.File(path, "w") as f:
            # Core
            f.attrs["radius"] = self.radius
            f.attrs["subdivision_level"] = self.subdivision_level
            f.attrs["seed"] = self.seed

            print(f"Saving planet with {self.mesh.faces.shape[0]} faces and face_ids: {self.mesh.face_ids is not None}")

            # Mesh
            if self.mesh:
                mesh_grp = f.create_group("mesh")
                mesh_grp.create_dataset("vertices", data=self.mesh.vertices)
                mesh_grp.create_dataset("faces", data=self.mesh.faces)
                # Convert adjacency dict to ragged array
                adj = [np.array(v, dtype=np.int32) for v in self.mesh.adjacency.values()]
                mesh_grp.create_dataset("adjacency_lengths", data=[len(v) for v in adj])
                mesh_grp.create_dataset("adjacency_flat", data=np.concatenate(adj))
                # Save face IDs
                if self.mesh.face_ids is None:
                    print("Generating face IDs before export...")
                    self.mesh.face_ids = np.arange(self.mesh.faces.shape[0], dtype=np.int32)
                mesh_grp.create_dataset("face_ids", data=self.mesh.face_ids)

    @staticmethod
    def load(path: str) -> "Planet":
        """Load a Planet from a .planetbin HDF5 file."""
        with h5py.File(path, "r") as f:
            radius = f.attrs["radius"]
            subdivision_level = f.attrs["subdivision_level"]
            seed = f.attrs["seed"]

            mesh = None
            if "mesh" in f:
                mesh_grp = f["mesh"]
                vertices = mesh_grp["vertices"][:]
                faces = mesh_grp["faces"][:]
                face_ids = mesh_grp["face_ids"][:] if "face_ids" in mesh_grp else None

                # Reconstruct adjacency dict
                lengths = mesh_grp["adjacency_lengths"][:]
                flat = mesh_grp["adjacency_flat"][:]
                adjacency = {}
                cursor = 0
                for i, length in enumerate(lengths):
                    adjacency[i] = flat[cursor:cursor+length].tolist()
                    cursor += length

                mesh = MeshData(vertices=vertices, faces=faces, adjacency=adjacency, face_ids=face_ids)

            return Planet(
                radius=radius,
                subdivision_level=subdivision_level,
                seed=seed,
                mesh=mesh
            )
