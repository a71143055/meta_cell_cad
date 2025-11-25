from typing import Dict, Tuple, List
from .cell import Cell, CellState

class Grid:
    def __init__(self, width: int, height: int):
        self.width = width
        self.height = height
        self.cells: Dict[Tuple[int, int], Cell] = {}
        self._init_neighbors()

    def _init_neighbors(self):
        for y in range(self.height):
            for x in range(self.width):
                cid = (x, y)
                if cid not in self.cells:
                    self.cells[cid] = Cell(id=cid, state=CellState(
                        type="logic", params={"diff_thresh":0.6}, signals={"clk":0, "in":0, "out":0}
                    ))
        for (x, y), cell in self.cells.items():
            nbrs = []
            for dx, dy in [(1,0),(-1,0),(0,1),(0,-1)]:
                nx, ny = x+dx, y+dy
                if 0 <= nx < self.width and 0 <= ny < self.height:
                    nbrs.append((nx, ny))
            cell.neighbors = nbrs

    def step(self):
        neighbor_map: Dict[Tuple[int,int], List[CellState]] = {}
        for cid, cell in self.cells.items():
            neighbor_map[cid] = [self.cells[n].state for n in cell.neighbors]
        for cid, cell in self.cells.items():
            cell.step(neighbor_map[cid])
            cell.differentiate()

    def snapshot(self):
        return {cid: (cell.state.type, cell.state.health, dict(cell.state.signals))
                for cid, cell in self.cells.items()}
