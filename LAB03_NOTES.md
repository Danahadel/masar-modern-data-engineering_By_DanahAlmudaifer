# LAB03 Notes — Build incremental Silver

## What I did
I read the Day 1 Bronze output instead of rebuilding the raw data. I created typed staging tables, normalized values, validated driver relationships, built the trusted Silver trip table, ingested the fixed late batch, and tested rerun behavior. I also ran the provided dbt workflow.

## What I observed
Staging row counts:
- `stg_trips`: **144**
- `stg_drivers`: **6**
- `stg_gps`: **216**

Silver checks passed for:
- real Delta files,
- independent expected results,
- unique business keys,
- late rows retained,
- replay preserving business contents.

The late batch added three trips, so the trusted trip table moved from **72 to 75 business trips**.

dbt evidence:
- base: **72 rows**, **1794.60 SAR**
- rerun: **72 rows**, **1794.60 SAR**
- late: **75 rows**, **1875.60 SAR**
- late replay: **75 rows**, **1875.60 SAR**
- documented models: **6**
- documented sources: **3**

## Business key and precedence
The business key is **`trip_id`**. The implementation uses source revision to decide whether a newer delivery can update the trusted row. Replays do not create another business row, and same-revision conflicting content is rejected rather than silently chosen.

## Decision
Bronze keeps every delivery; Silver represents one trusted business trip. This separation gives me both auditability and idempotent business results.

## Blockers
None after the Day 1 handoff was restored.
