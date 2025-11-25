from typing import Dict, Tuple
from ..core.netlist import Netlist

def place_grid(nl: Netlist, width: int, height: int) -> Dict[Tuple[int,int], Tuple[int,int]]:
    """Map logical cells to physical coordinates (identity for now)."""
    coords = {}
    for cid in nl.g.nodes:
        x, y = cid
        x = max(0, min(width-1, x))
        y = max(0, min(height-1, y))
        coords[cid] = (x, y)
    return coords
