# LAB01 Notes — Land and inspect raw feeds

## What I did
I verified the supplied source manifest before processing, inspected the three synthetic feeds, and created real Delta Bronze tables with source and ingestion metadata. I then replayed the trip delivery without overwriting Bronze history.

## What I observed
- Manifest files verified: **10**
- Base trips: **72**
- Drivers: **6**
- GPS events: **216**
- After the intentional trip replay, Bronze contains **144 trip delivery rows** while the business trip count remains **72**.
- The base files had no duplicate business keys, missing top-level fields, broken driver/trip links, or invalid coordinates.
- I observed a real label-conformance issue: **10 trip rows** changed when city labels were normalized. The raw labels included whitespace/case variants such as ` riyadh ` and `Riyadh`.

## Observed defect vs risk
**Observed defect:** inconsistent city formatting in 10 source rows.

**Risks I designed for:**
1. A source file can be replayed, which can duplicate deliveries if Bronze is overwritten or Silver is not deduplicated.
2. Late batches can arrive after the original batch and must still be included in the trusted table.
3. A source can change schema or send a corrected record, so downstream layers need explicit enforcement and correction rules.

## Decision
Bronze is append-only and preserves source/payload hashes. I do not deduplicate Bronze because it is the archive of what arrived. Deduplication belongs in Silver.

## Blockers
No data blocker was observed in the base source inspection.
