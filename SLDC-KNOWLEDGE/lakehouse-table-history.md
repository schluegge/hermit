# Lakehouse table history: snapshots, time travel, and retention

Verification date: 2026-08-20

Status: verified representative baseline for Apache Iceberg, Delta Lake, and Apache Hudi table-history semantics.

## Baseline definition

A lakehouse table-history layer records logical table states over time and exposes one or more mechanisms for reading, retaining, branching, restoring, or incrementally consuming those states. The exact identity model and retention semantics are format-specific.

This evidence plane is separate from generic data versioning (`data-versioning-lineage.md`): DVC/lakeFS version broader data artifacts or object-store states, while the systems here define transactional table-history semantics inside lakehouse table formats.

## SDLC / data-lifecycle role

Verified roles include:

- reproducible analytics and ML reads against an identified historical table state;
- debugging and audit reads of prior table states;
- controlled validation of candidate table changes where the format supports isolated references/branches;
- incremental/change-oriented downstream processing where supported;
- retention and garbage-collection policy that deliberately bounds how much historical state remains readable.

A historical read is evidence of a retained table state. It is not by itself evidence that the data is correct, complete, policy-compliant, or suitable for model/release promotion.

## Apache Iceberg 1.11.0

**Source scope:** Apache Iceberg official documentation/specification and official release record. Iceberg 1.11.0 was released 2026-05-19/20 and is the current release identified during this verification.

### Verified semantics

Iceberg table metadata maintains a snapshot log. Snapshots are the basis for reader isolation and time-travel queries. Spark integrations support `TIMESTAMP AS OF` and `VERSION AS OF`, with `VERSION AS OF` accepting a snapshot ID or a branch/tag name.

Iceberg also supports named snapshot references:

- **tags** identify individual snapshots;
- **branches** are mutable named references to snapshot lineages;
- branch/tag retention is configurable independently from ordinary table-history retention;
- `expire_snapshots` removes snapshots/files no longer protected by applicable retention rules.

Iceberg explicitly documents Write-Audit-Publish style workflows: writes can target an audit branch, validation can run against that branch, and the main branch can be fast-forwarded only after validation.

### Important boundary

Schema selection differs by access path. Iceberg documents that time travel to a concrete snapshot/timestamp uses the snapshot schema, while reading the head of a branch uses the current table schema. Automation must therefore preserve whether the reference is a snapshot ID, tag, branch, or timestamp rather than treating them as interchangeable strings.

### Selection / integration criteria

Prefer Iceberg history semantics when the selected execution engines and catalog support the required Iceberg features and when named branches/tags or WAP-style isolated validation are materially useful. Verify engine-specific support before assuming Java-library, Spark, and Flink behavior is identical.

Integration points include catalog metadata, Spark/Flink reads and writes, validation jobs, retention maintenance, audit pipelines, and reproducibility metadata that records the exact snapshot/reference consumed by a run.

### Automation possibilities

Deterministic automation can:

1. record the current snapshot ID before a data/ML job;
2. create a temporary branch or tag where supported;
3. run validation against that identified state;
4. fast-forward/publish only after explicit quality/security policy gates;
5. expire snapshots according to separately reviewed retention policy.

AI may assist with investigation or proposing retention/validation changes, but no source reviewed here grants an AI system autonomous authority to publish or expire production history.

## Delta Lake 4.3.1

**Source scope:** Delta Lake official documentation plus the maintainer GitHub release page. The maintainer release page identifies 4.3.1 as latest, released 2026-07-08, during this verification.

### Verified semantics

Delta Lake uses its transaction log as the source of truth for table state. It supports historical reads using:

- `TIMESTAMP AS OF`;
- `VERSION AS OF`;
- DataFrame options `timestampAsOf` and `versionAsOf`.

The documentation explicitly presents time travel for reproducibility, debugging/auditing, temporal analysis, and recovery-oriented workflows.

History availability depends on **both** transaction-log retention and retention of the underlying data files. Current documentation states:

- `delta.logRetentionDuration` defaults to 30 days;
- `delta.deletedFileRetentionDuration` defaults to 7 days;
- `VACUUM` deletes eligible data files and can make older table versions unreadable;
- `VACUUM` is not triggered automatically;
- retention must exceed the longest relevant concurrent transaction and stream lag to avoid removing files still needed by readers/writers.

`VACUUM DRY RUN` is available to inspect candidate deletions before destructive cleanup.

### Important boundaries

Timestamp-based time travel depends on transaction-log file timestamps. Delta documents that copying an entire table directory to another location can break timestamp-based time travel if those timestamps change, while version-based time travel is unaffected by that specific issue.

A clone has independent history from its source; source version numbers cannot be assumed to exist in the clone.

`VACUUM` is storage reclamation, not logical rollback. Conversely, historical readability is not permanent merely because a transaction-log version once existed.

### Selection / integration criteria

Use version IDs rather than timestamps when a stable logical version identity is required across filesystem copies or transfers. Retention settings must be derived from reproducibility/audit requirements, maximum transaction duration, stream lag, and storage budget rather than copied from defaults without review.

Integration points include Spark batch/stream processing, reproducible ML jobs, audit/debug tooling, retention maintenance, and pipelines that persist the consumed Delta version with run metadata.

### Automation possibilities

Automation can record `DESCRIBE HISTORY`/version identity, pin jobs to `versionAsOf`, run `VACUUM DRY RUN`, and gate destructive cleanup on retention policy plus active-reader/stream constraints. AI-generated cleanup recommendations require deterministic review of the exact retention settings and affected versions/files.

## Apache Hudi 1.2.0

**Source scope:** Apache Hudi official documentation and Apache Hudi maintainer release page. Hudi 1.2.0 is identified as the latest release on the maintainer release page, released 2026-05-23 with an announcement dated 2026-06-07.

### Verified semantics

Hudi records table actions on a timeline. Current documentation describes the timeline as the source of truth for table state and records requested, inflight, and completed action states.

Hudi supports:

- point-in-time/time-travel queries with `as.of.instant` / SQL `TIMESTAMP AS OF`;
- incremental queries over changes between commit instants;
- CDC queries that can expose changed records with before/after images and operation information when configured appropriately.

Hudi uses multiple file versions to provide snapshot isolation and historical reads. Its cleaning service reclaims older file slices and is enabled automatically by default for Spark-based writing.

Current cleaning policies include:

- `KEEP_LATEST_COMMITS` (default);
- `KEEP_LATEST_FILE_VERSIONS`;
- `KEEP_LATEST_BY_HOURS`.

The documentation explicitly ties retained commits to how much history remains available for incremental queries and warns that retention must protect files used by long-running queries.

### Important boundaries

Hudi **cleaning** and **timeline archival** are different mechanisms. Cleaning removes old file slices; archival controls how many instants remain in the active timeline. Neither should be interpreted as a generic application rollback mechanism.

Incremental query semantics return records changed within a commit range, while CDC can expose before/after images and operations. These are not interchangeable evidence products.

### Selection / integration criteria

Use Hudi when its timeline, incremental/CDC query model, and supported engines match the workload. Size cleaning retention against long-running readers and required incremental-history windows rather than assuming the default commit count is sufficient.

Integration points include Spark/Flink ingestion, downstream incremental consumers, CDC pipelines, cleaner/archival maintenance, and reproducibility metadata that preserves the exact instant boundaries used by a job.

### Automation possibilities

Automation can pin time-travel reads to explicit instants, track begin/end instants for incremental jobs, monitor cleaner retention, and validate that planned cleanup does not violate reader or downstream-history requirements. AI can assist with diagnosing timeline/retention configuration but should not independently shorten retention without policy and workload evidence.

## Cross-format decision rules

Do not normalize the three formats to a single generic `version` abstraction without preserving native identity and retention semantics.

| Concern | Iceberg | Delta Lake | Hudi |
|---|---|---|---|
| Historical identity | snapshot ID / timestamp / tag / branch | transaction-log version / timestamp | timeline instant / timestamp |
| Named branches/tags | verified | not established by sources reviewed here | not established by sources reviewed here |
| Incremental/change read in this baseline | engine/table history mechanisms exist but not evaluated as equivalent to Hudi CDC | streaming/change capabilities exist, but not evaluated here as equivalent to Hudi CDC | incremental query + CDC explicitly documented |
| History cleanup | snapshot expiration + ref retention | log/data retention + `VACUUM` | cleaner + timeline archival |
| Main retention hazard | expiring snapshots/references needed for reproducibility | `VACUUM` or log cleanup makes versions unreadable | cleaning file slices too aggressively breaks long reads/history windows |

Selection should be driven by the required history identity, engine/catalog compatibility, mutation/streaming model, retention guarantees, operational maintenance, and reproducibility/audit requirements. No performance superiority claim is made here; that requires independent workload-specific benchmarking.

## Contradiction / deduplication pass

- **Snapshot/time travel ≠ correctness.** Historical readability says which state was read, not whether it was valid.
- **Retention ≠ backup.** None of the reviewed history mechanisms is treated as a substitute for independently governed backup/disaster recovery.
- **History cleanup ≠ rollback.** Expiration/VACUUM/cleaning reclaim historical storage; they do not undo arbitrary external side effects.
- **Version IDs are format-specific.** Iceberg snapshot IDs, Delta versions, and Hudi instants must not be cross-mapped by name alone.
- **Timestamp semantics are not assumed identical.** Delta explicitly documents filesystem-timestamp sensitivity; Iceberg and Hudi use their own snapshot/timeline rules.
- **Existing `data-versioning-lineage.md` is not duplicated.** That file covers DVC/lakeFS/OpenLineage; this file covers transactional lakehouse table-history semantics.

## Unresolved

- Exact cross-engine compatibility matrices for every current Iceberg/Delta/Hudi feature were not exhaustively enumerated.
- Cross-format equivalence of CDC/change-feed semantics is unresolved and should be researched separately.
- Retention settings appropriate for a particular production workload require measured query duration, stream lag, audit/reproducibility requirements, and storage constraints.
- No independent benchmark was reviewed in this run; performance comparisons remain unresolved.
- AI systems with independently verified authority to modify production lakehouse retention/promotion policy were not established.

## Sources

Verified 2026-08-20.

1. Apache Iceberg, **Branching and Tagging**, official documentation: https://iceberg.apache.org/docs/latest/branching/
2. Apache Iceberg, **Spark Queries / Time Travel**, official documentation: https://iceberg.apache.org/docs/latest/spark-queries/
3. Apache Iceberg, **Specification — Snapshot References / Point in Time Reads**, official specification: https://iceberg.apache.org/spec/
4. Apache Iceberg, **Releases**, official project/maintainer record: https://github.com/apache/iceberg/blob/main/site/docs/releases.md
5. Delta Lake, **Table batch reads and writes — time travel / data retention**, official documentation: https://docs.delta.io/delta-batch/
6. Delta Lake, **Table utility commands — VACUUM**, official documentation: https://docs.delta.io/delta-utility/
7. Delta Lake, **Releases**, maintainer repository: https://github.com/delta-io/delta/releases
8. Apache Hudi, **Spark Quick Start — Time Travel / Incremental Query**, official documentation: https://hudi.apache.org/docs/quick-start-guide/
9. Apache Hudi, **Cleaning**, official documentation: https://hudi.apache.org/docs/cleaning/
10. Apache Hudi, **SQL Queries — Time Travel / CDC**, official documentation: https://hudi.apache.org/docs/next/sql_queries/
11. Apache Hudi, **Releases**, maintainer repository: https://github.com/apache/hudi/releases
