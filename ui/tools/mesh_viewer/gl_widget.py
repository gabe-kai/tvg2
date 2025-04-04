# ui/tools/mesh_viewer/gl_widget.py
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QMouseEvent, QWheelEvent
from PySide6.QtCore import Qt, QPoint

from OpenGL.raw.GLU import gluPerspective
from OpenGL.GL import *
import numpy as np
import math

from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from shared.logging.logger import get_logger

log = get_logger(__name__)


class PlanetGLWidget(QOpenGLWidget):
    """
    OpenGL rendering widget for displaying a planet mesh in wireframe.
    """

    def __init__(self, mesh_data: MeshRenderData, parent=None):
        super().__init__(parent)
        self.mesh_data = mesh_data

        # Rotation and mouse controls
        self.rotation = [0.0, 0.0]
        self.last_mouse_pos = QPoint()

        # Compute zoom based on mesh radius
        center = np.mean(mesh_data.vertices, axis=0)
        max_radius = np.linalg.norm(mesh_data.vertices - center, axis=1).max()
        self.mesh_center = center
        self.mesh_radius = max_radius
        self.zoom = -1  # Will be set in resizeGL based on window size

        log.info(f"Mesh center: {center}, max radius: {max_radius}")
        log.debug(f"Sample vertex: {mesh_data.vertices[0]}")

    def initializeGL(self):
        glEnable(GL_DEPTH_TEST)
        glEnable(GL_CULL_FACE)
        glPolygonMode(GL_FRONT_AND_BACK, GL_LINE)  # Wireframe mode
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

        # Draw mesh
        if self.mesh_data.vertices is not None and self.mesh_data.faces is not None:
            glBegin(GL_TRIANGLES)
            for face in self.mesh_data.faces:
                for idx in face:
                    vertex = self.mesh_data.vertices[idx]
                    glVertex3f(*vertex)
            glEnd()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.LeftButton:
            self.last_mouse_pos = event.position().toPoint()

    def mouseMoveEvent(self, event: QMouseEvent):
        if not self.last_mouse_pos.isNull():
            delta = event.position().toPoint() - self.last_mouse_pos
            self.rotation[0] += delta.x()
            self.rotation[1] += delta.y()
            self.last_mouse_pos = event.position().toPoint()
            self.update()

    def wheelEvent(self, event: QWheelEvent):
        delta = event.angleDelta().y() / 120  # One notch = 120
        zoom_step = self.mesh_radius * 0.05  # 5% of radius per scroll step
        self.zoom += -delta * zoom_step
        self.update()
