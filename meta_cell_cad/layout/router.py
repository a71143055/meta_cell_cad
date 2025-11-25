from typing import Dict, Tuple, List
from ..core.netlist import Netlist

def manhattan_route(nl: Netlist, coords: Dict[Tuple[int,int], Tuple[int,int]]) -> List[List[Tuple[int,int]]]:
    """Generate naive Manhattan paths for each edge."""
    paths = []
    for u, v in nl.g.edges:
        x1, y1 = coords[u]
        x2, y2 = coords[v]
        path = []
        x = x1
        y = y1
        while x != x2:
            x += 1 if x < x2 else -1
            path.append((x, y))
        while y != y2:
            y += 1 if y < y2 else -1
            path.append((x, y))
        paths.append(path)
    return paths
