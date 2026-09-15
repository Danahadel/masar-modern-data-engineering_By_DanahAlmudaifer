# LAB07 Notes — Integrate the Mini-Lakehouse

## What I did
I connected the accumulated pipeline and ran the supplied recovery exercise to prove that a downstream release is protected when an injected failure occurs.

## What I observed
All recovery checks passed:
- injected failure observed,
- previous release preserved,
- rebuild received a new identity,
- rebuilt logical content equals the previous valid content.

## Decision
A run is publishable only after its upstream dependencies succeed. Failure must preserve the previous good release instead of exposing a partial new one.

## Recovery attempt
The deliberate failure was followed by a clean rebuild. I compared logical contents rather than volatile run IDs/timestamps.

## Evidence preservation
I continued from the accumulated Day 1–4 workspace rather than rebuilding an unrelated fresh dataset.
