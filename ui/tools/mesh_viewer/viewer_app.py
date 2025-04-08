# ui/tools/mesh_viewer/viewer_app.py

from PySide6.QtWidgets import QMainWindow, QApplication, QToolBar
from PySide6.QtGui import QAction
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

        self._init_toolbar()
        log.info("Viewer window initialized.")

    def _init_toolbar(self):
        """Create and populate the viewer control toolbar."""
        toolbar = QToolBar("Viewer Controls")
        self.addToolBar(Qt.ToolBarArea.TopToolBarArea, toolbar)

        # Wireframe toggle
        self.wireframe_action = QAction("Wireframe Mode", self)
        self.wireframe_action.setCheckable(True)
        self.wireframe_action.setChecked(self.mesh_widget.show_wireframe)
        self.wireframe_action.triggered.connect(self.mesh_widget.set_show_wireframe)
        toolbar.addAction(self.wireframe_action)

        # Rotation lock toggle
        self.rotation_lock_action = QAction("Lock Rotation", self)
        self.rotation_lock_action.setCheckable(True)
        self.rotation_lock_action.setChecked(self.mesh_widget.rotation_locked)
        self.rotation_lock_action.triggered.connect(self.mesh_widget.set_rotation_locked)
        toolbar.addAction(self.rotation_lock_action)

        # Auto-rotate toggle
        self.auto_rotate_action = QAction("Auto-Rotate", self)
        self.auto_rotate_action.setCheckable(True)
        self.auto_rotate_action.setChecked(self.mesh_widget.auto_rotate)
        self.auto_rotate_action.triggered.connect(self.mesh_widget.set_auto_rotate)
        toolbar.addAction(self.auto_rotate_action)
