from meta_cell_cad.core.grid import Grid
from meta_cell_cad.core.netlist import Netlist
from meta_cell_cad.hdl.verilog_exporter import export_verilog
from meta_cell_cad.hdl.spice_exporter import export_spice

def test_verilog_export():
    nl = Netlist().from_grid(Grid(2,2))
    v = export_verilog(nl, "top")
    assert "module top" in v
    assert "endmodule" in v

def test_spice_export():
    nl = Netlist().from_grid(Grid(2,2))
    s = export_spice(nl, 1.0)
    assert "* SPICE netlist" in s
    assert ".end" in s
