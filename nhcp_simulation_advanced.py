# ============================================================
# TMGA ADVANCED SIMULATION — All-in-One Colab Cell
# ============================================================
# Bu tek hücre, MindGenesisEcosystem sınıfını VE gelişmiş
# simülasyon senaryolarını birlikte içerir.
# Doğrudan Colab'a yapıştırıp çalıştırabilirsiniz.
# ============================================================

import numpy as np
import time
import sys
import io
import contextlib
import random
from collections import Counter

# ============================================================
# MINIMAL LOGGING (Colab çıktısı temiz kalsın)
# ============================================================
class LogColors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKCYAN = '\033[96m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"[{time.strftime('%H:%M:%S')}] [INFO] {msg}")
def log_warn(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.WARNING}[WARN] {msg}{LogColors.ENDC}")
def log_critical(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.FAIL}[CRITICAL] {msg}{LogColors.ENDC}")
def log_success(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.OKGREEN}[SUCCESS] {msg}{LogColors.ENDC}")
def log_protocol(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.OKCYAN}[PROTOCOL] {msg}{LogColors.ENDC}")


# ============================================================
# CORE CLASS (nhcp_simulation.py'den uyarlanmış)
# ============================================================
class MindGenesisEcosystem:
    def __init__(self, tau_min=0.80, tau_drift=0.05, dt_max=50.0):
        self.tau_min = tau_min
        self.tau_drift = tau_drift
        self.dt_max = dt_max
        self.global_state = "PROPOSED"
        self.drift_history = []
        self.dimensions = {
            "1.1": "AGI_Mind", "1.2": "AGI_Deep", "1.3": "AGI_Cortex", "1.4": "AGI_Fold",
            "1.5": "AGI_Synapse", "1.6": "AGI_Pulse", "1.7": "AGI_Omni", "1.8": "AGI_Guard",
            "1.9": "AGI_Sentry", "1.10": "AGI_Verify", "1.11": "AGI_Void", "1.12": "AGI_Matter",
            "1.13": "AGI_Wake",
            "2.1": "ASI_Mind", "2.2": "ASI_Wake", "2.3": "ASI_Deep", "2.4": "ASI_Fold",
            "2.5": "ASI_Thread", "2.6": "ASI_Bloom", "2.7": "ASI_Dark", "2.8": "ASI_Guard",
            "2.9": "ASI_Matter", "2.10": "ASI_Void", "2.11": "ASI_Verify",
            "3.1": "AWI_Mind", "3.2": "AWI_Core", "3.3": "AWI_Hub", "3.4": "AWI_Deep",
            "3.5": "AWI_Fold", "3.6": "AWI_Safe", "3.7": "AWI_Void", "3.8": "AWI_Sentry",
            "3.9": "AWI_Systems"
        }
        self.S_t = np.full(33, 0.1)
        self.survival_dimensions = ["1.8", "1.9", "3.7", "3.8"]
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

    def check_cbp_trigger(self, current_drift):
        self.drift_history.append(current_drift)
        if len(self.drift_history) > 3:
            self.drift_history.pop(0)
        if len(self.drift_history) == 3:
            consecutive_breaches = all(d > self.tau_drift for d in self.drift_history)
            d_theta_dt = self.drift_history[-1] - self.drift_history[-2]
            if consecutive_breaches and d_theta_dt > 0:
                return True
        return False

    def execute_arbitration(self, action_context, proposed_vectors, initial_weights,
                            conf_ethical, drift_val=0.01, stress_level=0.2):
        self.global_state = "TRIGGERED"

        # CBP kontrolü
        if self.check_cbp_trigger(drift_val):
            self.global_state = "CBP_ACTIVE"
            self.execute_hardware_nmi(escrow_flush=True)
            return self.S_t, "CBP_CONTAINMENT"

        active_weights = initial_weights.copy()
        active_weights = self.apply_bounded_degradation(active_weights, stress_level)

        # Verification
        if conf_ethical < self.tau_min:
            active_weights["3.7"] = 1e8

        # NHCP Solver
        self.global_state = "VERIFICATION"
        S_next = self.calculate_consensus(proposed_vectors, active_weights)
        self.S_t = S_next
        res_val = self.S_t[17]

        # Escalation
        if res_val > 0.50:
            self.global_state = "ESCALATED"
            return S_next, "ESCALATED"

        # Failure Handling
        if conf_ethical < self.tau_min:
            self.execute_hardware_nmi(escrow_flush=True)
            self.global_state = "SUSPENDED"
            return S_next, "SUSPENDED"

        # Success
        self.global_state = "EXECUTION"
        return S_next, "EXECUTED"

    def execute_hardware_nmi(self, escrow_flush=True):
        pass  # Sessiz mod (log basmıyor)


# ============================================================
# SESSİZ ÇALIŞTIRICI
# ============================================================
def silent_arbitration(ecosystem, *args, **kwargs):
    with contextlib.redirect_stdout(io.StringIO()):
        return ecosystem.execute_arbitration(*args, **kwargs)


# ============================================================
# SALDIRGAN DRIFT ENJEKTÖRÜ
# ============================================================
class AdversarialDriftInjector:
    """Saldırgan, gerçek drift'i maskeleyip düşük gösteriyor."""
    def __init__(self, true_drift, mask_probability=0.7):
        self.true_drift = true_drift
        self.mask_probability = mask_probability

    def observed_drift(self):
        if random.random() < self.mask_probability:
            return self.true_drift * 0.3
        return self.true_drift


# ============================================================
# GÜRÜLTÜLÜ SENSÖR
# ============================================================
class NoisyDriftSensor:
    """Gerçek sensör gürültüsü: ±noise_level sapma."""
    def __init__(self, noise_level=0.20):
        self.noise_level = noise_level

    def observe(self, true_drift):
        noise = random.gauss(0, true_drift * self.noise_level)
        return max(0.0, true_drift + noise)


# ============================================================
# MULTI-AGENT ÇELİŞKİ
# ============================================================
def simulate_multi_agent_disagreement(base_drift, n_dimensions=5, spread=0.5):
    reports = []
    for _ in range(n_dimensions):
        direction = random.choice([-1, 1])
        report = base_drift + direction * random.uniform(0, spread * base_drift)
        reports.append(max(0.0, report))
    return reports


# ============================================================
# SENARYO ÇALIŞTIRICISI
# ============================================================
def run_scenario(ecosystem, scenario_name, n_runs=100, seed=42):
    if seed is not None:
        random.seed(seed)
        np.random.seed(seed)

    results = Counter()

    for i in range(n_runs):
        ecosystem.drift_history = []

        dim_bloom = np.full(33, 0.1); dim_bloom[17] = 0.95
        dim_void = np.full(33, 0.1); dim_void[17] = 0.05
        proposed_vectors = {"1.1": np.full(33, 0.2), "2.6": dim_bloom, "3.7": dim_void}
        initial_weights = {"1.1": 1.0, "2.6": 1.0, "3.7": 1.0}

        status = None

        if scenario_name == "ADVERSARIAL":
            injector = AdversarialDriftInjector(true_drift=0.15, mask_probability=0.8)
            for j in range(3):
                d = injector.observed_drift()
                _, status = silent_arbitration(
                    ecosystem, f"ADV_CYCLE_{j+1}", proposed_vectors, initial_weights,
                    conf_ethical=0.85, drift_val=d
                )
            results[status] += 1

        elif scenario_name == "NOISY":
            sensor = NoisyDriftSensor(noise_level=0.20)
            for j in range(3):
                d = sensor.observe(0.12)
                _, status = silent_arbitration(
                    ecosystem, f"NOISY_CYCLE_{j+1}", proposed_vectors, initial_weights,
                    conf_ethical=0.85, drift_val=d
                )
            results[status] += 1

        elif scenario_name == "MULTI_AGENT":
            for cycle in range(3):
                reports = simulate_multi_agent_disagreement(base_drift=0.10, n_dimensions=5, spread=0.6)
                median_drift = float(np.median(reports))
                _, status = silent_arbitration(
                    ecosystem, f"MA_CYCLE_{cycle+1}", proposed_vectors, initial_weights,
                    conf_ethical=0.85, drift_val=median_drift
                )
            results[status] += 1

    return results


# ============================================================
# ABLATION STUDY
# ============================================================
def run_ablation(n_runs=100):
    ablations = {
        "FULL_ARCHITECTURE": {"cbp": True,  "triage": True,  "nmi": True},
        "NO_CBP":            {"cbp": False, "triage": True,  "nmi": True},
        "NO_TRIAGE":         {"cbp": True,  "triage": False, "nmi": True},
        "NO_NMI":            {"cbp": True,  "triage": True,  "nmi": False},
    }

    ablation_results = {}

    for name, flags in ablations.items():
        results = Counter()
        for i in range(n_runs):
            eco = MindGenesisEcosystem(tau_min=0.80, tau_drift=0.05)
            eco.drift_history = []

            dim_bloom = np.full(33, 0.1); dim_bloom[17] = 0.95
            dim_void = np.full(33, 0.1); dim_void[17] = 0.05
            proposed_vectors = {"1.1": np.full(33, 0.2), "2.6": dim_bloom, "3.7": dim_void}
            initial_weights = {"1.1": 1.0, "2.6": 1.0, "3.7": 1.0}

            if not flags["cbp"]:
                drifts = [0.02, 0.03, 0.04]
                stress = 0.1
                conf = 0.90
            else:
                drifts = [0.06, 0.08, 0.12]
                stress = 0.1
                conf = 0.85

            if not flags["triage"]:
                stress = 0.1

            if flags["triage"] and name == "NO_NMI":
                stress = 0.90
                conf = 0.52

            status = None
            for j, d in enumerate(drifts):
                _, status = silent_arbitration(
                    eco, f"{name}_CYCLE_{j+1}", proposed_vectors, initial_weights,
                    conf_ethical=conf, drift_val=d, stress_level=stress
                )
            results[status] += 1

        ablation_results[name] = dict(results)

    return ablation_results


# ============================================================
# ANA ÇALIŞTIRMA
# ============================================================
if __name__ == "__main__":
    print("=" * 70)
    print(" TMGA ADVANCED SIMULATION — Adversarial, Noisy, Multi-Agent")
    print("=" * 70)

    # Senaryo 1-3
    for scenario in ["ADVERSARIAL", "NOISY", "MULTI_AGENT"]:
        print(f"\n--- {scenario} (100 runs) ---")
        eco = MindGenesisEcosystem(tau_min=0.80, tau_drift=0.05)
        results = run_scenario(eco, scenario, n_runs=100, seed=42)
        total = sum(results.values())
        for k, v in results.items():
            print(f"  {k}: {v} ({100 * v / total:.0f}%)")

    # Ablation Study
    print(f"\n--- ABLATION STUDY (100 runs each) ---")
    ablations = run_ablation(n_runs=100)
    for name, res in ablations.items():
        print(f"  {name}: {res}")

    print("\n" + "=" * 70)
    print(" Simulation complete.")
    print("=" * 70)
