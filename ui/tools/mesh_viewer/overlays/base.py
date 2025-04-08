# ui/tools/mesh_viewer/overlays/base.py

from abc import ABC, abstractmethod
from PySide6.QtOpenGLWidgets import QOpenGLWidget
from PySide6.QtGui import QMouseEvent, QPainter
from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData


class Overlay(ABC):
    """
    Base class for all overlays used in the mesh viewer.
    Each overlay can render visual elements and respond to mouse events.
    """

    def __init__(self):
        self._enabled = True

    def set_enabled(self, enabled: bool) -> None:
        """Enable or disable this overlay."""
        self._enabled = enabled

    def is_enabled(self) -> bool:
        """Return True if this overlay is currently enabled."""
        return self._enabled

    @abstractmethod
    def get_name(self) -> str:
        """Return the human-readable name of the overlay."""
        pass

    @abstractmethod
    def render(self, gl_widget: QOpenGLWidget) -> None:
        """
        Perform OpenGL rendering for the overlay.
        This will be called from the GLWidget's paintGL().
        """
        pass

    def render_qpainter(self, painter: QPainter, gl_widget: QOpenGLWidget) -> None:
        """
        Optional: render 2D elements using QPainter after OpenGL pass.
        Called from GLWidget's paintEvent().
        Default does nothing.
        """
        pass

    def handle_mouse(self, event: QMouseEvent) -> None:
        """
        Handle mouse input specific to this overlay.
        Override in subclasses as needed.
        """
        pass

    def update_data(self, mesh_data: MeshRenderData) -> None:
        """
        Called when new mesh data is loaded.
        Overlays can extract or preprocess what they need.
        """
        pass

    def get_category(self) -> str:
        """
        Return the category of this overlay for grouping in UI.
        Subclasses should override this.
        """
        return "Misc"

    def get_description(self) -> str:
        """
        Return a short description of the overlay.
        Used for tooltips and overlay selection UI.
        """
        return "No description provided."
