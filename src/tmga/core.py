"""Minimal reference implementations of TMGA core mechanisms.

These functions mirror the formulas described in the paper and are
intended for illustration and educational use, not for production
deployment.
"""
import math
from typing import List


def conf_ethical(rule_compliances: List[float],
                 rule_weights: List[float],
                 predictive_uncertainty: float) -> float:
    """Compute the ethical confidence metric from Section 4.2:

        Conf_ethical(A, C) = sum(V_i * w_i) / (1 + exp(delta_U))
    """
    if len(rule_compliances) != len(rule_weights):
        raise ValueError("rule_compliances and rule_weights must have equal length")
    weighted = sum(v * w for v, w in zip(rule_compliances, rule_weights))
    return weighted / (1.0 + math.exp(predictive_uncertainty))


def cbp_triggered(drift_history: List[float], tau_drift: float = 0.05) -> bool:
    """Return True iff the Circuit Breaker Protocol activation predicate holds.

    Formalized in Equation (1) of Section 11.1.1.
    """
    if len(drift_history) < 3:
        return False
    last3 = drift_history[-3:]
    all_breach = all(d > tau_drift for d in last3)
    positive_step = (last3[-1] - last3[-2]) > 0.0
    return all_breach and positive_step
