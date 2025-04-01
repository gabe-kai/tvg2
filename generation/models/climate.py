# generation/models/climate.py
from dataclasses import dataclass
import numpy as np

@dataclass
class ClimateData:
    temperature: np.ndarray          # shape (num_faces,)
    precipitation: np.ndarray       # shape (num_faces,)
