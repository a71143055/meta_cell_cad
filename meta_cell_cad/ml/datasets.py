import yaml

def load_cell_library(path: str):
    with open(path, "r", encoding="utf-8") as f:
        return yaml.safe_load(f)

def apply_library_defaults(grid, lib):
    for cid, cell in grid.cells.items():
        ctype = cell.state.type
        defaults = lib.get(ctype, {})
        for k, v in defaults.get("params", {}).items():
            cell.state.params.setdefault(k, v)
