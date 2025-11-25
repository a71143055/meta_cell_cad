from meta_cell_cad.core.grid import Grid

def test_grid_init():
    g = Grid(4,4)
    assert len(g.cells) == 16
    snap = g.snapshot()
    assert all(t in ("logic","mem","io") for t,_,_ in snap.values())

def test_step_changes_health():
    g = Grid(3,3)
    h0 = [c.state.health for c in g.cells.values()]
    g.step()
    h1 = [c.state.health for c in g.cells.values()]
    assert h0 != h1

