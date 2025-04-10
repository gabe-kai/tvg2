# ui/tools/mesh_viewer/overlays/craton_overlay.py

from .base import Overlay

class CratonOverlay(Overlay):
    name = "Cratons"

    def get_name(self):
        return "Cratons"

    def get_category(self):
        return "Tectonics"

    def get_description(self):
        return "Highlights craton center faces (seed positions)"

    def render(self, gl_widget):
        # This overlay only renders in OpenGL via render_faces()
        pass

    def is_visible(self, data, render_mode):
        return (
            hasattr(data, "planet") and hasattr(data.planet, "cratons")
            and data.planet.cratons
            and render_mode in ("flat", "sunlit")  # skip wireframe
        )

    def render_faces(self, data, mesh, render_mode):
        highlight = {}  # face index → (r, g, b, a)

        for craton in data.planet.cratons:
            face_id = craton.center_index
            highlight[face_id] = (1.0, 0.2, 0.1, 1.0)  # reddish-orange

        return highlight
