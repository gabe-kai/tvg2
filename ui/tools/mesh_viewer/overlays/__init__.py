# ui/tools/mesh_viewer/overlays/__init__.py

from .base import Overlay
from .face_index_overlay import FaceIndexOverlay
from .face_normals_overlay import FaceNormalsOverlay
#from .craton_overlay import CratonOverlay

ALL_OVERLAYS = [
    FaceIndexOverlay,
    FaceNormalsOverlay,
    # CratonOverlay,
]
