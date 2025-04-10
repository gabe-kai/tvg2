# tests/ui/tools/mesh_viewer/test_planet_loader.py

import pytest
import numpy as np
from pathlib import Path
import subprocess

from ui.tools.mesh_viewer.planet_loader import load_mesh_render_data
from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData

def test_load_real_planetbin(tmp_path):
    # Generate a small planet file using the CLI
    test_file = tmp_path / "test_output.planetbin"
    result = subprocess.run([
        "python", "-m", "generation.generate_planet",
        "--subdivision", "3",
        "--output", str(test_file)
    ], capture_output=True, text=True)

    assert result.returncode == 0, f"Planet generation failed: {result.stderr}"
    assert test_file.exists(), f"Generated file not found: {test_file}"

    mesh_data = load_mesh_render_data(test_file)

    assert isinstance(mesh_data, MeshRenderData)
    assert isinstance(mesh_data.vertices, np.ndarray)
    assert isinstance(mesh_data.faces, np.ndarray)

    # Basic shape checks
    assert mesh_data.vertices.ndim == 2
    assert mesh_data.vertices.shape[1] == 3
    assert mesh_data.faces.ndim == 2
    assert mesh_data.faces.shape[1] == 3

    # Optional: check known values at subdivision=3
    assert mesh_data.vertices.shape[0] == 642
    assert mesh_data.faces.shape[0] == 1280

    # Clean up is automatic with pytest tmp_path
