# ui/tools/mesh_viewer/overlays/face_normals_overlay.py

from .base import Overlay
from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from OpenGL.GL import *
from OpenGL.GL import (
    glGetDoublev, GL_MODELVIEW_MATRIX, GL_PROJECTION_MATRIX,
    glGetIntegerv, GL_VIEWPORT
)
from OpenGL.GLU import gluProject
import numpy as np


class FaceNormalsOverlay(Overlay):
    """
    Overlay that draws face normals as GL_LINES originating from the face centroids.
    Only draws normals for faces currently visible to the camera.
    """

    def __init__(self):
        self.enabled = True
        self.mesh_data: MeshRenderData | None = None

    def get_name(self):
        return "Face Normals"

    def get_category(self):
        return "Debug"

    def get_description(self):
        return "Displays outward-pointing normals from face centroids (camera-facing only)."

    def is_enabled(self):
        return self.enabled

    def set_enabled(self, value: bool):
        self.enabled = value

    def update_data(self, mesh_data):
        self.mesh_data = mesh_data

    def render(self, gl_widget):
        if not self.enabled or self.mesh_data is None:
            return

        vertices = self.mesh_data.vertices
        faces = self.mesh_data.faces
        if vertices is None or faces is None:
            return

        try:
            modelview = glGetDoublev(GL_MODELVIEW_MATRIX)
            projection = glGetDoublev(GL_PROJECTION_MATRIX)
            viewport = glGetIntegerv(GL_VIEWPORT).astype(np.int32)
        except Exception:
            return  # Skip rendering if OpenGL context isn't ready

        # Extract rotation portion of the modelview matrix (3x3 upper-left)
        rotation_matrix = np.array([
            [modelview[0][0], modelview[0][1], modelview[0][2]],
            [modelview[1][0], modelview[1][1], modelview[1][2]],
            [modelview[2][0], modelview[2][1], modelview[2][2]],
        ])

        # In camera space, view direction is always (0, 0, -1)
        camera_view_vector = np.array([0.0, 0.0, -1.0])

        scale = gl_widget.mesh_radius * 0.02  # length of normal lines

        glDisable(GL_LIGHTING)
        glColor3f(0.1, 1.0, 0.1)  # bright green
        glLineWidth(1.5)

        glBegin(GL_LINES)
        for face in faces:
            v0, v1, v2 = (vertices[idx] for idx in face)
            centroid = (v0 + v1 + v2) / 3

            # Project to screen to check visibility
            try:
                win_x, win_y, win_z = gluProject(
                    centroid[0], centroid[1], centroid[2],
                    modelview, projection, viewport
                )
            except Exception:
                continue

            if win_z < 0.0 or win_z > 1.0:
                continue

            # Compute face normal in world space and transform to camera space
            normal_world = np.cross(v1 - v0, v2 - v0)
            normal_world /= np.linalg.norm(normal_world)
            normal_camera = rotation_matrix.T @ normal_world

            if np.dot(normal_camera, camera_view_vector) < 0:
                endpoint = centroid + normal_world * scale
                glVertex3f(*centroid)
                glVertex3f(*endpoint)
        glEnd()

        glEnable(GL_LIGHTING)

    def render_qpainter(self, painter, gl_widget):
        pass  # not used
