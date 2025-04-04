# ui/tools/mesh_viewer/viewer_app.py

from PySide6.QtWidgets import QMainWindow, QApplication
from PySide6.QtCore import Qt

from ui.tools.mesh_viewer.gl_widget import PlanetGLWidget
from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from shared.logging.logger import get_logger

log = get_logger(__name__)


class PlanetViewerApp(QMainWindow):
    """
    Main application window for the mesh viewer. Hosts a PlanetGLWidget for 3D rendering.
    """

    def __init__(self, mesh_data: MeshRenderData, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Planet Mesh Viewer")
        self.setMinimumSize(800, 600)

        log.info("Initializing PlanetViewerApp...")
        self.mesh_widget = PlanetGLWidget(mesh_data)
        self.setCentralWidget(self.mesh_widget)
        log.info("Viewer window initialized.")
