from typing import Dict, Any

def coverage_objective(snapshot: Dict[Any, Any]) -> float:
    """Maximize proportion of 'logic' cells with healthy state."""
    healthy_logic = sum(1 for _, (t,h,_) in snapshot.items() if t=="logic" and h>0.7)
    total = len(snapshot)
    return healthy_logic / max(total, 1)

def diversity_objective(snapshot: Dict[Any, Any]) -> float:
    """Encourage type diversity akin to tissue heterogeneity."""
    types = [t for _, (t,_,_) in snapshot.items()]
    return len(set(types)) / max(len(types), 1)

def composite_reward(snapshot: Dict[Any, Any]) -> float:
    return 0.7 * coverage_objective(snapshot) + 0.3 * diversity_objective(snapshot)
