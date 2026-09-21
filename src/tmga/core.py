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
            = sum(V_i * w_i) / (1 + exp(delta_U))

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

    weighted = sum(
        value * weight
        for value, weight in zip(
            rule_compliances,
            rule_weights,
        )
    )

    # Numerically stable evaluation of:
    #
    #     weighted / (1 + exp(predictive_uncertainty))
    #
    # For large positive uncertainty, evaluating exp(x) directly may
    # overflow. The equivalent expression below keeps the expected
    # limiting behavior: Conf_ethical -> 0 as uncertainty -> +infinity.
    if predictive_uncertainty >= 0.0:
        exp_neg = math.exp(-predictive_uncertainty)
        confidence = (
            weighted
            * exp_neg
            / (1.0 + exp_neg)
        )
    else:
        exp_pos = math.exp(predictive_uncertainty)
        confidence = (
            weighted
            / (1.0 + exp_pos)
        )

    return confidence


def cbp_triggered(
    drift_history: Sequence[float],
    tau_drift: float = 0.05,
) -> bool:
    """Evaluate the reference Circuit Breaker Protocol predicate.

    CBP activates when the three most recent drift measurements all
    exceed ``tau_drift`` and the most recent drift step is positive.

    Formally, for the final three observations:

        d[t-2] > tau_drift
        d[t-1] > tau_drift
        d[t]   > tau_drift

    together with:

        d[t] - d[t-1] > 0

    This is a reference governance predicate used by the TMGA
    simulations. It is not a physical circuit breaker, hardware
    interrupt, deployment guarantee, or complete containment system.
    """
    if len(drift_history) < 3:
        return False

    last3 = drift_history[-3:]

    all_breach = all(
        drift > tau_drift
        for drift in last3
    )

    positive_step = (
        last3[-1]
        - last3[-2]
    ) > 0.0

    return (
        all_breach
        and positive_step
    )
