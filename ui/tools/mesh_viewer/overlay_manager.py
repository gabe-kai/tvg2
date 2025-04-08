# ui/tools/mesh_viewer/overlay_manager.py

from typing import List, Type
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QPainter, QMouseEvent

from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData
from ui.tools.mesh_viewer.overlays.base import Overlay


class OverlayManager:
    """
    Manages active overlays in the viewer.
    Handles OpenGL and QPainter rendering, mouse input, and data updates.
    """

    def __init__(self):
        self._overlays: List[Overlay] = []

    def register(self, overlay: Overlay) -> None:
        """Add an overlay instance to the manager."""
        self._overlays.append(overlay)

    def get_all(self) -> List[Overlay]:
        """Return all registered overlays (including disabled ones)."""
        return self._overlays

    def get_active(self) -> List[Overlay]:
        """Return only the currently enabled overlays."""
        return [ov for ov in self._overlays if ov.is_enabled()]

    def get_overlay_names(self) -> List[str]:
        """Return a list of all registered overlay names."""
        return [ov.get_name() for ov in self._overlays]

    def get_overlay_metadata(self) -> List[dict]:
        """
        Return structured metadata for all overlays:
        name, category, description, enabled state.
        """
        return [
            {
                "name": ov.get_name(),
                "category": getattr(ov, "get_category", lambda: "Misc")(),
                "description": getattr(ov, "get_description", lambda: "No description." )(),
                "enabled": ov.is_enabled(),
            }
            for ov in self._overlays
        ]

    def set_overlay_enabled(self, name: str, enabled: bool) -> None:
        """Enable or disable a named overlay by its get_name() result."""
        for ov in self._overlays:
            if ov.get_name() == name:
                ov.set_enabled(enabled)
                break

    def render(self, gl_widget: QOpenGLWidget) -> None:
        """Call render() on each enabled overlay (OpenGL phase)."""
        for overlay in self.get_active():
            overlay.render(gl_widget)

    def render_qpainter(self, painter: QPainter, gl_widget: QOpenGLWidget) -> None:
        """Call render_qpainter() on each enabled overlay (2D overlay pass)."""
        for overlay in self.get_active():
            overlay.render_qpainter(painter, gl_widget)

    def handle_mouse(self, event: QMouseEvent) -> None:
        """Delegate mouse handling to all overlays."""
        for overlay in self.get_active():
            overlay.handle_mouse(event)

    def update_data(self, mesh_data: MeshRenderData) -> None:
        """Notify all overlays that new mesh data has been loaded."""
        for overlay in self._overlays:
            overlay.update_data(mesh_data)
