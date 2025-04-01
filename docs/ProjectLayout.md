# Project Layout

`docs/ProjectLayout.md`

## File & Folder Structure
```
├── config
│   └── earthlike_default.json          # CLI/JSON config preset for generating an Earth-like planet
├── docs
│   ├── DevelopmentNotes.md             # Development procedures and methods this project (should) follow
│   ├── PipelineDesign.md               # High-level overview of all major pipelines (generation, game, UI)
│   ├── ProjectLayout.md                # This file
│   └── Status.md                       # Current in-progress work and critical conventions (like how to use the logger)
├── game_logic                          # Simulation and runtime logic layer for civilizations and world events
│   └── docs
│       └── GamePipeline.md             # Detailed design document for the game logic pipeline
├── generation                          # Planet generation layer and all associated data and algorithms
│   ├── docs
│   │   └── PlanetPipeline.md           # Detailed design document for the planet generation pipeline
│   ├── models
│   │   ├── biomes.py                   # BiomeMap
│   │   ├── climate.py                  # Temperature, Precipitation
│   │   ├── elevation.py                # Elevation, Drainage
│   │   ├── mesh.py                     # MeshData (vertices, faces, adjacency)
│   │   ├── planet.py                   # Main Planet container class
│   │   ├── politics.py                 # Nations, PoliticalMap
│   │   ├── regions.py                  # Region names and boundaries
│   │   └── tectonics.py                # Craton, Plate, PlateMap
│   ├── pipeline                        # Stage-by-stage modular planet generation components
│   │   ├── export_planet               # Export the final Planet object to .planetbin format
│   │   ├── generate_biomes             # Assign biomes based on climate and elevation
│   │   ├── generate_elevation          # Elevation generation using tectonics and orogeny
│   │   ├── generate_mesh               # Icosphere/hex sphere mesh construction
│   │   │   ├── __init__.py             # get_strategy(name: str) dispatcher
│   │   │   ├── base.py                 # BaseMeshStrategy Abstract Interface
│   │   │   └── icosphere.py            # IcosphereMeshStrategy
│   │   ├── generate_political_map      # Nation borders, political control, and metadata
│   │   ├── populate_regions            # Naming and tagging of natural world regions
│   │   ├── seed_cratons                # Craton placement strategies and tectonic base
│   │   ├── simulate_climate            # Precipitation, temperature, wind and atmospheric data
│   │   ├── simulate_erosion            # Water and wind erosion applied to terrain
│   │   └── simulate_plate_motion       # Tectonic plate growth and movement simulation
│   └── generate_planet.py              # CLI entry point to launch the planet generation pipeline
├── logs                                # Run-time logs, debug traces, and structured output files
├── scripts
│   └── structure_dump.py               # The script to auto-update this file.
├── shared                              # Shared utilities, constants, and cross-layer interfaces
│   ├── config
│   │   └── planet_gen_config.py        # Dataclass schema for PlanetGenConfig used by CLI and config files
│   └── logging
│       ├── __init__.py
│       ├── logger.py                   # Main interface: get_logger()
│       └── log_config.py               # Log formatting, handlers, levels
├── tests                               # Unit and integration tests across all project layers
│   ├── generation
│   │   └── pipeline
│   │       └── generate_mesh
│   │           └── test_icosphere.py   # Unit tests for IcosphereMeshStrategy and Planet mesh validity
│   └── logging
│       ├── test_logger_interface.py    # Tests for get_logger and basic use
│       └── tet_log_config.py           # Tests for config setup, TRACE level, hooks
└── ui                                  # UI application and rendering layer (initially PySide6 prototype)
    └── docs
        └── UIPipeline.md               # Detailed design document for the user interface pipeline
```
