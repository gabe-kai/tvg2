# ui/tools/mesh_viewer/overlays/craton_overlay.py

from .base import Overlay
from OpenGL.GL import *

class CratonOverlay(Overlay):
    """
    Overlay that highlights the seed (center) face of each craton in the mesh.

    This overlay uses OpenGL immediate mode to render each craton seed face
    as a filled triangle in reddish-orange. It currently only activates in
    'flat' and 'sunlit' rendering modes.

    Additionally, it defines a render_faces() method intended for future support
    of face-level highlight rendering, which returns a face-index → color mapping.
    """
    name = "Cratons"

    def get_name(self):
        """Unique name used for overlay toggle and identification."""
        return "Cratons"

    def get_category(self):
        """Grouping category shown in the overlay menu."""
        return "Tectonics"

    def get_description(self):
        """Short tooltip-style description of the overlay's purpose."""
        return "Highlights craton center faces (seed positions)"

    def render(self, gl_widget):
        """
        Render each craton seed face as a filled triangle using OpenGL.
        Only runs if overlay is enabled and in a visible rendering mode.
        """
        if not self.is_enabled():
            return

        data = gl_widget.mesh_data
        if not self.is_visible(data, gl_widget.render_mode.name.lower()):
            return

        vertices = data.vertices
        faces = data.faces
        if vertices is None or faces is None:
            return

        glDisable(GL_LIGHTING)
        glColor4f(1.0, 0.2, 0.1, 1.0)  # Set triangle color to reddish-orange
        glBegin(GL_TRIANGLES)

        for craton in data.planet.cratons:
            face_id = craton.center_index
            if face_id < 0 or face_id >= len(faces):
                continue
            v0, v1, v2 = (vertices[idx] for idx in faces[face_id])  # Get triangle vertices for the craton center face
            glVertex3f(*v0)
            glVertex3f(*v1)
            glVertex3f(*v2)

        glEnd()
        glEnable(GL_LIGHTING)

    def is_visible(self, data, render_mode):
        """
        Determine whether this overlay should render in the given mode.
        Requires craton data and a non-wireframe render mode.
        """
        return (
            hasattr(data, "planet") and hasattr(data.planet, "cratons")
            and data.planet.cratons
            and render_mode in ("flat", "sunlit")  # skip wireframe
        )

    def render_faces(self, data, mesh, render_mode):
        """
        Return a mapping of face index → color for potential future face highlight support.
        Currently unused by the viewer, but retained for extensibility.
        """
        highlight = {}  # face index → (r, g, b, a)

        for craton in data.planet.cratons:
            face_id = craton.center_index
            highlight[face_id] = (1.0, 0.2, 0.1, 1.0)  # reddish-orange

        return highlight
