# Reference Simulation Scripts

This directory contains the reference simulation scripts described in Sections 8.5–8.9 of the paper.

## Scripts

| Script | Paper Section | Purpose |
|--------|---------------|---------|
| `nhcp_simulation.py` | Section 8.5, Table 9 | Base simulation (`NOMINAL`, `STRESS`, and `CBP` scenarios, 100 runs each) |
| `nhcp_simulation_advanced.py` | Section 8.6, Table 10 | Advanced & ablation simulation (`ADVERSARIAL`, `NOISY`, `MULTI-AGENT`, and ablation conditions) |
| `nhcp_simulation_comparative.py` | Sections 8.7–8.8, Tables 11–12 | Comparative evaluation and sensitivity analysis over `τ_drift` |
| `nhcp_simulation_extended.py` | Section 8.9, Table 13 | Extended simulation with seven critical governance components active simultaneously |

## Requirements

- Python 3.10 or higher
- NumPy (`numpy>=1.24`)

The simulation scripts use Python's standard library together with NumPy.

When the repository is installed with:

```bash
pip install -e .
```

the dependencies declared in `pyproject.toml` are installed automatically.

## Running

The scripts can be run directly from this directory:

```bash
python nhcp_simulation.py
python nhcp_simulation_advanced.py
python nhcp_simulation_comparative.py
python nhcp_simulation_extended.py
```

### Base Simulation

`nhcp_simulation.py` evaluates the `NOMINAL`, `STRESS`, and `CBP` scenarios described in Section 8.5 and reports the results to standard output.

### Advanced & Ablation Simulation

`nhcp_simulation_advanced.py` evaluates the `ADVERSARIAL`, `NOISY`, and `MULTI-AGENT` scenarios together with the ablation conditions described in Section 8.6.

The script prints the results to standard output and writes the corresponding numerical results to:

```text
advanced_simulation_results.json
```

in the repository root.

### Comparative & Sensitivity Simulation

`nhcp_simulation_comparative.py` compares the TMGA CBP activation predicate with the `single-breach` and `three-cycle average` baselines and performs the threshold sensitivity analysis described in Sections 8.7–8.8.

The corresponding numerical results are stored in:

```text
comparative_sensitivity_results.json
```

in the repository root.

### Extended Multi-Dimensional Simulation

`nhcp_simulation_extended.py` evaluates the core governance pathway with seven critical components active simultaneously:

- `AGI Guard`
- `ASI Guard`
- `ASI Verify`
- `AWI Void`
- `AWI Sentry`
- `CBP`
- `NHCP`

The corresponding numerical results are stored in:

```text
extended_simulation_results.json
```

in the repository root.

The remaining 26 dimensions of the proposed 33-dimensional taxonomy are not separately simulated or empirically validated by this experiment.

## Reproducibility and Scope

The scripts use fixed random seeds where stochastic scenarios are evaluated so that the numerical results reported in the manuscript can be reproduced under the specified reference conditions.

These scripts are reference simulations, not production implementations. Scenario parameters and thresholds are illustrative and have not been empirically calibrated for deployment.

The simulations evaluate the behavior of specified architectural predicates under synthetic conditions. Their results should therefore be interpreted as simulation-level behavioral observations rather than evidence of:

- real-world system security or robustness;
- empirical validation of the complete 33-dimensional architecture;
- formal verification of TMGA as a whole;
- physical implementation of hardware-level containment mechanisms; or
- guaranteed alignment, safety, or deployment readiness.

Hardware mechanisms discussed in the paper, including NMI-based interruption, escrow buffering, and actuator isolation, are architectural proposals and are not physically instantiated by these reference simulations.
