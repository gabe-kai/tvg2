# tests/generation/pipeline/export_planet/test_export_strategy.py

import numpy as np
import pytest
import h5py
from pathlib import Path

from generation.models.planet import Planet
from generation.models.mesh import MeshData
from generation.pipeline.export_planet import get_strategy


def create_mock_planet() -> Planet:
    vertices = np.array([
        [0, 0, 1], [0, 1, 0], [1, 0, 0],
        [0, 0, -1], [0, -1, 0], [-1, 0, 0]
    ], dtype=np.float32)
    faces = np.array([
        [0, 1, 2], [3, 4, 5]
    ], dtype=np.int32)
    adjacency = {
        0: [1],
        1: [0]
    }
    mesh = MeshData(vertices=vertices, faces=faces, adjacency=adjacency)

    return Planet(radius=1000, subdivision_level=1, seed=999, mesh=mesh)


def test_export_strategy_writes_hdf5(tmp_path):
    planet = create_mock_planet()
    output_path = tmp_path / "exported.planetbin"

    exporter = get_strategy("hdf5", output_path=str(output_path))
    result = exporter.run(planet)

    assert isinstance(result, Planet)
    assert output_path.exists(), "Export file should exist after run()"

    with h5py.File(output_path, "r") as f:
        assert f.attrs["radius"] == planet.radius
        assert f.attrs["subdivision_level"] == planet.subdivision_level
        assert f.attrs["seed"] == planet.seed
        assert "mesh/vertices" in f
        assert "mesh/faces" in f
