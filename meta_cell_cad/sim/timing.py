from typing import Dict, Tuple
import math

def estimate_delay(paths) -> float:
    """Very rough delay estimate proportional to path length."""
    total = sum(len(p) for p in paths)
    return math.log(1 + total)
