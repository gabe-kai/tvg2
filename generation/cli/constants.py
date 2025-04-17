# generation/cli/constants.py
"""
Parameter schemas for CLI argument validation and config merging.
Defines expected keys, types, and default values for each pipeline stage.
"""

CRATON_PARAMS = {
    "strategy": {
        "type": str,
        "default": "spaced_random",
    },
    "count": {
        "type": int,
        "default": None,  # Will be auto-computed if not specified
    },
    "spacing_factor": {
        "type": float,
        "default": 1.0,
    },
    # "min_distance" is not exposed via CLI yet, but can be added later if needed
}

# Example placeholder for future mesh configuration
MESH_PARAMS = {
    "strategy": {
        "type": str,
        "default": "icosphere",
    },
    # Add mesh-related parameter definitions here if needed
}
