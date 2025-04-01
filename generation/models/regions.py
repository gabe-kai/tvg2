# generation/models/regions.py
from dataclasses import dataclass
from typing import Dict, Any

@dataclass
class RegionMap:
    named_regions: Dict[str, Any]    # name -> metadata (location, type, faces)
