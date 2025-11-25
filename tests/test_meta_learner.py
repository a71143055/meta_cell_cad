from meta_cell_cad.ml.meta_learner import MetaLearner
from meta_cell_cad.core.grid import Grid

def test_meta_train_runs():
    ml = MetaLearner(seed=7)
    rewards, meta = ml.train(episodes=2, grid_factory=lambda: Grid(4,4))
    assert len(rewards) == 2
