# DECISIONS

## 1. Bronze is append-only
**Chosen:** preserve every source delivery with source and payload metadata.  
**Rejected:** overwrite a prior raw delivery when the same file/trip is replayed.  
**Why:** Bronze is the audit/rebuild layer. The replay therefore produces 144 trip delivery rows while the underlying 72 business trips are still represented downstream once.

## 2. Silver has one business row per `trip_id`
**Chosen:** `trip_id` as the business key, with source revision controlling valid updates. Replays are idempotent and conflicting same-revision content is rejected.  
**Rejected:** deduplicating by arbitrary row order.  
**Why:** the rule is deterministic and auditable.

## 3. Late data is incremental, not a rebuild
**Chosen:** ingest the supplied late-trip batch on top of the existing Silver lineage.  
**Why:** the trusted table moves to 75 rows and a rerun remains at the same logical content.

## 4. Schema enforcement fails closed
**Chosen:** reject unexpected/unapproved writes and prove atomic failure.  
**Rejected:** silently dropping unexpected columns or invalid rows.  
**Why:** trusted data should not change when validation fails.

## 5. Destructive Delta exercises use copies
**Chosen:** delete/restore/vacuum training exercises run on isolated copies or dry runs.  
**Why:** the trusted Silver table remains unchanged.

## 6. Streaming correctness includes checkpoint state
**Chosen:** preserve query checkpoint identity through stop/restart and reconcile producer/consumer offsets.  
**Why:** a restart must not silently duplicate or lose event content.

## 7. Quality is a promotion gate
**Chosen:** quarantine invalid candidates with explicit reason codes and block promotion.  
**Why:** a passing report is not enough if failed data can still reach trusted outputs.

## 8. Failure preserves the previous release
**Chosen:** downstream publication only occurs after dependency success.  
**Why:** the injected Lab 07 failure left the previous release intact, and the later rebuild produced equal logical content with a new run identity.

## 9. AI features use point-in-time availability
**Chosen:** features use an `as_of_utc` cut-off and only source information available by that time. Future labels remain `UNOBSERVED` until available.  
**Rejected:** using future outcomes to populate current feature rows.  
**Why:** prevents target leakage.

## 10. Performance claims stay bounded
**Chosen:** report the actual 72-row timings and their limits.  
**Rejected:** claiming that Delta is faster based on this run.  
**Why:** the observed local Delta median was slower than CSV and the dataset is too small for a general performance conclusion.
