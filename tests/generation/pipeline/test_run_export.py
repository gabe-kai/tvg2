# tests/generation/pipeline/test_run_export.py
"""
Unit test for the planet export pipeline stage.
"""

import tempfile
from pathlib import Path

from generation.pipeline.run_mesh import run_mesh
from generation.pipeline.run_export import run_export
from shared.config.planet_gen_config import PlanetGenConfig
from generation.models.planet import Planet


def test_run_export_writes_file():
    config = PlanetGenConfig(radius=5000, subdivision_level=2, seed=123)
    planet = Planet(radius=config.radius, subdivision_level=config.subdivision_level, seed=config.seed)
    planet = run_mesh(planet, config, cli_args={})

    with tempfile.TemporaryDirectory() as tmpdir:
        output_path = Path(tmpdir) / "testplanet.planetbin"
        run_export(planet, str(output_path))

        assert output_path.exists()
        assert output_path.stat().st_size > 0

        # Optional: re-load and verify summary
        loaded = Planet.load(str(output_path))
        assert isinstance(loaded, Planet)
        assert loaded.mesh is not None
        assert hasattr(loaded.mesh, "faces")
