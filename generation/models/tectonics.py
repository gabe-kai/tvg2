# generation/models/tectonics.py

from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class Craton:
    center_index: int
    size: float
    id: int

@dataclass
class Plate:
    id: int
    craton_ids: List[int]
    motion_vector: np.ndarray        # shape (3,)

@dataclass
class PlateMap:
    face_to_plate: np.ndarray        # shape (num_faces,)
