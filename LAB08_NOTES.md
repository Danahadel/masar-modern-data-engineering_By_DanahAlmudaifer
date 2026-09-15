# LAB08 Notes — Serve AI and BI

## What I did
I produced Gold, BI and AI outputs from the same trusted lineage and validated their schemas, grains, keys and reconciliation.

## What I observed
All serving checks passed, including:
- Gold/BI/AI schemas and keys,
- fact grain of **75 trips**,
- valid foreign keys,
- Gold/fact totals match,
- events aggregated before the join,
- group grains reconcile,
- labels are not fabricated,
- feature availability is checked,
- feature and label keys align.

BI totals:
| Zone | Trips | Fare SAR |
|---|---:|---:|
| Dammam | 25 | 670.40 |
| Jeddah | 25 | 625.20 |
| Riyadh | 25 | 585.00 |
| **Total** | **75** | **1880.60** |

The trusted total and BI total reconcile with a difference of **0 trips** and **0.00 SAR**.

## Point-in-time correctness
The AI feature example uses an `as_of_utc` cut-off and records the maximum source availability time. The future label for the shown prediction hour is `UNOBSERVED` with no fabricated target value. This keeps future information out of the feature row.

## Decision
BI outputs and AI features come from the same trusted lineage, but their grains and time rules are explicit and different.

## Blockers
None.
