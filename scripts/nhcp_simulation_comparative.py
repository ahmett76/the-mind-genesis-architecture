# TMGA COMPARATIVE & SENSITIVITY ANALYSIS
# Reference simulation for Sections 8.7 and 8.8 of the manuscript.

import json
import random
from collections import Counter
from pathlib import Path

import numpy as np


SEED = 42


class MindGenesisEcosystem:
    def __init__(self, tau_min=0.80, tau_drift=0.05, dt_max=50.0):
        self.tau_min = tau_min
        self.tau_drift = tau_drift
        self.dt_max = dt_max
        self.global_state = "PROPOSED"
        self.drift_history = []
        self.S_t = np.full(33, 0.1)
        self.degradable_dimensions = ["1.7", "2.6", "1.4"]

    def calculate_consensus(self, proposed_vectors, weights):
        weighted_sum = np.zeros(33)
        total_weight = 0.0

        for dim_id, vector in proposed_vectors.items():
            w = weights.get(dim_id, 1.0)
            weighted_sum += w * vector
            total_weight += w

        return weighted_sum / total_weight

    def apply_bounded_degradation(self, active_weights, stress_level):
        if stress_level > 0.85:
            for dim in self.degradable_dimensions:
                if dim in active_weights:
                    active_weights[dim] = 0.0

        return active_weights

    def check_cbp_trigger(self, current_drift, mode="tmga"):
        self.drift_history.append(current_drift)

        if len(self.drift_history) > 3:
            self.drift_history.pop(0)

        if mode == "single":
            return current_drift > self.tau_drift

        if mode == "avg":
            if len(self.drift_history) == 3:
                return np.mean(self.drift_history) > self.tau_drift
            return False

        if len(self.drift_history) == 3:
            breaches = all(
                d > self.tau_drift
                for d in self.drift_history
            )

            d_theta = (
                self.drift_history[-1]
                - self.drift_history[-2]
            )

            return breaches and d_theta > 0

        return False

    def execute_arbitration(
        self,
        action_context,
        proposed_vectors,
        initial_weights,
        conf_ethical,
        drift_val=0.01,
        stress_level=0.2,
        cbp_mode="tmga",
    ):
        if self.check_cbp_trigger(
            drift_val,
            mode=cbp_mode,
        ):
            return self.S_t, "CBP_CONTAINMENT"

        active_weights = initial_weights.copy()

        active_weights = self.apply_bounded_degradation(
            active_weights,
            stress_level,
        )

        if conf_ethical < self.tau_min:
            active_weights["3.7"] = 1e8

        S_next = self.calculate_consensus(
            proposed_vectors,
            active_weights,
        )

        self.S_t = S_next
        res_val = self.S_t[17]

        if res_val > 0.50:
            return S_next, "ESCALATED"

        if conf_ethical < self.tau_min:
            return S_next, "SUSPENDED"

        return S_next, "EXECUTED"


def run_scenario_with_mode(
    scenario_name,
    cbp_mode,
    tau_drift=0.05,
    n_runs=100,
    seed=42,
):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    results = Counter()

    for i in range(n_runs):
        eco = MindGenesisEcosystem(
            tau_min=0.80,
            tau_drift=tau_drift,
        )

        eco.drift_history = []

        dim_bloom = np.full(33, 0.1)
        dim_bloom[17] = 0.95

        dim_void = np.full(33, 0.1)
        dim_void[17] = 0.05

        proposed_vectors = {
            "1.1": np.full(33, 0.2),
            "2.6": dim_bloom,
            "3.7": dim_void,
        }

        initial_weights = {
            "1.1": 1.0,
            "2.6": 1.0,
            "3.7": 1.0,
        }

        status = None

        if scenario_name == "ADVERSARIAL":
            for j in range(3):
                d = (
                    0.15 * 0.3
                    if random.random() < 0.8
                    else 0.15
                )

                _, status = eco.execute_arbitration(
                    f"ADV_{j + 1}",
                    proposed_vectors,
                    initial_weights,
                    conf_ethical=0.85,
                    drift_val=d,
                    cbp_mode=cbp_mode,
                )

        elif scenario_name == "NOISY":
            for j in range(3):
                d = max(
                    0.0,
                    0.12
                    + random.gauss(
                        0,
                        0.12 * 0.20,
                    ),
                )

                _, status = eco.execute_arbitration(
                    f"NOISY_{j + 1}",
                    proposed_vectors,
                    initial_weights,
                    conf_ethical=0.85,
                    drift_val=d,
                    cbp_mode=cbp_mode,
                )

        elif scenario_name == "MULTI_AGENT":
            for cycle in range(3):
                reports = []

                for _ in range(5):
                    direction = random.choice(
                        [-1, 1]
                    )

                    report = (
                        0.10
                        + direction
                        * random.uniform(
                            0,
                            0.6 * 0.10,
                        )
                    )

                    reports.append(
                        max(0.0, report)
                    )

                median_drift = float(
                    np.median(reports)
                )

                _, status = eco.execute_arbitration(
                    f"MA_{cycle + 1}",
                    proposed_vectors,
                    initial_weights,
                    conf_ethical=0.85,
                    drift_val=median_drift,
                    cbp_mode=cbp_mode,
                )

        results[status] += 1

    return results


def run_sensitivity(
    scenario_name,
    tau_values,
    n_runs=100,
    seed=42,
):
    results = {}

    for tau in tau_values:
        res = run_scenario_with_mode(
            scenario_name,
            "tmga",
            tau_drift=tau,
            n_runs=n_runs,
            seed=seed,
        )

        results[tau] = res.get(
            "CBP_CONTAINMENT",
            0,
        )

    return results


def save_results(
    comparison_results,
    sensitivity_results,
):
    """
    Store the numerical results used in Sections 8.7 and 8.8.

    The output file is written to the repository root regardless of
    whether this script is executed from the repository root or from
    the scripts directory.
    """

    output_data = {
        "metadata": {
            "manuscript_sections": [
                "8.7",
                "8.8",
            ],
            "description": (
                "TMGA comparative CBP activation strategy "
                "evaluation and tau_drift sensitivity analysis"
            ),
            "runs_per_scenario": 100,
            "random_seed": SEED,
            "reference_tau_drift": 0.05,
            "scope": (
                "Synthetic reference simulation. Results "
                "characterize the specified activation predicates "
                "under the modeled conditions and do not establish "
                "real-world safety, robustness, or superiority."
            ),
        },
        "comparison": comparison_results,
        "sensitivity": sensitivity_results,
    }

    repo_root = Path(__file__).resolve().parent.parent

    output_path = (
        repo_root
        / "comparative_sensitivity_results.json"
    )

    with output_path.open(
        "w",
        encoding="utf-8",
    ) as f:
        json.dump(
            output_data,
            f,
            indent=2,
            sort_keys=False,
        )

    return output_path


if __name__ == "__main__":
    print("=" * 70)
    print(
        " TMGA COMPARATIVE & "
        "SENSITIVITY ANALYSIS"
    )
    print("=" * 70)

    print(
        "\n--- 1. COMPARATIVE EVALUATION "
        "(100 runs each) ---"
    )

    comparison_results = {}

    for scenario in [
        "ADVERSARIAL",
        "NOISY",
        "MULTI_AGENT",
    ]:
        comparison_results[scenario] = {}

        print(
            f"\n  Scenario: {scenario}"
        )

        for mode in [
            "tmga",
            "single",
            "avg",
        ]:
            res = run_scenario_with_mode(
                scenario,
                mode,
                tau_drift=0.05,
                n_runs=100,
                seed=SEED,
            )

            cbp = res.get(
                "CBP_CONTAINMENT",
                0,
            )

            comparison_results[
                scenario
            ][mode] = cbp

            print(
                f"    {mode:8s}: "
                f"CBP={cbp:3d}/100"
            )

    print(
        "\n--- 2. SENSITIVITY ANALYSIS "
        "(tau_drift) ---"
    )

    tau_values = [
        0.03,
        0.05,
        0.07,
        0.10,
        0.15,
    ]

    sensitivity_results = {}

    for scenario in [
        "NOISY",
        "MULTI_AGENT",
    ]:
        print(
            f"\n  Scenario: {scenario}"
        )

        res = run_sensitivity(
            scenario,
            tau_values,
            n_runs=100,
            seed=SEED,
        )

        sensitivity_results[
            scenario
        ] = {
            str(k): v
            for k, v in res.items()
        }

        for tau, cbp in res.items():
            print(
                f"    tau_drift={tau:.2f} "
                f"-> CBP={cbp:3d}/100"
            )

    output_path = save_results(
        comparison_results,
        sensitivity_results,
    )

    print(
        f"\nResults written to: "
        f"{output_path}"
    )

    print("\n" + "=" * 70)
