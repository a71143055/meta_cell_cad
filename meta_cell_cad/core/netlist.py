import networkx as nx
from typing import Dict
from .grid import Grid

class Netlist:
    def __init__(self):
        self.g = nx.DiGraph()

    def from_grid(self, grid: Grid) -> "Netlist":
        self.g.clear()
        for cid, cell in grid.cells.items():
            self.g.add_node(cid, type=cell.state.type, params=cell.state.params)
        for cid, cell in grid.cells.items():
            for nbr in cell.neighbors:
                self.g.add_edge(cid, nbr, signal="out")
        return self

    def stats(self) -> Dict[str, int]:
        return {"nodes": self.g.number_of_nodes(), "edges": self.g.number_of_edges()}
