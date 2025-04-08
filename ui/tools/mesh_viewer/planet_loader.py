# ui/tools/mesh_viewer/planet_loader.py

from pathlib import Path
import h5py
import numpy as np

from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from shared.logging.logger import get_logger

log = get_logger(__name__)


def load_mesh_render_data(path: str | Path) -> MeshRenderData:
    """
    Load a .planetbin file and extract mesh data for rendering.
    Only the minimal data needed for MeshRenderData is loaded.
    """
    path = Path(path)
    log.info(f"Loading .planetbin file from: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Planet file not found: {path}")

    with h5py.File(path, "r") as f:
        vertices = np.array(f["mesh/vertices"])
        faces = np.array(f["mesh/faces"])

        # Optional fields
        elevation = None
        face_ids = None

        if "elevation/values" in f:
            elevation = np.array(f["elevation/values"])
        if "face_ids" in f["mesh"]:
            face_ids = np.array(f["mesh/face_ids"])

    log.info(f"Loaded mesh: {len(vertices)} vertices, {len(faces)} faces")
    log.debug(f"Elevation: {'present' if elevation is not None else 'absent'}; Face IDs: {'present' if face_ids is not None else 'absent'}")
    if face_ids is not None:
        log.debug(f"Loaded {len(face_ids)} face IDs")
    return MeshRenderData(vertices=vertices, faces=faces,
                          elevation=elevation, face_ids=face_ids)
