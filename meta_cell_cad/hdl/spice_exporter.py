from ..core.netlist import Netlist

def export_spice(nl: Netlist, vdd: float = 1.0) -> str:
    lines = [f"* SPICE netlist (vdd={vdd}V)"]
    lines.append(".include std_cells.lib")
    # Nodes and connections
    for cid in nl.g.nodes:
        lines.append(f"* cell {cid}")
        lines.append(f"V{cid[0]}_{cid[1]} VDD 0 {vdd}")
    for u, v, d in nl.g.edges(data=True):
        lines.append(f"* {u} -> {v} ({d.get('signal','out')})")
        lines.append(f"X{u[0]}_{u[1]}_{v[0]}_{v[1]} VDD 0 cell_link")
    lines.append(".end")
    return "\n".join(lines)
