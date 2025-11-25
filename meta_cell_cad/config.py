from dataclasses import dataclass

@dataclass
class SynthesisConfig:
    grid_width: int = 16
    grid_height: int = 16
    max_iters: int = 100
    seed: int = 42

@dataclass
class ExportConfig:
    top_module_name: str = "top"
    spice_supply_v: float = 1.0
