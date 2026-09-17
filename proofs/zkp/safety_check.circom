pragma circom 2.1.6;

/*
    TMGA Safety Check — Illustrative Circom Circuit
    -------------------------------------------------
    This circuit is a minimal illustration of the cryptographic
    relation R = {(x, w) | Phi(x, w) = 1} described in Section 8.2.1
    of the paper.

    It verifies two properties without revealing the private witness:
      1. The agent's ethical confidence is at least the public threshold.
      2. The agent's planned resource usage does not exceed the public cap.

    NOT a production circuit. Provided for illustration only.
*/

include "circomlib/circuits/comparators.circom";

template TMGASafetyCheck() {
    // === Public inputs (x) ===
    signal input tauMin;          // minimum ethical confidence (scaled by 1000)
    signal input maxResourceCap;  // maximum permitted resource usage

    // === Private witness (w) ===
    signal input confEthical;     // computed ethical confidence (scaled by 1000)
    signal input plannedResource; // planned resource usage

    // === Output ===
    signal output isValid;

    // Constraint 1: confEthical >= tauMin
    component geqConf = GreaterEqThan(32);
    geqConf.in[0] <== confEthical;
    geqConf.in[1] <== tauMin;

    // Constraint 2: plannedResource <= maxResourceCap
    component leqRes = LessEqThan(32);
    leqRes.in[0] <== plannedResource;
    leqRes.in[1] <== maxResourceCap;

    // Both constraints must hold.
    isValid <== geqConf.out * leqRes.out;
}

component main {public [tauMin, maxResourceCap]} = TMGASafetyCheck();
