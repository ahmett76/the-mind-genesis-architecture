# Reference Simulation Scripts

This directory contains the reference simulation scripts described in Sections 8.5–8.9 of the paper.

## Scripts

| Script | Paper Section | Purpose |
|--------|---------------|---------|
| `nhcp_simulation.py` | Section 8.5, Table 9 | Base simulation (NOMINAL, STRESS, CBP scenarios, 100 runs each) |
| `nhcp_simulation_advanced.py` | Section 8.6, Table 10 | Advanced & ablation simulation (ADVERSARIAL, NOISY, MULTI-AGENT + ablations) |
| `nhcp_simulation_comparative.py` | Sections 8.7–8.8, Tables 11–12 | Comparative evaluation & sensitivity analysis over `τ_drift` |
| `nhcp_simulation_extended.py` | Section 8.9, Table 13 | Extended 7-dimension multi-dimensional simulation |

## Requirements

- Python 3.9 or higher (Python 3.12 recommended)
- Standard library only (`math`, `time`, `json`, `unittest`)
- No third-party dependencies

## Running

Each script can be run directly:

```bash
python nhcp_simulation.py
python nhcp_simulation_advanced.py
python nhcp_simulation_comparative.py
python nhcp_simulation_extended.py
