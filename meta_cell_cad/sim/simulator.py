from typing import Dict, Tuple
from ..core.grid import Grid

def simulate(grid: Grid, steps: int = 50) -> Dict[Tuple[int,int], float]:
    for _ in range(steps):
        grid.step()
    snap = grid.snapshot()
    return {cid: h for cid, (_, h, _) in snap.items()}
