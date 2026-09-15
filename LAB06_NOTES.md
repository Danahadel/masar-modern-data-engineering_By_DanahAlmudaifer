# LAB06 Notes — Quality gate and governance

## What I did
I ran the Great Expectations quality workflow at the promotion boundary, tested the supplied invalid quality cases, quarantined failed records with reason codes, and verified that an unsafe candidate was not promoted.

## What I observed
All quality checks passed, including:
- trusted/rechecked data passes GX,
- mixed candidate fails GX,
- expected mixed counts,
- reason codes match the reference rules,
- failed candidate is not promoted,
- quarantine Delta readback,
- approved readback matches trusted business contents,
- source Silver remains untouched,
- Data Docs exist for all three cases.

The quality test quarantined **7 records**. Example reason codes were:
- `MISSING_TRIP_ID`
- `INVALID_FARE`
- `UNKNOWN_DRIVER`
- `INVALID_TIMESTAMP`
- `INVALID_DURATION`
- `INVALID_DISTANCE`
- `INVALID_CITY`

Approved rows after the gate: **75**.

## Decision
The quality gate is a promotion boundary, not only a report. Failed candidates go to quarantine with reasons and trusted outputs remain unchanged.

## Governance note
The project uses only the supplied synthetic Masar data. Lineage, ownership, intended access and retention are documented in `GOVERNANCE.md`.

## Blockers
Great Expectations was pinned to the course-compatible version used in the executed Colab run.
