pragma circom 2.1.6;

/*
    TMGA Constraint Check — Illustrative Circom Circuit
    ----------------------------------------------------

    This circuit provides a minimal illustration of a cryptographic
    verification relation of the form:

        R = {(x, w) | Phi(x, w) = 1}

    as discussed in the TMGA paper.

    The circuit checks two numerical constraints while allowing the
    corresponding witness values to remain private:

      1. The supplied ethical-confidence value is greater than or equal
         to the public minimum threshold.

      2. The supplied planned-resource value is less than or equal to
         the public resource cap.

    IMPORTANT SCOPE LIMITATIONS

    This circuit does not prove that an action is ethically correct,
    safe, aligned, or otherwise acceptable.

    It does not independently verify how confEthical was computed or
    whether the underlying inputs, rules, weights, measurements, or
    assumptions used to derive that value are valid.

    Likewise, it does not verify that plannedResource corresponds to
    actual physical or computational resource consumption.

    The circuit therefore demonstrates only that the supplied private
    witness values satisfy the two encoded numerical constraints.

    This is an illustrative reference circuit, not a production
    implementation or a formal verification of TMGA as a whole.
*/

include "circomlib/circuits/comparators.circom";


template TMGAConstraintCheck() {

    // -------------------------------------------------
    // Public inputs (x)
    // -------------------------------------------------

    // Minimum permitted ethical-confidence value.
    // Integer representation scaled by 1000.
    signal input tauMin;

    // Maximum permitted resource-usage value.
    signal input maxResourceCap;


    // -------------------------------------------------
    // Private witness values (w)
    // -------------------------------------------------

    // Supplied ethical-confidence value.
    // Integer representation scaled by 1000.
    //
    // This circuit checks the threshold relation only;
    // it does not verify the computation that produced
    // this value.
    signal input confEthical;

    // Supplied planned-resource value.
    //
    // This circuit checks the cap relation only;
    // it does not establish correspondence with actual
    // physical or computational resource consumption.
    signal input plannedResource;


    // -------------------------------------------------
    // Output
    // -------------------------------------------------

    signal output isValid;


    // -------------------------------------------------
    // Constraint 1
    //
    // confEthical >= tauMin
    // -------------------------------------------------

    component geqConf = GreaterEqThan(32);

    geqConf.in[0] <== confEthical;
    geqConf.in[1] <== tauMin;


    // -------------------------------------------------
    // Constraint 2
    //
    // plannedResource <= maxResourceCap
    // -------------------------------------------------

    component leqRes = LessEqThan(32);

    leqRes.in[0] <== plannedResource;
    leqRes.in[1] <== maxResourceCap;


    // -------------------------------------------------
    // Combined predicate
    //
    // isValid = 1 iff both encoded numerical
    // constraints are satisfied.
    // -------------------------------------------------

    isValid <==
        geqConf.out
        * leqRes.out;
}


component main {
    public [
        tauMin,
        maxResourceCap
    ]
} = TMGAConstraintCheck();
