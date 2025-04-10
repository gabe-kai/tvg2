# generation/models/tectonics.py

"""
Geological data structures for tectonic modeling.

- Craton: ancient, undeformable core region of a plate
- Plate: mobile lithospheric segment potentially composed of one or more cratons
- PlateMap: mapping from mesh face index to tectonic plate ID
"""

from dataclasses import dataclass
from typing import List
import numpy as np

@dataclass
class Craton:
    """
    Represents an ancient, stable region of the planet's lithosphere.

    Attributes:
        center_index: The mesh face index representing the core of the craton
        id: A unique identifier for this craton
        face_ids: Optional list of face indices that make up the craton's region
        name: Optional human-readable name for display or debugging
    """
    center_index: int
    id: int
    face_ids: List[int] = None
    name: str = None

@dataclass
class Plate:
    """
    Represents a tectonic plate that moves and deforms under geophysical forces.

    Attributes:
        id: Unique plate ID
        craton_ids: List of craton IDs that form the structural core of the plate
        motion_vector: A 3D unit vector representing motion direction in world space
    """
    id: int
    craton_ids: List[int]
    motion_vector: np.ndarray        # shape (3,)

@dataclass
class PlateMap:
    """
    Maps each mesh face to a tectonic plate.

    Attributes:
        face_to_plate: Array mapping face index to a plate ID (shape: num_faces,)
    """
    face_to_plate: np.ndarray        # shape (num_faces,)
