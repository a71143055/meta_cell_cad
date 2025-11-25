import math

def estimate_delay(paths) -> float:
    total = sum(len(p) for p in paths)
    return math.log(1 + total)
