# LAB02 Notes — Cost and local scan evidence

## What I did
I compared an always-on compute assumption with scheduled compute using hypothetical teaching units, then measured CSV and Delta scans using Spark and checked that both returned the same logical aggregate.

## Cost assumptions and result
The values are **teaching units, not currency**.

- Always-on total: **1460 TU**
- Scheduled total at the base assumption: **185 TU**
- Difference: **1275 TU**
- Break-even work time: **23.25 hours/day**
- Counterexample: at **23.75 hours/day**, scheduled compute becomes **1490 TU**, which is more expensive than the 1460 TU always-on case.

## Measured Spark result
Both formats returned:
- Rows: **72**
- Non-null fares: **72**
- Fare total: **1794.60 SAR**

Observed local medians:
- CSV: **0.444 s**
- Delta v0: **2.893 s**

Delta was slower in this tiny local run. I do not use this result to claim that CSV is generally faster or that Delta gives a speed-up. The dataset is intentionally small, so these timings are evidence of this run only.

## Decision
I separate the architectural cost argument from the local performance measurement. The cost model explains compute-storage separation; the Spark benchmark records what actually happened on this small dataset.

## Blockers
### Timing variability

I repeated the local benchmark during development. The exact scan timings
changed between runs, while the logical result remained identical.

This is expected for a small local Spark benchmark because JVM warm-up,
filesystem state, metadata caching and OS caching were not fully controlled.

For that reason, I do not claim a general CSV-versus-Delta performance
ranking from these measurements.
