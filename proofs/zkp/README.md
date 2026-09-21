# Illustrative Zero-Knowledge Constraint Example

This directory contains a minimal Circom example accompanying the
cryptographic-verifiability discussion in The Mind Genesis Architecture
(TMGA).

The main example is:

[`safety_check.circom`](safety_check.circom)

## Purpose

The circuit illustrates a verification relation of the form:

```text
R = {(x, w) | Φ(x, w) = 1}
```

where `x` represents public inputs and `w` represents private witness
values.

The example checks two numerical constraints:

1. the supplied ethical-confidence value is greater than or equal to a
   public minimum threshold; and
2. the supplied planned-resource value is less than or equal to a
   public resource cap.

The example is intended to demonstrate how selected TMGA constraints
could be represented in a proof-oriented circuit.

## Scope and Limitations

This example does **not** prove that an action is ethical, safe, aligned,
or otherwise acceptable.

In particular, the circuit does not independently establish:

- that `confEthical` was computed correctly;
- that the rules, weights, measurements, or assumptions used to derive
  `confEthical` are valid;
- that `plannedResource` corresponds to actual physical or computational
  resource consumption;
- that the complete TMGA architecture has been formally verified;
- that the proposed 33-dimensional taxonomy has been empirically
  validated; or
- that satisfying the encoded constraints provides a real-world safety
  guarantee.

The circuit verifies only the numerical relations explicitly encoded in
the constraint system.

## Zero-Knowledge Context

Circom specifies an arithmetic constraint system. Whether witness values
are protected through a zero-knowledge proof depends on the proving
system, circuit compilation, proof-generation procedure, verification
procedure, and associated implementation choices.

Accordingly, this repository should not be interpreted as providing a
complete production zero-knowledge deployment.

## Status

The circuit is an illustrative research example.

It is:

- not a production circuit;
- not a complete TMGA implementation;
- not a safety certification mechanism;
- not a proof of ethical correctness; and
- not formally audited.

## Related Material

The accompanying TMGA paper discusses cryptographic verifiability for
opaque architectures and introduces the reference relation:

```text
R = {(x, w) | Φ(x, w) = 1}
```

The implementation in this directory provides a small executable
illustration of that concept rather than a formal verification of TMGA
as a whole.
