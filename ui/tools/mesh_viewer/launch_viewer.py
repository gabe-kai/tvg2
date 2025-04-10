# ui/tools/mesh_viewer/launch_viewer.py

import argparse
import sys

from PySide6.QtWidgets import QApplication

from ui.tools.mesh_viewer.viewer_app import PlanetViewerApp
from ui.tools.mesh_viewer.planet_loader import load_mesh_render_data
from shared.logging.logger import get_logger

log = get_logger(__name__)


def main():
    parser = argparse.ArgumentParser(description="Planet Mesh Viewer")
    parser.add_argument(
        "--load", type=str, required=True,
        help="Path to the .planetbin file to view"
    )

    args = parser.parse_args()

    mesh_data = load_mesh_render_data(args.load)

    app = QApplication(sys.argv)
    viewer = PlanetViewerApp(mesh_data)
    viewer.show()

    log.info("Starting application event loop...")
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
