# Meta-Cell CAD

세포형(meta-learning) 반도체칩/집적회로 설계를 위한 최소 기능 CAD:
- 셀 추상화
- 메타러닝 규칙 학습
- Netlist 생성 → Verilog/SPICE 내보내기
- 배치/배선 및 시뮬레이션

## 실행
```bash
pip install -e .
python -m meta_cell_cad.ui.cli synth \
  --design meta_cell_cad/examples/example_design.json \
  --out build/
