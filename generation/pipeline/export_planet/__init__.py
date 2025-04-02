# generation/pipeline/export_planet/__init__.py

from generation.pipeline.export_planet.hdf5_export import HDF5ExportStrategy


def get_strategy(name: str, **kwargs):
    name = name.lower()
    if name == "hdf5":
        return HDF5ExportStrategy(**kwargs)
    raise ValueError(f"Unknown export strategy: {name}")