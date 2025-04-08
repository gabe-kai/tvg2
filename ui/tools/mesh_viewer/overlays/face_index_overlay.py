# ui/tools/mesh_viewer/overlays/face_index_overlay.py

from PySide6.QtGui import QPainter, QColor, QFont
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from OpenGL.GL import (glGetDoublev, glGetIntegerv, GL_MODELVIEW_MATRIX, GL_PROJECTION_MATRIX,
                       GL_VIEWPORT, glDisable, glEnable, GL_DEPTH_TEST, GL_FRONT_AND_BACK, GL_FILL,
                       GL_POLYGON_MODE, glPolygonMode)
from OpenGL.GLU import gluProject
import numpy as np

from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from ui.tools.mesh_viewer.overlays.base import Overlay
from shared.logging.logger import get_logger

log = get_logger(__name__)


class FaceIndexOverlay(Overlay):
    """
    Displays the numeric ID of each face at its center using QPainter.
    """

    def __init__(self):
        super().__init__()
        self.face_ids = None
        self.face_centers = None

    def get_name(self) -> str:
        return "Face Index"

    def get_category(self) -> str:
        return "Debug"

    def get_description(self) -> str:
        return "Displays the numeric ID of each face at its center."

    def update_data(self, mesh_data: MeshRenderData) -> None:
        if mesh_data.face_ids is None:
            self.face_ids = None
            self.face_centers = None
            return

        self.face_ids = mesh_data.face_ids

        # Compute center point of each face
        vertices = mesh_data.vertices
        faces = mesh_data.faces
        self.face_centers = np.mean(vertices[faces], axis=1)
        log.debug(f"FaceIndexOverlay: computed {len(self.face_centers)} face centers")

    def render(self, gl_widget: QOpenGLWidget) -> None:
        # This overlay only uses QPainter
        pass

    def render_qpainter(self, painter: QPainter, gl_widget: QOpenGLWidget) -> None:
        if not self.is_enabled():
            log.debug("FaceIndexOverlay: disabled, skipping draw")
            return
        if self.face_ids is None or self.face_centers is None:
            return

        gl_widget.makeCurrent()
        # Temporarily switch polygon mode to fill so text isn't affected by wireframe
        current_mode = glGetIntegerv(GL_POLYGON_MODE)
        if isinstance(current_mode, np.ndarray):
            current_mode = int(current_mode[0])
        glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        glDisable(GL_DEPTH_TEST)  # Disable depth test to draw labels in front

        painter.setRenderHint(QPainter.TextAntialiasing)
        font = QFont("Courier New")
        font.setPixelSize(14)
        painter.setFont(font)

        # Use global modelview once per frame
        modelview_global = glGetDoublev(GL_MODELVIEW_MATRIX).reshape((4, 4))
        visible = []  # (depth, idx, screen_pos)

        for idx, center in enumerate(self.face_centers):
            tri = gl_widget.mesh_data.faces[idx]
            v0, v1, v2 = gl_widget.mesh_data.vertices[tri]
            normal = np.cross(v1 - v0, v2 - v0)
            norm = np.linalg.norm(normal)
            if norm == 0:
                continue
            normal /= norm
            view_normal = modelview_global[:3, :3] @ normal
            if view_normal[2] >= 0:
                continue  # back‑facing

            # Depth = negative view‑space z (smaller means farther away)
            center_h = np.append(center, 1.0)
            view_center = modelview_global @ center_h
            depth = -view_center[2]

            screen_pos = self._project_to_screen(center, gl_widget)
            if screen_pos is None:
                continue
            visible.append((depth, idx, screen_pos))

        # Sort nearest first and clamp to 100 faces
        visible.sort(key=lambda t: t[0])
        for depth, idx, (x, y) in visible[:100]:
            label = str(int(self.face_ids[idx]))
            # Drop shadow
            painter.setPen(QColor(0, 0, 128))
            painter.drawText(x + 1, y + 1, label)
            # Foreground
            painter.setPen(QColor(255, 255, 0))
            painter.drawText(x, y, label)

        glEnable(GL_DEPTH_TEST)
        # Restore polygon mode
        glPolygonMode(GL_FRONT_AND_BACK, current_mode)

    def _project_to_screen(self, point_3d: np.ndarray, gl_widget: QOpenGLWidget):
        """Convert 3D point to 2D screen coordinates using OpenGL projection."""
        try:
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            viewport = glGetIntegerv(GL_VIEWPORT).astype(np.int32)

            win_x, win_y, _ = gluProject(point_3d[0], point_3d[1], point_3d[2], modelview, projection, viewport)

            # Convert OpenGL origin (bottom-left) to Qt (top-left)
            qt_y = gl_widget.height() - int(win_y)
            return int(win_x), qt_y
        except Exception as e:
            log.warning(f"Projection failed for point {point_3d}: {e}")
            return None
