from meta_cell_cad.core.grid import Grid
from meta_cell_cad.core.netlist import Netlist
from meta_cell_cad.layout.placer import place_grid
from meta_cell_cad.layout.router import manhattan_route

def test_place_and_route():
    nl = Netlist().from_grid(Grid(3,3))
    coords = place_grid(nl, 3, 3)
    routes = manhattan_route(nl, coords)
    assert isinstance(routes, list)
