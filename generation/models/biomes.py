# generation/models/biomes.py
from dataclasses import dataclass
import numpy as np

@dataclass
class BiomeMap:
    biome_ids: np.ndarray            # shape (num_faces,)
