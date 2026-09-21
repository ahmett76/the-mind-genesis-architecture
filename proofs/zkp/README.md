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
