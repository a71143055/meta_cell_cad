import argparse
import json
import os
from ..config import SynthesisConfig, ExportConfig
from ..logging_utils import get_logger
from ..core.grid import Grid
from ..core.netlist import Netlist
from ..ml.meta_learner import MetaLearner
from ..ml.datasets import load_cell_library, apply_library_defaults
from ..hdl.verilog_exporter import export_verilog
from ..hdl.spice_exporter import export_spice
from ..layout.placer import place_grid
from ..layout.router import manhattan_route
from ..sim.simulator import simulate
from ..sim.timing import estimate_delay

log = get_logger("cli")

def synthesize(design_path: str, out_dir: str):
    os.makedirs(out_dir, exist_ok=True)
    with open(design_path, "r", encoding="utf-8") as f:
        design = json.load(f)

    cfg = SynthesisConfig(**design.get("synthesis", {}))
    exp_cfg = ExportConfig(**design.get("export", {}))
    lib_path = design.get("cell_library", "")

    grid = Grid(cfg.grid_width, cfg.grid_height)
    if lib_path:
        lib = load_cell_library(lib_path)
        apply_library_defaults(grid, lib)
        log.info("Applied cell library defaults")

    ml = MetaLearner(seed=cfg.seed)
    rewards, meta = ml.train(episodes=design.get("episodes", 3),
                             grid_factory=lambda: Grid(cfg.grid_width, cfg.grid_height))
    log.info(f"Meta rewards: {rewards}; meta: {meta}")

    nl = Netlist().from_grid(grid)
    log.info(f"Netlist stats: {nl.stats()}")

    v_content = export_verilog(nl, exp_cfg.top_module_name)
    s_content = export_spice(nl, exp_cfg.spice_supply_v)
    with open(os.path.join(out_dir, "top.v"), "w", encoding="utf-8") as vf:
        vf.write(v_content)
    with open(os.path.join(out_dir, "top.spice"), "w", encoding="utf-8") as sf:
        sf.write(s_content)
    log.info("Exported Verilog and SPICE")

    coords = place_grid(nl, cfg.grid_width, cfg.grid_height)
    routes = manhattan_route(nl, coords)
    delay = estimate_delay(routes)
    with open(os.path.join(out_dir, "layout.json"), "w", encoding="utf-8") as lf:
        json.dump({"coords": {str(k): v for k,v in coords.items()},
                   "routes": routes,
                   "delay_estimate": delay}, lf, indent=2)
    log.info(f"Layout done, delay~{delay:.3f}")

    healths = simulate(grid, steps=design.get("sim_steps", 50))
    with open(os.path.join(out_dir, "sim.json"), "w", encoding="utf-8") as sf:
        json.dump({"health": healths}, sf, indent=2)
    log.info("Simulation complete")

def main():
    parser = argparse.ArgumentParser(description="Meta-Cell CAD")
    sub = parser.add_subparsers(dest="cmd")

    p_synth = sub.add_parser("synth", help="Synthesize design")
    p_synth.add_argument("--design", required=True, help="Design JSON path")
    p_synth.add_argument("--out", required=True, help="Output directory")

    args = parser.parse_args()
    if args.cmd == "synth":
        synthesize(args.design, args.out)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
