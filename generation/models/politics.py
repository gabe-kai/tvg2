# generation/models/politics.py
from dataclasses import dataclass
from typing import List, Dict, Any
import numpy as np

@dataclass
class Nation:
    name: str
    capital: int                     # face index
    territory: List[int]             # face indices
    metadata: Dict[str, Any]         # optional tags (color, culture, etc.)

@dataclass
class PoliticalMap:
    face_to_nation: np.ndarray       # shape (num_faces,)
