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

The benchmark was executed more than once during development against the
same synthetic 72-trip population. The notebook and machine-generated report
therefore preserve two separate valid executions.

Both executions returned the same logical result:

| Metric | Value |
|---|---:|
| Rows | 72 |
| Non-null fares | 72 |
| Fare total | 1794.60 SAR |

### Run preserved in `day01/STUDENT.ipynb`

This is the benchmark execution whose output is retained in the Day 1 notebook.

**CSV:** 0.4871, 0.3743, 0.4009, 0.4916 s  
Median: **0.4440 s**

**Delta v0:** 3.6888, 3.1597, 2.6092, 2.6271 s  
Median: **2.8934 s**

### Later run preserved in `reports/benchmark.json`

`reports/benchmark.json` contains a later execution of the same benchmark.

**CSV:** <COPY CURRENT REPORT SAMPLES HERE>  
Median: **<COPY CURRENT REPORT MEDIAN HERE> s**

**Delta v0:** <COPY CURRENT REPORT SAMPLES HERE>  
Median: **<COPY CURRENT REPORT MEDIAN HERE> s**

Across both executions:

- the source population remained 72 rows;
- the non-null fare count remained 72;
- the fare total remained 1794.60 SAR;
- CSV and Delta returned matching logical results;
- payload/query-result validation passed.

## Benchmark method

The benchmark used:

- one warm-up per storage variant;
- four measured repetitions per variant;
- alternating execution order between CSV and Delta;
- no explicit Spark cache.

The timing scope included query construction, planning, Spark action and
collection. Spark-session startup and ingestion were excluded.

OS, JVM, filesystem and metadata caches were not fully controlled.

## Interpretation

The exact wall-clock measurements varied between executions. This is expected
for a small local Spark workload where JVM warm-up and operating-system,
filesystem and metadata caching are not fully controlled.

Delta was slower than CSV in the observed local runs, but I do **not** interpret
this as evidence that CSV is generally faster than Delta, nor do I claim a
Delta speed-up from this learning dataset.

The useful evidence is that both formats were evaluated against the same
population, produced the same logical result, and were measured using an
explicit and repeatable procedure.

## Limitations

- The dataset contains only 72 synthetic trips.
- Execution was performed on local/Colab compute and storage.
- OS, JVM, filesystem and metadata caches were not fully controlled.
- The measurements do not represent distributed-cluster performance.
- The cost model uses teaching units, not real cloud pricing.
- No general CSV-versus-Delta performance ranking can be inferred from these results.

