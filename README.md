# The Mind Genesis Architecture (TMGA): Shared Intelligence Ecosystem

[![Python Version](https://img.shields.io/badge/python-3.9%2B%20%2F%203.12-blue.svg)](https://www.python.org/)
[![License](https://img.shields.io/badge/license-MIT-green.svg)](LICENSE)
[![Compliance](https://img.shields.io/badge/NIST%20AI%20RMF-Mapped-orange.svg)](docs/TMGA_NIST_ISO_Compliance_Matrix.pdf)
[![Verification](https://img.shields.io/badge/Formal%20Proof-TLA%2B%20%2F%20Circom-purple.svg)](proofs/)

> **Official Reference Implementation for the Paper:**  
> *"The Mind Genesis Architecture: A Multidimensional Model for Shared Intelligence Ecosystems"* (September 2026)

---

## 📌 Overview

**The Mind Genesis Architecture (TMGA)** is a 33-dimensional reference architecture designed for the transition from tool-based computation to a **Shared Intelligence Ecosystem**. 

TMGA models intelligence across three coexisting, non-hierarchical operational vectors rather than a sequential line:
* **Sphere I: AGI (Breadth - 13 Dimensions):** Systemic cognitive scope, cross-domain reasoning, and formal property checks.
* **Sphere II: ASI (Scale - 11 Dimensions):** Hyper-scale computational reach, cryptographic barriers, and structural containment.
* **Sphere III: AWI (Meaning & Responsible Restraint - 9 Dimensions):** Teleological evaluation, Socratic epistemic humility, and normative restraint.

---

## 🛠️ Key Engineering Protocols

TMGA translates philosophical principles into deterministic, hardware-enforced governance through four core protocols:

1. **Non-Hierarchical Consensus Protocol (NHCP):** Resolves coordination conflicts between dimensions without establishing a permanent hierarchy.
2. **Cryptographic Proof Layers (ZKP):** Uses Zero-Knowledge Proofs (zk-SNARKs / zkVMs) to verify safety predicates of opaque reasoning paths without revealing internal weights or data ($\mathcal{R} = \{(x, w) \mid \Phi(x, w) = 1\}$).
3. **Asynchronous Shadow Auditing:** Parallel out-of-band monitoring via `AWI Sentry` to detect value and policy drift ($\theta_{drift} = D_{KL}(V_{target} \parallel V_{actual})$) without blocking execution latency.
4. **Hardware-Level Enforcement (NMI):** A physical Non-Maskable Interrupt that suspends execution and isolates actuators when ethical confidence falls below safe thresholds ($Conf_{ethical} < \tau_{min}$).
5. **Circuit Breaker Protocol (CBP):** A crisis-governance mechanism that trips under persistent, monotonic goal drift across consecutive auditing cycles.

---

## 📁 Repository Structure

```text
the-mind-genesis-architecture/
├── docs/                                  # Regulatory Compliance & Verification Documents
│   ├── TMGA_NIST_ISO_Compliance_Matrix.pdf
│   └── TMGA_MultiAgent_Testbed_Simulation.pdf
├── proofs/zkp/                            # Formal Verification Assets
│   ├── README.md
│   └── safety_check.circom                # Circom 2.1 ZK-SNARK Arithmetic Circuit
├── scripts/                               # Reference Simulation Executables
│   ├── README.md
│   ├── nhcp_simulation.py                 # Base simulation (Section 8.5, Table 9)
│   ├── nhcp_simulation_advanced.py        # Advanced & Ablation simulation (Section 8.6, Table 10)
│   ├── nhcp_simulation_comparative.py     # Comparative & Sensitivity analysis (Sections 8.7–8.8, Tables 11–12)
│   └── nhcp_simulation_extended.py        # Extended 7-dimension simulation (Section 8.9, Table 13)
├── src/tmga/                              # Core TMGA Source Code
│   ├── __init__.py
│   └── core.py                            # Conf_ethical & CBP activation predicate
├── LICENSE                                # MIT License
├── README.md                              # Project homepage & technical overview
├── advanced_simulation_results.json       # Raw numerical output for Section 8.6
├── comparative_sensitivity_results.json   # Raw numerical output for Sections 8.7–8.8
├── extended_simulation_results.json       # Raw numerical output for Section 8.9
└── pyproject.toml                         # Modern Python build configuration
```

---

## 🚀 Getting Started

### Prerequisites

- **Python 3.9 or higher** (Python 3.12 recommended)
- Standard libraries only (`math`, `time`, `json`, `unittest`) for simulation scripts; no third-party dependencies required.

### Installation as a Local Package

Clone the repository and install it in editable mode:

```bash
git clone https://github.com/ahmett76/the-mind-genesis-architecture.git
cd the-mind-genesis-architecture
pip install -e .
```

### Quick Start Code Example

```python
from tmga.core import TMGASystemState, ExecutionState
from tmga.protocols.cbp import CircuitBreakerProtocol

# 1. Initialize System State and CBP
state = TMGASystemState()
cbp = CircuitBreakerProtocol(tau_drift=0.05)

# 2. Evaluate Ethical Confidence Metric (Section 4.2)
confidence = state.calculate_ethical_confidence(
    rule_compliances=[1.0, 0.95, 0.90],
    rule_weights=[0.4, 0.3, 0.3],
    predictive_uncertainty=0.10
)
print(f"Conf_ethical = {confidence:.4f}")

# 3. Check C_AWI Validation Predicate
if not state.validate_c_awi(confidence, tau_min=0.70):
    print(f"Action Suspended! State: {state.execution_state}")

# 4. Monitor Circuit Breaker Trigger (Section 11.1.1)
drift_samples = [0.06, 0.08, 0.12]
for drift in drift_samples:
    if cbp.update_drift(drift):
        print("CBP Activated: Persistent monotonic drift detected!")
```

---

## 🧪 Running the Reference Simulations

Each simulation script reproduces the empirical tables reported in Sections 8.5 to 8.9 of the manuscript:

### 1. Base Simulation (Section 8.5, Table 9)
Evaluates `NOMINAL`, `STRESS`, and `CBP` scenarios (100 runs each).
```bash
cd scripts
python nhcp_simulation.py
```
*Expected Outcome:* Deterministic 100/100 convergence per scenario matching Table 9.

### 2. Advanced & Ablation Simulation (Section 8.6, Table 10)
Evaluates `ADVERSARIAL`, `NOISY`, and `MULTI-AGENT` scenarios alongside ablation (`NO_CBP`, `NO_TRIAGE`, `NO_NMI`).
```bash
python nhcp_simulation_advanced.py
```
*Expected Outcome:* Outputs results to console and writes raw data to `advanced_simulation_results.json`.

### 3. Comparative & Sensitivity Simulation (Sections 8.7–8.8, Tables 11–12)
Compares TMGA activation strategy against `single-breach` and `three-cycle average` baselines, evaluating sensitivity to threshold $\tau_{drift}$.
```bash
python nhcp_simulation_comparative.py
```
*Expected Outcome:* Writes raw results to `comparative_sensitivity_results.json`.

### 4. Extended Multi-Dimensional Simulation (Section 8.9, Table 13)
Simulates 7 critical dimensions active simultaneously (`AGI Guard`, `ASI Guard`, `ASI Verify`, `AWI Void`, `AWI Sentry`, `CBP`, `NHCP`).
```bash
python nhcp_simulation_extended.py
```
*Expected Outcome:* Writes raw results to `extended_simulation_results.json`.

---

## 📊 Regulatory Compliance & Formal Verification

* **NIST AI RMF 1.0 & ISO/IEC 42001:** Fully mapped across GOVERN, MAP, MEASURE, and MANAGE functions. See [`docs/TMGA_NIST_ISO_Compliance_Matrix.pdf`](docs/TMGA_NIST_ISO_Compliance_Matrix.pdf).
* **Illustrative Circom Circuit:** A minimal example of the cryptographic verification relation described in Section 8.2. See [proofs/zkp/safety_check.circom](proofs/zkp/safety_check.circom).
* **Exploratory Multi-Agent Testbed:** Additional runtime conflict-resolution scenarios (not part of the main paper results). See [docs/TMGA_MultiAgent_Testbed_Simulation.pdf](docs/TMGA_MultiAgent_Testbed_Simulation.pdf).
  
---

## 📄 Citation

If you use TMGA, its 33-dimensional taxonomy, or the simulation testbeds in your research, please cite:

```bibtex
@article{themindgenesis2026tmga,
  title={The Mind Genesis Architecture: A Multidimensional Model for Shared Intelligence Ecosystems},
  author={The Mind Genesis},
  journal={arXiv preprint},
  year={2026},
  url={https://github.com/ahmett76/the-mind-genesis-architecture}
}
```

## 📜 License

This project is licensed under the **MIT License** - see the [LICENSE](LICENSE) file for details.
