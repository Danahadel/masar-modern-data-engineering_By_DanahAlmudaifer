# BENCHMARKS

## Scope
These measurements come from my local/Colab execution of the supplied **synthetic 72-trip learning dataset**. They are not production performance benchmarks.

## Hypothetical cost model
The cost model uses **teaching units (TU), not currency**.

| Scenario | Result |
|---|---:|
| Always-on total | 1460 TU |
| Scheduled total at base assumption | 185 TU |
| Difference | 1275 TU |
| Break-even work time | 23.25 h/day |

A counterexample was tested at 23.75 h/day: scheduled compute was 1490 TU, higher than 1460 TU always-on. This shows scheduled operation is not automatically cheaper in every usage pattern.

## Spark scan measurement
Both scans returned exactly the same logical result:

| Metric | Value |
|---|---:|
| Rows | 72 |
| Non-null fares | 72 |
| Fare total | 1794.60 SAR |

Observed samples:

**CSV:** 0.4871, 0.3743, 0.4009, 0.4916 s  
Median: **0.4440 s**

**Delta v0:** 3.6888, 3.1597, 2.6092, 2.6271 s  
Median: **2.8934 s**

## Interpretation
Delta was slower in this tiny run. I do not claim a Delta speed-up from this dataset. The useful evidence is that both scans returned equal results and that I inspected/measured the actual execution rather than making an unsupported performance claim.


## Repeated-run note

The benchmark was executed more than once during development on the same
72-row synthetic population.

The saved notebook contains an earlier run, while `reports/benchmark.json`
contains a later repeated run. The exact wall-clock timings varied between
executions, which is expected for this small local Spark workload because
OS, JVM and metadata caches were not controlled.

Across the runs, the logical result remained unchanged:

- 72 rows
- 72 non-null fares
- fare total = 1794.60 SAR
- CSV and Delta payloads matched
- query-result validation passed

Therefore, these timings are treated only as local observations and not as
evidence that one storage format is generally faster than the other.
