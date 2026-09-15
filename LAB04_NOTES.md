# LAB04 Notes — Delta operations

## What I did
I tested Delta transaction history, correction replay, schema enforcement, earlier-version reads, schema evolution, compaction, delete/restore, and a non-destructive vacuum exercise.

## What I observed
Transaction checks passed:
- correction matched the expected source correction,
- row count stayed **75**,
- replay and stale delivery preserved the correct values,
- same-revision conflict was rejected,
- an earlier Delta version was read successfully,
- a mixed valid/invalid batch was rejected atomically.

The trusted table moved from version **1** before the correction to version **2** after the correction while remaining at 75 business rows.

Maintenance checks passed:
- unexpected column rejected,
- approved schema evolution preserved business values,
- compaction preserved values,
- delete affected an isolated copy only,
- restore created a new commit,
- vacuum exercise was a dry run,
- trusted Silver remained unchanged.

## Decision
Potentially destructive maintenance exercises run only on isolated training copies. The trusted Silver table is not used as a sandbox.

## Blockers
None.
