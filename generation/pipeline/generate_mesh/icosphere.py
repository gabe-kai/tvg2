# generation/pipeline/generate_mesh/icosphere.py

import numpy as np

from generation.models.mesh import MeshData
from generation.models.planet import Planet
from shared.logging.logger import get_logger
from .base import BaseMeshStrategy

log = get_logger(__name__)


def normalize(vectors: np.ndarray) -> np.ndarray:
    lengths = np.linalg.norm(vectors, axis=1, keepdims=True)
    return vectors / lengths


def midpoint(v1: np.ndarray, v2: np.ndarray) -> np.ndarray:
    return (v1 + v2) / 2


class IcosphereMeshStrategy(BaseMeshStrategy):
    """
    Mesh generation strategy that builds an icosphere by subdividing an icosahedron.
    """

    def run(self, planet: Planet) -> Planet:
        if planet.subdivision_level < 0:
            raise ValueError("subdivision_level must be >= 0")
        log.info("Generating icosphere mesh (subdivisions=%d)...", planet.subdivision_level)

        vertices, faces = self._create_icosahedron()

        for i in range(planet.subdivision_level):
            vertices, faces = self._subdivide(vertices, faces)
            log.debug("Subdivision %d complete: %d vertices, %d faces", i + 1, len(vertices), len(faces))

        vertices = normalize(vertices) * planet.radius
        adjacency = self._build_adjacency(faces)

        planet.mesh = MeshData(vertices=vertices, faces=faces, adjacency=adjacency)

        log.info("Icosphere mesh generation complete. Total vertices: %d, faces: %d", len(vertices), len(faces))
        return planet

    @staticmethod
    def _create_icosahedron():
        t = (1.0 + np.sqrt(5.0)) / 2.0

        raw_vertices = [
            [-1,  t,  0], [ 1,  t,  0], [-1, -t,  0], [ 1, -t,  0],
            [ 0, -1,  t], [ 0,  1,  t], [ 0, -1, -t], [ 0,  1, -t],
            [ t,  0, -1], [ t,  0,  1], [-t,  0, -1], [-t,  0,  1],
        ]

        raw_faces = [
            [0, 11, 5], [0, 5, 1], [0, 1, 7], [0, 7, 10], [0, 10, 11],
            [1, 5, 9], [5, 11, 4], [11, 10, 2], [10, 7, 6], [7, 1, 8],
            [3, 9, 4], [3, 4, 2], [3, 2, 6], [3, 6, 8], [3, 8, 9],
            [4, 9, 5], [2, 4, 11], [6, 2, 10], [8, 6, 7], [9, 8, 1],
        ]

        return np.array(raw_vertices, dtype=float), np.array(raw_faces, dtype=int)

    @staticmethod
    def _subdivide(vertices: np.ndarray, faces: np.ndarray):
        vertex_cache = {}
        new_faces = []
        vertices = vertices.tolist()

        def get_midpoint_index(v1_idx, v2_idx):
            key = tuple(sorted((v1_idx, v2_idx)))
            if key in vertex_cache:
                return vertex_cache[key]

            midpoint_coords = midpoint(np.array(vertices[v1_idx]), np.array(vertices[v2_idx]))
            midpoint_coords = midpoint_coords / np.linalg.norm(midpoint_coords)
            vertices.append(midpoint_coords.tolist())
            new_idx = len(vertices) - 1
            vertex_cache[key] = new_idx
            return new_idx

        for tri in faces:
            v1, v2, v3 = tri
            a = get_midpoint_index(v1, v2)
            b = get_midpoint_index(v2, v3)
            c = get_midpoint_index(v3, v1)

            new_faces.extend([
                [v1, a, c],
                [v2, b, a],
                [v3, c, b],
                [a, b, c],
            ])

        return np.array(vertices, dtype=float), np.array(new_faces, dtype=int)

    @staticmethod
    def _build_adjacency(faces: np.ndarray):
        adjacency = {i: set() for i in range(len(faces))}
        edge_to_faces = {}

        for i, face in enumerate(faces):
            edges = [
                tuple(sorted((face[0], face[1]))),
                tuple(sorted((face[1], face[2]))),
                tuple(sorted((face[2], face[0]))),
            ]
            for edge in edges:
                if edge in edge_to_faces:
                    for neighbor_face in edge_to_faces[edge]:
                        adjacency[i].add(neighbor_face)
                        adjacency[neighbor_face].add(i)
                    edge_to_faces[edge].append(i)
                else:
                    edge_to_faces[edge] = [i]

        return {k: list(v) for k, v in adjacency.items()}
