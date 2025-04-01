# Project Layout

`docs/ProjectLayout.md`

## File & Folder Structure
```
├── docs
│   ├── DevelopmentNotes.md             # Development procedures and methods this project (should) follow
│   ├── PipelineDesign.md               # High-level overview of all major pipelines (generation, game, UI)
│   ├── ProjectLayout.md                # This file
│   └── Status.md                       # Current in-progress work and critical conventions (like how to use the logger)
├── game_logic                          # Simulation and runtime logic layer for civilizations and world events
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
│   │   ├── generate_political_map      # Nation borders, political control, and metadata
│   │   ├── populate_regions            # Naming and tagging of natural world regions
│   │   ├── seed_cratons                # Craton placement strategies and tectonic base
│   │   ├── simulate_climate            # Precipitation, temperature, wind and atmospheric data
│   │   ├── simulate_erosion            # Water and wind erosion applied to terrain
│   │   └── simulate_plate_motion       # Tectonic plate growth and movement simulation
│   └── generate_planet.py              # Planet generation pipeline orchestrator
├── logs                                # Run-time logs, debug traces, and structured output files
├── scripts
│   └── structure_dump.py               # The script to auto-update this file.
├── shared                              # Shared utilities, constants, and cross-layer interfaces
├── tests                               # Unit and integration tests across all project layers
└── ui                                  # UI application and rendering layer (initially PySide6 prototype)
```
