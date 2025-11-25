from dataclasses import dataclass, field
from typing import Dict, List, Tuple

@dataclass
class CellState:
    type: str                   # e.g., "logic", "mem", "io"
    params: Dict[str, float]    # learned params, thresholds
    signals: Dict[str, int]     # input/output logical signals
    health: float = 1.0         # cell viability (0..1)
    age: int = 0                # steps lived

@dataclass
class Cell:
    id: Tuple[int, int]         # (x, y)
    state: CellState
    neighbors: List[Tuple[int, int]] = field(default_factory=list)

    def step(self, neighbor_states: List[CellState]) -> None:
        """Update cell based on neighbors: emulate cellular interaction."""
        # Simple rule: average neighbor health affects this cell's health
        if neighbor_states:
            avg_h = sum(ns.health for ns in neighbor_states) / len(neighbor_states)
            self.state.health = 0.9 * self.state.health + 0.1 * avg_h
        # Age increments
        self.state.age += 1
        # Example signal update: majority vote on 'clk' from neighbors
        clk_votes = [ns.signals.get("clk", 0) for ns in neighbor_states]
        if clk_votes:
            self.state.signals["clk"] = 1 if sum(clk_votes) >= (len(clk_votes) / 2) else 0

    def differentiate(self) -> None:
        """Allow cell to change type when health or signals reach thresholds."""
        th = self.state.params.get("diff_thresh", 0.5)
        if self.state.health > th and self.state.type == "logic":
            self.state.type = "mem"  # simplistic differentiation
        elif self.state.health < (th * 0.5):
            self.state.type = "io"
