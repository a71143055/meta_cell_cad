# Meta-Cell CAD

세포형(meta-learning) 반도체칩/집적회로 설계를 위한 최소 기능 CAD:
- 셀 추상화(분화, 이웃 상호작용, 규칙 기반 전이)
- 메타러닝으로 셀 규칙/파라미터 학습(간단한 MAML-풍 인터페이스)
- Netlist 생성 → Verilog/SPICE 내보내기
- 배치/배선(Layout) 및 간단 시뮬레이션

## 빠른 시작
```bash
pip install -e .
python -m meta_cell_cad.ui.cli synth \
  --design meta_cell_cad/examples/example_design.json \
  --out build/
