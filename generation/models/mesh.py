# generation/models/mesh.py
from dataclasses import dataclass
import numpy as np
from typing import Dict, List

@dataclass
class MeshData:
    vertices: np.ndarray              # shape (N, 3)
    faces: np.ndarray                 # shape (M, 3)
    adjacency: Dict[int, List[int]]  # face index -> neighboring face indices
