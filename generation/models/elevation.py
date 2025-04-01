# generation/models/elevation.py
from dataclasses import dataclass
import numpy as np

@dataclass
class ElevationMap:
    elevation: np.ndarray            # shape (num_vertices,) or (num_faces,)

@dataclass
class DrainageMap:
    flow: np.ndarray                 # optional water flow vector or volume
