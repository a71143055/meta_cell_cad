from ..core.grid import Grid

def simulate(grid: Grid, steps: int = 50):
    for _ in range(steps):
        grid.step()
    snap = grid.snapshot()
    return {str(cid): h for cid, (_, h, _) in snap.items()}
