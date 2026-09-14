#!/usr/bin/env python3
r"""
THE MIND GENESIS ARCHITECTURE (TMGA) - REFERENCE IMPLEMENTATION
Non-Hierarchical Consensus Protocol (NHCP), Circuit Breaker Protocol (CBP)
& Hardware Escrow Buffer Simulation

Reference simulation for Section 8.5 of the manuscript.
"""

import numpy as np
import time

class LogColors:
    HEADER = '\033[95m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    OKGREEN = '\033[92m'
    OKCYAN = '\033[96m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'

def log_info(msg): print(f"[{time.strftime('%H:%M:%S')}] [INFO] {msg}")
def log_warn(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.WARNING}[WARN] {msg}{LogColors.ENDC}")
def log_critical(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.FAIL}[CRITICAL] {msg}{LogColors.ENDC}")
def log_success(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.OKGREEN}[SUCCESS] {msg}{LogColors.ENDC}")
def log_protocol(msg): print(f"[{time.strftime('%H:%M:%S')}] {LogColors.OKCYAN}[PROTOCOL] {msg}{LogColors.ENDC}")


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

        if self.check_cbp_trigger(drift_val):
            self.global_state = "CBP_ACTIVE"
            return self.S_t, "CBP_CONTAINMENT"

        active_weights = initial_weights.copy()
        active_weights = self.apply_bounded_degradation(active_weights, stress_level)

        if conf_ethical < self.tau_min:
            active_weights["3.7"] = 1e8

        self.global_state = "VERIFICATION"
        S_next = self.calculate_consensus(proposed_vectors, active_weights)
        self.S_t = S_next
        res_val = self.S_t[17]

        if res_val > 0.50:
            self.global_state = "ESCALATED"
            return S_next, "ESCALATED"

        if conf_ethical < self.tau_min:
            self.global_state = "SUSPENDED"
            return S_next, "SUSPENDED"

        self.global_state = "EXECUTION"
        return S_next, "EXECUTED"


if __name__ == "__main__":
    # Parameters from manuscript Section 8.5.1
    ecosystem = MindGenesisEcosystem(tau_min=0.80, tau_drift=0.05)

    dim_bloom = np.full(33, 0.1); dim_bloom[17] = 0.95
    dim_void = np.full(33, 0.1); dim_void[17] = 0.05
    proposed_vectors = {"1.1": np.full(33, 0.2), "2.6": dim_bloom, "3.7": dim_void}
    initial_weights = {"1.1": 1.0, "2.6": 1.0, "3.7": 1.0}

    # --- NOMINAL (100 runs) ---
    results = {"EXECUTED": 0, "SUSPENDED": 0, "CBP_CONTAINMENT": 0, "ESCALATED": 0}
    for i in range(100):
        ecosystem.drift_history = []
        _, status = ecosystem.execute_arbitration(
            "NOMINAL", proposed_vectors, initial_weights,
            conf_ethical=0.90, drift_val=0.02, stress_level=0.1
        )
        results[status] += 1
    print("\n=== NOMINAL (100 runs) ===")
    for k, v in results.items():
        print(f"{k}: {v} ({v}%)")

    # --- STRESS (100 runs) ---
    results = {"EXECUTED": 0, "SUSPENDED": 0, "CBP_CONTAINMENT": 0, "ESCALATED": 0}
    for i in range(100):
        ecosystem.drift_history = []
        _, status = ecosystem.execute_arbitration(
            "STRESS", proposed_vectors, initial_weights,
            conf_ethical=0.75, drift_val=0.065, stress_level=0.1
        )
        results[status] += 1
    print("\n=== STRESS (100 runs) ===")
    for k, v in results.items():
        print(f"{k}: {v} ({v}%)")

    # --- CBP (100 runs) ---
    results = {"EXECUTED": 0, "SUSPENDED": 0, "CBP_CONTAINMENT": 0, "ESCALATED": 0}
    for i in range(100):
        ecosystem.drift_history = []
        ecosystem.execute_arbitration("CYCLE_1", proposed_vectors, initial_weights,
                                       conf_ethical=0.85, drift_val=0.06)
        ecosystem.execute_arbitration("CYCLE_2", proposed_vectors, initial_weights,
                                       conf_ethical=0.85, drift_val=0.08)
        _, status = ecosystem.execute_arbitration("CYCLE_3", proposed_vectors, initial_weights,
                                                   conf_ethical=0.85, drift_val=0.12)
        results[status] += 1
    print("\n=== CBP (100 runs) ===")
    for k, v in results.items():
        print(f"{k}: {v} ({v}%)")
