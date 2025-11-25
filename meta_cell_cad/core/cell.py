from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class CellState:
    type: str
    params: Dict[str, float]
    signals: Dict[str, int]
    health: float = 1.0
    age: int = 0

@dataclass
class Cell:
    id: Tuple[int, int]
    state: CellState
    neighbors: List[Tuple[int, int]] = field(default_factory=list)

    def step(self, neighbor_states: List[CellState]) -> None:
        if neighbor_states:
            avg_h = sum(ns.health for ns in neighbor_states) / len(neighbor_states)
            self.state.health = 0.9 * self.state.health + 0.1 * avg_h
        self.state.age += 1
        clk_votes = [ns.signals.get("clk", 0) for ns in neighbor_states]
        if clk_votes:
            self.state.signals["clk"] = 1 if sum(clk_votes) >= (len(clk_votes) / 2) else 0

    def differentiate(self) -> None:
        th = self.state.params.get("diff_thresh", 0.5)
        if self.state.health > th and self.state.type == "logic":
            self.state.type = "mem"
        elif self.state.health < (th * 0.5):
            self.state.type = "io"
