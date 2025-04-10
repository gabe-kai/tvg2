# Project Layout

`docs/ProjectLayout.md`

## File & Folder Structure
```
├── config/
│   └── earthlike_default.json      # CLI/JSON config preset for generating an Earth-like planet
│   
├── docs/
│   ├── step_plans/
│   │   └── IcosphereViewerSession2.md
│   │   
│   ├── DevelopmentNotes.md                 # Development procedures and methods this project (should) follow
│   ├── PipelineDesign.md                   # High-level overview of all major pipelines (generation, game, UI)
│   ├── ProjectLayout.md                    # This file
│   └── Status.md                           # Current in-progress work and critical conventions (like how to use the logger)
│   
├── game_logic/                 # Simulation and runtime logic layer for civilizations and world events
│   └── docs/
│       └── GamePipeline.md     # Detailed design document for the game logic pipeline
│       
├── generation/                         # Planet generation layer and all associated data and algorithms
│   ├── docs/
│   │   ├── Design_SeedCratons.md       # Detailed design document for the craton seeding pipeline
│   │   └── PlanetPipeline.md           # Detailed design document for the planet generation pipeline
│   │   
│   ├── models/
│   │   ├── biomes.py                   # BiomeMap
│   │   ├── climate.py                  # Temperature, Precipitation
│   │   ├── elevation.py                # Elevation, Drainage
│   │   ├── mesh.py                     # MeshData (vertices, faces, adjacency)
│   │   ├── planet.py                   # Main Planet container class
│   │   ├── politics.py                 # Nations, PoliticalMap
│   │   ├── regions.py                  # Region names and boundaries
│   │   └── tectonics.py                # Craton, Plate, PlateMap
│   │   
│   ├── pipeline/                       # Stage-by-stage modular planet generation components
│   │   ├── export_planet/              # Export the final Planet object to .planetbin format
│   │   │   ├── __init__.py             # Strategy selector for planet export (e.g. get_strategy("hdf5"))
│   │   │   ├── base.py                 # BaseExportPlanetStrategy ABC for export stage structure
│   │   │   └── hdf5_export.py          # HDF5ExportStrategy that writes a Planet to .planetbin format
│   │   │   
│   │   ├── generate_biomes/
│   │   ├── generate_elevation/
│   │   ├── generate_mesh/              # Icosphere/hex sphere mesh construction
│   │   │   ├── __init__.py             # get_strategy(name: str) dispatcher
│   │   │   ├── base.py                 # BaseMeshStrategy Abstract Interface
│   │   │   └── icosphere.py            # IcosphereMeshStrategy
│   │   │   
│   │   ├── generate_political_map/
│   │   ├── populate_regions/
│   │   ├── seed_cratons/
│   │   │   ├── __init__.py             # Strategy loader
│   │   │   ├── base.py                 # Abstract base class: SeedCratonsStrategy
│   │   │   └── spaced_random.py        # Random placement with minimum distance enforcement
│   │   │   
│   │   ├── simulate_climate/
│   │   ├── simulate_erosion/
│   │   └── simulate_plate_motion/
│   └── generate_planet.py              # CLI entry point: generate, load, and export Planet data
│   
├── logs/
│   └── vassal.log
│   
├── scripts/
│   └── structure_dump.py       # (OLD) The script to auto-update this file.
│   
├── shared/                             # Shared utilities, constants, and cross-layer interfaces
│   ├── config/
│   │   └── planet_gen_config.py        # Dataclass schema for PlanetGenConfig used by CLI and config files
│   │   
│   ├── logging/
│   │   ├── __init__.py
│   │   ├── log_config.py               # Main interface: get_logger()
│   │   └── logger.py                   # Log formatting, handlers, levels
│   │   
│   └── project_layout_manager/         # Core engine for scanning, storing, and exporting the project’s structure
│       ├── config/                     # User-defined settings controlling output paths and formatting behavior
│       │   ├── __init__.py
│       │   └── layout_config.py        # Loads and validates layout/export settings
│       │   
│       ├── exporters/                  # Output logic for saving project structure in various formats
│       │   ├── __init__.py
│       │   ├── ascii_exporter.py       # Writes the ASCII tree structure to a .md file
│       │   └── flat_exporter.py        # Writes a flat file list (one path per line)
│       │   
│       ├── importer/                   # Parsers for reading existing layout files (like .md)
│       │   ├── __init__.py
│       │   └── ascii_parser.py         # Reads PROJECT_LAYOUT_TREE.md and extracts comments
│       │   
│       ├── models/                     # Shared data models for layout nodes and comment management
│       │   ├── __init__.py
│       │   ├── comment_manager.py      # Handles merging and syncing of comment data across formats
│       │   └── node.py                 # Defines the Node class representing a file or folder
│       │   
│       ├── scanner/                    # Tools for walking the project directory
│       │   ├── __init__.py
│       │   └── file_scanner.py         # Scans filesystem and updates/removes nodes accordingly
│       │   
│       ├── storage/                    # Handles persistent layout data storage
│       │   ├── __init__.py
│       │   └── json_storage.py         # Reads/writes project_state.json which stores the internal node tree
│       │   
│       ├── layout_manager.py           # Orchestrates scanning, parsing, merging, and exporting
│       ├── PROJECT_LAYOUT_FLAT.txt     # Flat export file (generated)
│       ├── PROJECT_LAYOUT_TREE.md      # ASCII tree export file with editable comments
│       ├── project_state.json          # Internal representation of the current project layout (updated automatically)
│       └── purge_removed.py            # CLI utility to permanently delete removed nodes from project_state.json
│       
├── tests/                                      # Unit and integration tests across all project layers
│   ├── generation/                             # Planet generation tests
│   │   ├── models/
│   │   │   └── test_planet_io.py               # Tests for Planet.save() and Planet.load() HDF5 serialization
│   │   │   
│   │   └── pipeline/
│   │       ├── export_planet/
│   │       │   └── test_export_strategy.py     # Tests that HDF5ExportStrategy correctly writes .planetbin files
│   │       │   
│   │       ├── generate_mesh/
│   │       │   └── test_icosphere.py           # Unit tests for IcosphereMeshStrategy and Planet mesh validity
│   │       │   
│   │       └── seed_cratons/
│   │           └── test_spaced_random.py
│   │           
│   ├── logging/                                # Logging config and logger interface tests
│   │   ├── __init__.py
│   │   ├── test_log_config.py                  # Tests for config setup, TRACE level, hooks
│   │   └── test_logger_interface.py            # Tests for get_logger and basic use
│   │   
│   ├── ui/
│   │   └── tools/
│   │       └── mesh_viewer/
│   │           ├── test_mesh_render_data.py    # Unit tests for MeshRenderData validation and shape constraints
│   │           └── test_planet_loader.py       # Tests the planet_loader with CLI-generated .planetbin files
│   │           
│   └── __init__.py
│   
├── ui/
│   ├── docs/
│   │   └── UIPipeline.md                       # Detailed design document for the user interface pipeline
│   │   
│   └── tools/
│       └── mesh_viewer/
│           ├── overlays/
│           │   ├── __init__.py                 # Overlay auto-registration (ALL_OVERLAYS)
│           │   ├── base.py                     # Overlay base class defining required interface
│           │   ├── craton_overlay.py           # (WIP) Future overlay for showing craton size and placement
│           │   ├── elevation_overlay.py        # (WIP) Future overlay for showing elevation shading
│           │   ├── face_index_overlay.py       # Displays numeric face IDs at centroids (via QPainter)
│           │   ├── face_normals_overlay.py     # Draws face normals for visible geometry (via OpenGL)
│           │   └── region_overlay.py           # (WIP) Future overlay for highlighting political regions
│           │   
│           ├── gl_widget.py                    # Contains PlanetGLWidget (QOpenGLWidget)
│           ├── launch_viewer.py                # CLI entrypoint for the standalone viewer
│           ├── mesh_render_data.py             # MeshRenderData class (DTO for rendering)
│           ├── overlay_manager.py
│           ├── planet_loader.py                # Load .planetbin → MeshRenderData
│           └── viewer_app.py                   # Contains PlanetViewerApp (QMainWindow)
│           
├── pytest.ini      # Test output file generated by the planet creation pipeline
└── testplanet.planetbin
```
