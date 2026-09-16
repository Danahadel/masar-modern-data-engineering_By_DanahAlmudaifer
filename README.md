# Masar Mini-Lakehouse — Danah Adel Almudaifer

Masar Mini-Lakehouse is my end-to-end data-engineering capstone for a fictional mobility operator. It builds one reproducible lineage from raw batch and GPS event feeds into trustworthy reporting tables and point-in-time-correct AI feature tables. The project uses **synthetic data only**.

## Programme
Developed as part of **Modern Data Engineering for AI Systems (SDA-DSC-214)** at **SDAIA Academy**.  
SDAIA Academy: https://github.com/SDAIAAcademy  

#SDAIAAcademy


Course materials by Meaad Al-Marri. Original course repository attribution is preserved.

## Architecture

```text
Synthetic CSV / NDJSON
        |
        v
     Bronze
append-only raw deliveries
source + ingestion metadata
        |
        v
   Staging / Silver
typed + normalized + validated
one trusted business trip
        |
        +-------------------+
        |                   |
        v                   v
 Kafka GPS events       Quality gate
 Structured Streaming   Great Expectations
 checkpoints            quarantine + reasons
        |                   |
        +---------+---------+
                  |
                  v
                Gold
          /               \
         v                 v
       BI                  AI
 reporting grain     point-in-time features
```

### Layer guarantees
- **Bronze:** append-only archive of what arrived; replay is preserved.
- **Silver:** typed, normalized, driver-validated and deduplicated to one trusted trip definition.
- **Streaming:** real Kafka + Spark Structured Streaming with persistent checkpoint evidence.
- **Quality:** failed candidates are quarantined and cannot promote.
- **Gold/BI:** explicit reporting grains and reconciled totals.
- **AI:** feature availability is checked at the prediction cut-off and future labels are not fabricated.

### Environment setup

The tested course environment uses Python 3.11 and Java 17.

From the repository root:

```bash
python3.11 -m venv .venv
source .venv/bin/activate

python --version
java -version

python -m pip install -r requirements-course.txt -r requirements-day01.txt
python -m pip check
```

`requirements-course.txt` includes the pinned Day 4 and dbt dependencies, while
`requirements-day01.txt` provides the notebook/Jupyter environment.

For Day 4, the supplied Kafka setup also uses:

```bash
python -m pip install -r requirements-day04.txt
python -m pip check
```

See `docs/SETUP.md` and `day04/SETUP.md` for the complete environment and Kafka setup.

### Notebook execution order

Run the notebooks in dependency order:

```text
1. day01/STUDENT.ipynb  -> Labs 01–02
2. day02/STUDENT.ipynb  -> Lab 03
3. day03/STUDENT.ipynb  -> Lab 04
4. day04/STUDENT.ipynb  -> Labs 05–06
5. day05/STUDENT.ipynb  -> Labs 07–08
```

### Restoring handoff archives between sessions

Each day's final notebook cell creates an ignored handoff ZIP under `outputs/`.
When continuing in a fresh session, place the previous day's archive back under
`outputs/`, then extract it from the repository root so its relative paths are
preserved.

For Day 2:

```bash
cd /content/masar-modern-data-engineering
unzip -o outputs/day01_handoff.zip -d .
```

For Day 3:

```bash
unzip -o outputs/day02_handoff.zip -d .
```

For Day 4:

```bash
unzip -o outputs/day03_handoff.zip -d .
```

For Day 5:

```bash
unzip -o outputs/day04_handoff.zip -d .
```

The handoff ZIPs are runtime/session-transfer artifacts and are intentionally
excluded from normal Git commits. Day 2's separate dbt workspace evidence
should also be retained because later handoffs do not replace it.

## How to run

Clone my fork and use the `develop` branch:

```bash
git clone https://github.com/Danahadel/masar-modern-data-engineering_By_DanahAlmudaifer.git masar-modern-data-engineering
cd masar-modern-data-engineering
git switch develop
```

Install the course dependencies using the supplied requirements files, then execute the notebooks in dependency order:

```text
1. day01/STUDENT.ipynb  -> Labs 01–02
2. day02/STUDENT.ipynb  -> Lab 03
3. day03/STUDENT.ipynb  -> Lab 04
4. day04/STUDENT.ipynb  -> Labs 05–06
5. day05/STUDENT.ipynb  -> Labs 07–08
```

Between separate sessions, restore the prior day's supplied handoff workspace before continuing. The notebooks are committed with their observed outputs retained as assessment evidence.

## Results

### Source and Bronze
- 72 base trips
- 6 drivers
- 216 GPS events
- replayed trip deliveries: **144 rows**
- distinct base business trips remain **72**

### Silver
- staging trips: 144
- staging drivers: 6
- staging GPS events: 216
- late batch produces **75 trusted trips**
- late replay remains **75** logical rows

### Streaming
Transport rows by phase: **216, 216, 218, 219**  
Unique event IDs by phase: **216, 216, 216, 217**

The restart/checkpoint, offset reconciliation, source preservation and late-event checks passed.

### Quality gate
- invalid supplied quality cases quarantined: **7**
- approved trusted rows: **75**
- failed candidate promotion blocked

### BI reconciliation

| Metric | Trusted/Gold | BI | Difference |
|---|---:|---:|---:|
| Trip count | 75 | 75 | 0 |
| Fare total (SAR) | 1880.60 | 1880.60 | 0.00 |

Zone-level BI output:

| Zone | Trips | Fare SAR |
|---|---:|---:|
| Dammam | 25 | 670.40 |
| Jeddah | 25 | 625.20 |
| Riyadh | 25 | 585.00 |

### AI point-in-time behavior
The feature output records `as_of_utc`, history window and maximum source availability. The observed future label example remains `UNOBSERVED` with `target_trip_count=None`, rather than leaking future information.

## Decisions
See [DECISIONS.md](DECISIONS.md). Important choices include:
1. append-only Bronze,
2. deterministic Silver business-key/revision handling,
3. quality promotion that fails closed,
4. checkpoint-aware streaming recovery,
5. point-in-time AI features.

## Governance
See [GOVERNANCE.md](GOVERNANCE.md).

## Benchmarks
See [BENCHMARKS.md](BENCHMARKS.md).

## Limitations
- The dataset is small and synthetic: 72 base trips, 6 drivers and 216 base GPS events.
- The local scan timings are learning evidence, not production performance benchmarks.
- A successful local Kafka exercise demonstrates the tested restart/replay behavior; it is not evidence about every distributed Kafka failure mode.
- The project is intentionally a data pipeline, not a production ride-booking application or paid cloud deployment.

## Credits
This project was developed as part of **Modern Data Engineering for AI Systems (SDA-DSC-214) at SDAIA Academy** — https://github.com/SDAIAAcademy. **#SDAIAAcademy**

Course materials by **Meaad Al-Marri**. Attribution for reused course material is preserved.
