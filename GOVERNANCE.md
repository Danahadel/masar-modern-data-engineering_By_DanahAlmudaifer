# GOVERNANCE

## Dataset classification
All data in this repository is **synthetic Masar training data**. No real rider, driver, personal, credential, or real coordinate data is added to the fork.

## Lineage
`source files -> Bronze -> staging/Silver -> quality-approved trusted data -> Gold -> BI and AI products`

Kafka GPS events join the same trusted lineage after streaming ingestion and validation.

## Ownership
| Asset | Intended owner |
|---|---|
| Source/Bronze ingestion | Data Engineering |
| Silver trusted trip definition | Data Engineering |
| Quality rules / quarantine | Data Engineering with data-owner review |
| Gold / BI products | Data Engineering / Analytics |
| AI feature definitions | Data Engineering / Data Science |

## Intended access
- Bronze: engineering/audit use because it preserves raw deliveries and ingestion metadata.
- Silver: trusted internal business-level data for downstream products.
- Quarantine: engineering/data-quality review.
- Gold/BI: reporting consumers.
- AI feature/label tables: model-development consumers with point-in-time rules.

## Retention
For this training project, Bronze is retained as the append-only archive of record for the life of the project. Silver and Gold are reproducible from Bronze and the documented transformations. Runtime caches, Kafka data directories, handoff ZIPs, environments and large generated Delta artifacts are kept out of normal Git history.

## Quality and observability
The promotion boundary uses Great Expectations and explicit quarantine reason codes. A failed candidate is not promoted. Run-health observations include source counts, streaming offset/count reconciliation, checkpoint evidence, quality-gate status, and serving reconciliation.

## Security
No passwords, tokens, private keys or `.env` secrets belong in the repository. GitHub credentials are provided through the execution environment, not notebook cells.
