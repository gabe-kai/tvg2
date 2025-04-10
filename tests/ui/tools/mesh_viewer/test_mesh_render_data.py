# tests/ui/tools/mesh_viewer/test_mesh_render_data.py

import pytest
import numpy as np
from ui.tools.mesh_viewer.mesh_render_data import MeshRenderData


def test_valid_mesh_render_data():
    vertices = np.random.rand(100, 3)
    faces = np.random.randint(0, 100, size=(200, 3))
    elevation = np.random.rand(100)
    face_ids = np.random.randint(0, 10, size=(200,))

    data = MeshRenderData(
        vertices=vertices,
        faces=faces,
        elevation=elevation,
        face_ids=face_ids
    )

    assert data.vertices.shape == (100, 3)
    assert data.faces.shape == (200, 3)
    assert data.elevation.shape == (100,)
    assert data.face_ids.shape == (200,)


@pytest.mark.parametrize("vertices", [
    np.random.rand(100),                # 1D
    np.random.rand(100, 2),             # wrong shape
    np.random.rand(100, 4)              # wrong shape
])
def test_invalid_vertices(vertices):
    faces = np.random.randint(0, 100, size=(200, 3))
    with pytest.raises(AssertionError):
        MeshRenderData(vertices=vertices, faces=faces)


@pytest.mark.parametrize("faces", [
    np.random.randint(0, 100, size=(200,)),      # 1D
    np.random.randint(0, 100, size=(200, 2)),    # wrong shape
    np.random.randint(0, 100, size=(200, 4))     # wrong shape
])
def test_invalid_faces(faces):
    vertices = np.random.rand(100, 3)
    with pytest.raises(AssertionError):
        MeshRenderData(vertices=vertices, faces=faces)


def test_invalid_overlay_shapes():
    vertices = np.random.rand(100, 3)
    faces = np.random.randint(0, 100, size=(200, 3))

    with pytest.raises(AssertionError):
        MeshRenderData(vertices=vertices, faces=faces, elevation=np.random.rand(50))

    with pytest.raises(AssertionError):
        MeshRenderData(vertices=vertices, faces=faces, face_ids=np.random.randint(0, 10, size=(150,)))
