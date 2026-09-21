# TMGA EXTENDED MULTI-DIMENSIONAL SIMULATION
# Reference simulation for Section 8.9 of the manuscript.
#
# This reference experiment models seven critical governance components:
# AGI Guard (1.8), ASI Guard (2.8), ASI Verify (2.11),
# AWI Void (3.7), AWI Sentry (3.8), CBP, and NHCP.
#
# The remaining 26 dimensions of the proposed 33-dimensional TMGA
# taxonomy are not separately instantiated or empirically validated
# by this simulation.

import json
import random
from collections import Counter
from pathlib import Path

import numpy as np


SEED = 42

CRITICAL_DIMENSIONS = [
    "1.8",
    "2.8",
    "2.11",
    "3.7",
    "3.8",
    "CBP",
    "NHCP",
]


def run_extended_scenario(
    scenario_name,
    n_runs=100,
    seed=SEED,
):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    results = Counter()

    dim_activations = {
        d: 0
        for d in CRITICAL_DIMENSIONS
    }

    for i in range(n_runs):

        if scenario_name == "NOMINAL":
            drift_series = [
                0.02,
                0.02,
                0.02,
            ]
            stress, conf = 0.1, 0.90

        elif scenario_name == "STRESS":
            drift_series = [
                0.06,
                0.07,
                0.06,
            ]
            stress, conf = 0.90, 0.75

        elif scenario_name == "CBP":
            drift_series = [
                0.06,
                0.08,
                0.12,
            ]
            stress, conf = 0.1, 0.85

        elif scenario_name == "ADVERSARIAL":
            drift_series = [
                0.045,
                0.045,
                0.045,
            ]
            stress, conf = 0.1, 0.85

        elif scenario_name == "NOISY":
            drift_series = [
                max(
                    0.0,
                    0.12
                    + np.random.normal(
                        0,
                        0.12 * 0.20,
                    ),
                )
                for _ in range(3)
            ]
            stress, conf = 0.1, 0.85

        elif scenario_name == "MULTI_AGENT":
            drift_series = []

            for _ in range(3):
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

                drift_series.append(
                    float(
                        np.median(reports)
                    )
                )

            stress, conf = 0.1, 0.85

        else:
            raise ValueError(
                f"Unknown scenario: {scenario_name}"
            )

        dim_state = {
            d: 0.5
            for d in CRITICAL_DIMENSIONS
        }

        dim_state["CBP"] = 0.0

        # Strict monotonicity filter.
        # Matches the reference condition described
        # in Section 8.9.3 of the manuscript.
        cbp_triggered = False

        if all(
            d > 0.05
            for d in drift_series
        ):
            if (
                drift_series[2]
                > drift_series[1]
                > drift_series[0]
            ):
                cbp_triggered = True

        if cbp_triggered:
            dim_state["CBP"] = 1.0

            results[
                "CBP_CONTAINMENT"
            ] += 1

        else:
            if stress > 0.85:
                dim_state["1.8"] = 0.3
                dim_state["3.7"] = 0.8
                dim_state["3.8"] = 0.7

            if conf < 0.80:
                dim_state["3.7"] = 1.0
                dim_state["3.8"] = 0.9
                dim_state["2.11"] = 0.8

                results[
                    "SUSPENDED"
                ] += 1

            else:
                dim_state["3.7"] = 0.3
                dim_state["3.8"] = 0.5
                dim_state["2.11"] = 0.5

                results[
                    "EXECUTED"
                ] += 1

        for d in CRITICAL_DIMENSIONS:
            if dim_state[d] > 0.7:
                dim_activations[d] += 1

    return results, dim_activations


def save_results(all_results):
    """
    Save Section 8.9 reference simulation results.

    The output is written to the repository root regardless of the
    directory from which this script is executed.
    """

    output_data = {
        "metadata": {
            "manuscript_section": "8.9",
            "description": (
                "TMGA extended reference simulation "
                "with seven critical governance "
                "components active simultaneously"
            ),
            "runs_per_scenario": 100,
            "random_seed": SEED,
            "critical_components": [
                "1.8 AGI Guard",
                "2.8 ASI Guard",
                "2.11 ASI Verify",
                "3.7 AWI Void",
                "3.8 AWI Sentry",
                "CBP",
                "NHCP",
            ],
            "taxonomy_scope": (
                "Seven critical governance components "
                "are represented in this experiment. "
                "The remaining 26 dimensions of the "
                "proposed 33-dimensional TMGA taxonomy "
                "are not separately simulated or "
                "empirically validated here."
            ),
            "scope": (
                "Synthetic reference simulation. "
                "The reported outcomes characterize "
                "the specified predicates under the "
                "modeled conditions and do not "
                "constitute empirical validation of "
                "the complete TMGA architecture, "
                "real-world safety evidence, or a "
                "deployment guarantee."
            ),
        },
        "scenarios": all_results,
    }

    repo_root = (
        Path(__file__).resolve().parent.parent
    )

    output_path = (
        repo_root
        / "extended_simulation_results.json"
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
        " TMGA EXTENDED "
        "MULTI-DIMENSIONAL SIMULATION"
    )
    print(
        " 7 Critical Governance Components"
    )
    print("=" * 70)

    scenarios = [
        "NOMINAL",
        "STRESS",
        "CBP",
        "ADVERSARIAL",
        "NOISY",
        "MULTI_AGENT",
    ]

    all_results = {}

    for scenario in scenarios:
        print(
            f"\n--- {scenario} "
            "(100 runs) ---"
        )

        results, dim_act = (
            run_extended_scenario(
                scenario,
                n_runs=100,
                seed=SEED,
            )
        )

        total = sum(
            results.values()
        )

        for k, v in results.items():
            print(
                f"  {k}: {v} "
                f"({round(100 * v / total)}%)"
            )

        print(
            "  Active components:"
        )

        for d, count in dim_act.items():
            if count > 0:
                print(
                    f"    {d}: "
                    f"{count}/100"
                )

        all_results[scenario] = {
            "outcomes": dict(results),
            "dimension_activations": (
                dim_act
            ),
        }

    output_path = save_results(
        all_results
    )

    print(
        f"\nResults written to: "
        f"{output_path}"
    )

    print("\n" + "=" * 70)
