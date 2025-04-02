# generation/pipeline/export_planet/hdf5_export.py

from generation.models.planet import Planet
from shared.logging.logger import get_logger

log = get_logger(__name__)


class HDF5ExportStrategy:
    def __init__(self, output_path: str):
        self.output_path = output_path

    def run(self, planet: Planet) -> Planet:
        log.info("Exporting planet to: %s", self.output_path)
        planet.save(self.output_path)
        log.info("Export complete.")
        return planet
