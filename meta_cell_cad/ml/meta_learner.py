import random
from dataclasses import dataclass
from ..core.grid import Grid
from .objectives import composite_reward

@dataclass
class MetaParams:
    diff_thresh_mean: float = 0.6
    diff_thresh_std: float = 0.1
    clk_bias: float = 0.5

class MetaLearner:
    def __init__(self, seed: int = 42):
        random.seed(seed)
        self.meta = MetaParams()

    def sample_task(self):
        return {
            "diff_thresh": random.gauss(self.meta.diff_thresh_mean, self.meta.diff_thresh_std),
            "clk_bias": self.meta.clk_bias + random.uniform(-0.1, 0.1),
        }

    def inner_loop(self, grid: Grid, iters: int = 30) -> float:
        task = self.sample_task()
        for cell in grid.cells.values():
            cell.state.params["diff_thresh"] = max(0.1, min(0.9, task["diff_thresh"]))
            cell.state.signals["clk"] = 1 if random.random() < task["clk_bias"] else 0
        for _ in range(iters):
            grid.step()
        snapshot = grid.snapshot()
        return composite_reward(snapshot)

    def outer_update(self, rewards):
        avg = sum(rewards) / max(len(rewards), 1)
        if avg < 0.5:
            self.meta.diff_thresh_mean -= 0.01
        else:
            self.meta.diff_thresh_mean += 0.005
        self.meta.diff_thresh_mean = max(0.2, min(0.8, self.meta.diff_thresh_mean))

    def train(self, episodes: int, grid_factory):
        rewards = []
        for _ in range(episodes):
            grid = grid_factory()
            r = self.inner_loop(grid)
            rewards.append(r)
            self.outer_update([r])
        return rewards, self.meta
