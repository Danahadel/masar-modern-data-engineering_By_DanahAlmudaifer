# LAB05 Notes — Stream events and resume safely

## What I did
I ran a real local Kafka broker in Colab, verified the Python Kafka client, used Spark Structured Streaming with the Spark Kafka connector, and exercised the supplied stop/restart/replay/late-event scenario.

## What I observed
Kafka was reachable on `127.0.0.1:9092`, and a test topic was created successfully.

Observed transport rows by phase:
`[216, 216, 218, 219]`

Observed distinct event IDs by phase:
`[216, 216, 216, 217]`

The streaming validation passed for:
- expected transport and event counts,
- unique transport keys,
- same query identity after restart,
- new execution IDs after restart,
- persistent checkpoint files,
- producer/consumer offset reconciliation,
- source JSON preservation,
- event content matching the source,
- Delta readback of unique events,
- events linked to trusted trips,
- retention of the supplied late event.

## Event time vs processing time
`event_ts` is the time recorded by the source event. Processing time is when Spark/Kafka handles the event. They are not interchangeable: a late event can have an old event timestamp but arrive during a later processing run.

## Blocker and recovery
Spark initially reported that it could not find the Kafka data source. I fixed this by loading `org.apache.spark:spark-sql-kafka-0-10_2.12:3.5.8` before the Spark JVM started. The final executed streaming checks all passed.

## Decision
Checkpoint state is persistent and part of the streaming correctness model; I do not treat a restart as a new logical stream.
