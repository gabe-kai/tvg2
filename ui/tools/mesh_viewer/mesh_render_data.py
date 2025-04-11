# ui/tools/mesh_viewer/mesh_render_data.py

from dataclasses import dataclass
from typing import Optional
import numpy as np


@dataclass
class MeshRenderData:
    """
    Lightweight data structure for rendering a planet mesh.
    Decouples the viewer from full Planet and MeshData models.
    """
    vertices: np.ndarray         # Shape: (n, 3)
    faces: np.ndarray            # Shape: (m, 3), indices into vertices
    face_ids: Optional[np.ndarray] = None   # Shape: (m,)
    elevation: Optional[np.ndarray] = None  # Shape: (n,) or (m,)
    planet: Optional["Planet"] = None       # Full Planet object for overlay/debugging access

    def __post_init__(self):
        assert self.vertices.ndim == 2 and self.vertices.shape[1] == 3, \
            "Vertices must be a 2D array with shape (n, 3)"
        assert self.faces.ndim == 2 and self.faces.shape[1] == 3, \
            "Faces must be a 2D array with shape (m, 3)"
        if self.face_ids is not None:
            assert self.face_ids.shape[0] == self.faces.shape[0], \
                "face_ids length must match number of faces"
        if self.elevation is not None:
            assert self.elevation.shape[0] in (self.vertices.shape[0], self.faces.shape[0]), \
                "elevation must match either number of vertices or faces"
