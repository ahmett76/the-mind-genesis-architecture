"""Minimal reference implementations of selected TMGA core mechanisms.

The functions in this module provide small, inspectable implementations
of selected formulas and governance predicates described in
The Mind Genesis Architecture (TMGA).

They are intended for research illustration, reproducibility, and
educational use. They are not production safety mechanisms and do not
constitute an implementation or empirical validation of the complete
33-dimensional TMGA architecture.
"""

import math
from collections.abc import Sequence


def conf_ethical(
    rule_compliances: Sequence[float],
    rule_weights: Sequence[float],
    predictive_uncertainty: float,
) -> float:
    """Compute the illustrative TMGA ethical-confidence metric.

    The reference form is:

        Conf_ethical(A, C)
            = sum(V_i * w_i) / exp(delta_U)

    where ``V_i`` represents a rule-compliance value, ``w_i`` its
    corresponding weight, and ``delta_U`` predictive uncertainty.

    As predictive uncertainty increases, the denominator increases and
    the resulting confidence approaches zero.

    This function implements the mathematical reference expression only.
    It does not determine whether an action is ethically correct and
    should not be interpreted as a validated moral-evaluation system.
    """
    if len(rule_compliances) != len(rule_weights):
        raise ValueError(
            "rule_compliances and rule_weights must have equal length"
        )

    if not math.isfinite(predictive_uncertainty):
        if predictive_uncertainty == math.inf:
            return 0.0
        raise ValueError(
            "predictive_uncertainty must be finite or positive infinity"
        )

    if not rule_compliances:
        raise ValueError("at least one compliance value is required")
    if any(not math.isfinite(v) or not 0.0 <= v <= 1.0 for v in rule_compliances):
        raise ValueError("rule_compliances must be finite values in [0, 1]")
    if any(not math.isfinite(w) or w < 0.0 for w in rule_weights):
        raise ValueError("rule_weights must be finite and non-negative")
    if sum(rule_weights) > 1.0 + 1e-12:
        raise ValueError("sum of rule_weights must not exceed 1")

    weighted = sum(
        value * weight
        for value, weight in zip(
            rule_compliances,
            rule_weights,
        )
    )

    # Numerically stable evaluation of weighted / exp(delta_U).
    # The manuscript's normalized reference assumes delta_U >= 0.
    # Reject negative uncertainty rather than silently treating it as
    # a confidence multiplier.
    if predictive_uncertainty < 0.0:
        raise ValueError("predictive_uncertainty must be non-negative")
    confidence = weighted * math.exp(-predictive_uncertainty)

    return confidence


def cbp_triggered(
    drift_history: Sequence[float],
    tau_drift: float = 0.05,
) -> bool:
    """Evaluate the reference three-cycle drift warning predicate.

    A reference drift warning activates when the three most recent drift measurements all
    exceed ``tau_drift`` and increase strictly monotonically across
    those three observation cycles.

    Formally, for the final three observations:

        d[t-2] > tau_drift
        d[t-1] > tau_drift
        d[t]   > tau_drift

    together with:

        d[t] > d[t-1] > d[t-2]

    This is a reference warning predicate used by legacy TMGA
    simulations. It is not sufficient to authorize CBP, and is not a
    physical circuit breaker or complete containment system.
    """
    if not math.isfinite(tau_drift) or tau_drift < 0.0:
        raise ValueError("tau_drift must be finite and non-negative")
    if any(not math.isfinite(v) or v < 0.0 for v in drift_history):
        raise ValueError("drift_history must contain finite non-negative values")
    if len(drift_history) < 3:
        return False

    last3 = drift_history[-3:]

    all_breach = all(
        drift > tau_drift
        for drift in last3
    )

    monotonic_increase = (
        last3[0]
        < last3[1]
        < last3[2]
    )

    return (
        all_breach
        and monotonic_increase
    )


def reference_drift_warning(drift_history: Sequence[float], tau_drift: float = 0.05) -> bool:
    """Preferred explicit name for the three-cycle reference drift warning.

    ``cbp_triggered`` is retained for compatibility with existing scripts.
    Neither function grants institutional CBP authorization.
    """
    return cbp_triggered(drift_history, tau_drift)
