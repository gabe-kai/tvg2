# ui/tools/mesh_viewer/gl_widget.py

from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QMouseEvent, QWheelEvent, QPainter
from PySide6.QtCore import Qt, QPoint, QTimer

from OpenGL.raw.GLU import gluPerspective
from OpenGL.GL import *
import numpy as np
import math
from enum import Enum

from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from shared.logging.logger import get_logger
from ui.tools.mesh_viewer.overlay_manager import OverlayManager
from ui.tools.mesh_viewer.overlays import ALL_OVERLAYS

log = get_logger(__name__)


class RenderMode(Enum):
    WIREFRAME = "wireframe"
    FLAT_SHADED = "flat"
    SUNLIT = "sunlit"


class PlanetGLWidget(QOpenGLWidget):
    """
    OpenGL rendering widget for displaying a planet mesh in wireframe or filled mode.
    """

    def __init__(self, mesh_data: MeshRenderData, parent=None):
        super().__init__(parent)
        self.mesh_data = mesh_data

        # Rotation and mouse controls
        self.rotation = [0.0, 0.0]
        self.last_mouse_pos = QPoint()
        self.rotation_locked = False

        # Rendering mode
        self.render_mode = RenderMode.SUNLIT

        # Auto-rotation
        self.auto_rotate = False
        self._rotation_timer = QTimer(self)
        self._rotation_timer.timeout.connect(self._rotate_step)
        self._rotation_timer.start(30)  # Update every 30 ms

        # Compute zoom based on mesh radius
        center = np.mean(mesh_data.vertices, axis=0)
        max_radius = np.linalg.norm(mesh_data.vertices - center, axis=1).max()
        self.mesh_center = center
        self.mesh_radius = max_radius

        # Overlay manager
        self.overlay_manager = OverlayManager()
        for overlay_cls in ALL_OVERLAYS:
            self.overlay_manager.register(overlay_cls())
        self.overlay_manager.update_data(mesh_data)
        self.zoom = -1  # Will be set in resizeGL based on window size

        log.info(f"Mesh center: {center}, max radius: {max_radius}")
        log.debug(f"Sample vertex: {mesh_data.vertices[0]}")

    def set_render_mode(self, mode: RenderMode):
        self.render_mode = mode
        self.update()

    def set_rotation_locked(self, locked: bool):
        """Enable or disable mouse-based rotation."""
        self.rotation_locked = locked

    def set_auto_rotate(self, enabled: bool):
        """Enable or disable automatic mesh rotation."""
        self.auto_rotate = enabled

    def _rotate_step(self):
        """Rotate slightly if auto-rotation is enabled."""
        if self.auto_rotate:
            self.rotation[0] += 0.3
            self.update()

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)

        # Lighting setup
        glEnable(GL_LIGHT0)
        glLightfv(GL_LIGHT0, GL_POSITION, [0.0, 0.0, 1.0, 0.0])  # Directional light from +Z
        glLightfv(GL_LIGHT0, GL_DIFFUSE, [1.0, 1.0, 1.0, 1.0])   # Soft white light

        glEnable(GL_LIGHT1)
        glLightfv(GL_LIGHT1, GL_POSITION, [1.0, 0.5, 1.0, 0.0])  # Simulated sun direction
        glLightfv(GL_LIGHT1, GL_DIFFUSE, [1.0, 1.0, 0.2, 1.0])   # Warm sunlight yellow
        glLightfv(GL_LIGHT1, GL_SPECULAR, [1.0, 1.0, 0.4, 1.0])

        glEnable(GL_COLOR_MATERIAL)
        glColorMaterial(GL_FRONT_AND_BACK, GL_AMBIENT_AND_DIFFUSE)

        log.info("OpenGL initialized.")

    def resizeGL(self, w, h):
        glViewport(0, 0, w, h)
        glMatrixMode(GL_PROJECTION)
        glLoadIdentity()
        aspect = w / h if h > 0 else 1.0
        gluPerspective(45.0, aspect, 0.1, 100000.0)
        glMatrixMode(GL_MODELVIEW)

        # Adjust zoom to fit entire mesh based on smaller window dimension
        view_angle_rad = math.radians(45.0 / 2)
        min_dimension = min(w, h)
        fov_scale = min_dimension / h  # scale factor based on vertical space
        optimal_distance = (self.mesh_radius / math.tan(view_angle_rad)) * fov_scale * 1.1
        self.zoom = -optimal_distance

        log.info(f"Viewport resized: ({w}x{h}), adjusted zoom: {self.zoom:.2f}")

    def paintGL(self):
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        glLoadIdentity()

        # Camera transform
        glTranslatef(0.0, 0.0, self.zoom)
        glRotatef(self.rotation[1], 1.0, 0.0, 0.0)
        glRotatef(self.rotation[0], 0.0, 1.0, 0.0)

        # Set rendering mode
        if self.render_mode == RenderMode.WIREFRAME:
            glDisable(GL_LIGHTING)
            glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)
        elif self.render_mode == RenderMode.FLAT_SHADED:
            glEnable(GL_LIGHTING)
            glDisable(GL_LIGHT1)
            glEnable(GL_LIGHT0)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)
        elif self.render_mode == RenderMode.SUNLIT:
            glEnable(GL_LIGHTING)
            glDisable(GL_LIGHT0)
            glEnable(GL_LIGHT1)
            glPolygonMode(GL_FRONT_AND_BACK, GL_FILL)

        # Draw mesh
        if self.mesh_data.vertices is not None and self.mesh_data.faces is not None:
            glBegin(GL_TRIANGLES)
            for face in self.mesh_data.faces:
                v0, v1, v2 = (self.mesh_data.vertices[idx] for idx in face)
                normal = np.cross(v1 - v0, v2 - v0)
                normal /= np.linalg.norm(normal)
                glNormal3f(*normal)

                # Clay-like face color
                glColor3f(0.7, 0.5, 0.4)
                for idx in face:
                    vertex = self.mesh_data.vertices[idx]
                    glVertex3f(*vertex)
            glEnd()

        # Overlay OpenGL render pass
        self.overlay_manager.render(self)

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.rotation_locked and not self.last_mouse_pos.isNull():
            delta = event.position().toPoint() - self.last_mouse_pos
            self.rotation[0] += delta.x()
            self.rotation[1] += delta.y()
            self.last_mouse_pos = event.position().toPoint()
            self.update()

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        self.overlay_manager.render_qpainter(painter, self)
        painter.end()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y() / 120  # One notch = 120
        zoom_step = self.mesh_radius * 0.05  # 5% of radius per scroll step
        self.zoom += -delta * zoom_step
        self.update()
