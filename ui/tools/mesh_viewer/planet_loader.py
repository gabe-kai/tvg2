# ui/tools/mesh_viewer/planet_loader.py

from pathlib import Path
from generation.models.planet import Planet
from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from shared.logging.logger import get_logger

log = get_logger(__name__)


def load_mesh_render_data(path: str | Path) -> MeshRenderData:
    """
    Load a .planetbin file and extract mesh data for rendering.
    """
    path = Path(path)
    log.info(f"Loading .planetbin file from: {path}")

    if not path.exists():
        raise FileNotFoundError(f"Planet file not found: {path}")

    planet = Planet.load(path)
    mesh = planet.mesh

    log.info(f"Loaded mesh: {len(mesh.vertices)} vertices, {len(mesh.faces)} faces")
    log.debug(f"Elevation: {'present' if planet.elevation is not None else 'absent'}; Face IDs: {'present' if mesh.face_ids is not None else 'absent'}")
    if mesh.face_ids is not None:
        log.debug(f"Loaded {len(mesh.face_ids)} face IDs")

    return MeshRenderData(
        vertices=mesh.vertices,
        faces=mesh.faces,
        elevation=planet.elevation,
        face_ids=mesh.face_ids,
        planet=planet
    )
