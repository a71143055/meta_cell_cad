from ..core.netlist import Netlist

def export_verilog(nl: Netlist, top_module: str = "top") -> str:
    lines = [f"module {top_module}();"]
    for cid in nl.g.nodes:
        lines.append(f"  // cell {cid}")
        lines.append(f"  wire cell_{cid[0]}_{cid[1]}_out;")
    for u, v, d in nl.g.edges(data=True):
        lines.append(f"  // {u} -> {v} ({d.get('signal','out')})")
        lines.append(f"  assign cell_{v[0]}_{v[1]}_out = cell_{u[0]}_{u[1]}_out;")
    lines.append("endmodule")
    return "\n".join(lines)
