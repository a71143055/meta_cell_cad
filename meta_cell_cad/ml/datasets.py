import yaml
from typing import Dict, Any

def load_cell_library(path: str) -> Dict[str, Any]:
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def apply_library_defaults(grid, lib: Dict[str, Any]) -> None:
    for cid, cell in grid.cells.items():
        ctype = cell.state.type
        defaults = lib.get(ctype, {})
        # Merge simple defaults (thresholds etc.)
        for k, v in defaults.get("params", {}).items():
            cell.state.params.setdefault(k, v)
