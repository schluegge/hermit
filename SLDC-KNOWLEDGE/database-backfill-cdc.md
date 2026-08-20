# Large-scale backfills and CDC-assisted database migration

Verification date: 2026-08-20

This document extends the database-evolution baseline with primary evidence for long-running data backfills and change-data-capture (CDC) migration bridges. It does not redefine schema expand/contract or engine-specific online-DDL semantics already owned by `zero-downtime-database-evolution.md`.

## 1. Baseline definition and SDLC role

Large-scale database evolution often requires two different mechanisms that must not be conflated:

1. **Backfill:** migrate or recompute historical rows over time, normally in bounded, restartable batches.
2. **CDC bridge:** capture source changes while an initial copy or snapshot is in progress so a downstream target can converge toward current source state before cutover.

Neither mechanism proves zero downtime by itself. A safe rollout still requires application/schema compatibility, bounded resource use, measurable progress, data validation, and explicit cutover/recovery criteria.

## 2. Large-scale resumable backfills — GitLab batched background migrations

GitLab's current maintainer documentation provides concrete implementation evidence for large data migrations that exceed normal migration time limits.

### Verified behavior

GitLab states that batched background migrations should be used for data migrations that would exceed regular migration time limits, including high-traffic tables and large datasets. It explicitly says **not** to use this mechanism for schema migrations.

The framework:

- queues data work separately from the schema migration;
- executes work in batches through background workers;
- expects jobs to be small and idempotent because retries can occur;
- can split timeout-failing jobs into smaller batches;
- adjusts batch size from recent execution performance;
- evaluates database health after jobs and can put a migration on hold;
- uses health indicators including pending WAL archival, active autovacuum on affected tables, Patroni Apdex/SLO degradation, and WAL-rate thresholds;
- keeps long-running migration code isolated from ordinary application models because newer application versions can deploy while a migration is still running;
- requires an explicit completion/finalization gate before later code may assume that 100% of the data has been migrated.

GitLab's current documentation recommends cursor-based iteration for new batched background migrations and supports composite cursor keys. It also documents re-queue procedures when a prior migration was buggy, became invalidated by later application behavior, or used a batch size that caused failure.

### Selection and integration implications

A general backfill framework should be evaluated for:

- deterministic cursor/range partitioning;
- idempotent retry semantics;
- persistent progress state;
- bounded batch/sub-batch size;
- automatic or operator-controlled throttling;
- health signals tied to the actual database topology;
- completion/finalization evidence before dependent cleanup or feature activation;
- isolation from application code that may change during the backfill;
- observability of failed, retried, paused, completed, and re-queued work.

GitLab is a concrete production implementation, not evidence that its exact thresholds or health indicators are universally correct for other systems.

### Source

- Source type: official maintainer documentation.
- GitLab batched background migrations, verified 2026-08-20: https://docs.gitlab.com/development/database/batched_background_migrations/

## 3. CDC plus incremental snapshotting — Debezium

Debezium's current 3.4 documentation provides a different mechanism: CDC streams ongoing source changes, while ad hoc incremental snapshots can re-read existing table contents in chunks during runtime.

### Verified behavior

Debezium documents that incremental snapshots:

- divide tables into configurable chunks rather than reading the entire table in one blocking snapshot;
- can be triggered while a connector is already streaming changes;
- use signaling plus a watermarking mechanism for supported connectors to reconcile snapshot rows with concurrently captured change events;
- can be scoped to selected tables and, for supported connectors, filtered subsets;
- can be stopped, paused, and resumed through signals;
- are available across multiple connectors including Db2, MySQL/MariaDB, MongoDB, Oracle, PostgreSQL, and SQL Server, with connector-specific prerequisites and caveats.

The PostgreSQL connector documentation additionally distinguishes **incremental** snapshots from **blocking** snapshots: a blocking snapshot temporarily stops streaming, whereas an incremental snapshot proceeds in chunks while change capture continues.

### Selection and integration implications

CDC-assisted backfill/snapshotting requires evidence for:

- source-log retention long enough to cover migration lag and interruptions;
- connector-specific snapshot and signaling support;
- a stable row key or supported surrogate-key strategy for chunking;
- deduplication/watermark semantics for overlap between snapshot data and streamed changes;
- downstream idempotency and ordering expectations;
- measurable source/consumer lag;
- source load created by snapshot scans and CDC reads;
- validation that the downstream target converged before cutover.

Debezium incremental snapshots are not a schema-migration engine and do not by themselves prove target equivalence or application cutover safety.

### Sources

- Source type: official Debezium documentation.
- Debezium 3.4 signaling and ad hoc snapshot actions, verified 2026-08-20: https://debezium.io/documentation/reference/3.4/configuration/signalling.html
- Debezium stable PostgreSQL connector snapshots/incremental snapshots, verified 2026-08-20: https://debezium.io/documentation/reference/stable/connectors/postgresql.html

## 4. Full-load + CDC migration bridge — AWS Database Migration Service

AWS DMS independently corroborates the full-copy-plus-change-stream migration pattern with different implementation and operational constraints.

### Verified behavior

AWS documents three migration modes including **full load + CDC** and **CDC only**. In full-load-plus-CDC mode, DMS captures changes while the initial data load is running, applies cached changes after the initial load, and then continues ongoing replication. CDC-only can be paired with a separate bulk-load mechanism.

AWS explicitly states that DMS CDC is **not real-time replication** and provides no SLA for CDC latency. Documented latency factors include source workload/transaction-log rate, transaction size, network conditions, replication-instance capacity, and target ingestion capacity.

AWS also documents important consistency and scaling boundaries:

- transactional consistency is maintained within a DMS task, so tables participating in common transactions should not be split across independent tasks without accounting for that boundary;
- parallel full-load settings multiply resource usage and can exhaust task memory;
- source full-load operations perform table scans and CDC tasks add source-log/change-capture load;
- a configurable transaction-consistency timeout can allow full load to begin even while source transactions remain open after the timeout;
- rapid DDL/DML/DDL sequences during CDC can produce incorrect parsing, data loss, or unexpected behavior for supported DDL replication paths; AWS advises allowing each DDL change to apply before subsequent operations;
- DMS data validation exists for source-target comparison, including CDC-aware validation, and should be treated as a separate evidence plane from replication status.

### Cutover implication

AWS's documented full-load-plus-CDC flow reaches a steady state, after which an application can be stopped, remaining changes allowed to flow, and the application restarted against the target. This is evidence for a migration bridge that reduces the cutover window; it is **not** evidence for a universally zero-downtime cutover or zero replication lag.

### Sources

- Source type: official AWS documentation.
- AWS DMS ongoing replication / CDC, verified 2026-08-20: https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Task.CDC.html
- AWS DMS components and full-load-plus-CDC cutover flow, verified 2026-08-20: https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.Components.html
- AWS DMS best practices and CDC latency/transactional boundaries, verified 2026-08-20: https://docs.aws.amazon.com/dms/latest/userguide/CHAP_BestPractices.html
- AWS DMS full-load task settings, verified 2026-08-20: https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Tasks.CustomizingTasks.TaskSettings.FullLoad.html
- AWS DMS supported DDL during CDC and rapid-DDL caveat, verified 2026-08-20: https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Introduction.SupportedDDL.html
- AWS DMS data validation, verified 2026-08-20: https://docs.aws.amazon.com/dms/latest/userguide/CHAP_Validating.html

## 5. Cross-mechanism selection criteria

Select a backfill/CDC strategy against the following evidence, not product labels:

1. whether the task is schema evolution, historical-data transformation, source-to-target replication, or a combination;
2. total row/data volume and live write rate;
3. row-key/cursor/chunking stability;
4. idempotency and retry behavior;
5. progress persistence and resume semantics;
6. source DB health and resource budgets;
7. source-log retention and CDC lag budget;
8. transactional consistency boundary across tables/tasks;
9. duplicate/order reconciliation between snapshot/backfill and live changes;
10. target validation and convergence criteria;
11. explicit completion/finalization before contract/destructive cleanup;
12. cutover, abort, forward-fix, and rollback/recovery procedures.

## 6. Integration and AI-driven automation possibilities

A bounded automated pipeline can:

- classify work into schema change, batched historical-data migration, CDC bridge, or mixed migration;
- generate candidate cursor/chunk plans and estimate workload from production-like statistics;
- execute idempotent batches while recording cursor/progress state;
- throttle or pause work on measured database-health signals;
- monitor CDC source/target latency and source-log retention margin;
- verify task-level transactional boundaries before splitting work for parallelism;
- run source-target validation and record mismatches separately from replication health;
- block contract/destructive cleanup until the backfill is explicitly complete and target validation passes;
- preserve batch sizes, retry counts, health signals, CDC positions/lag, validation results, migration versions, and cutover evidence.

AI can assist with migration classification, batch-plan generation, anomaly interpretation, SQL/code review, test generation, and candidate remediation. AI-generated plans or fixes remain untrusted until deterministic progress, health, consistency, validation, and cutover gates succeed.

## 7. Contradiction and deduplication pass

- `zero-downtime-database-evolution.md` remains the owner of expand/contract and engine-specific online-DDL semantics; this file owns long-running data movement/backfill and CDC-assisted convergence.
- GitLab batched background migrations are for data migrations, not schema migrations.
- Debezium incremental snapshotting is CDC/snapshot infrastructure, not a database schema migration framework.
- AWS DMS full-load-plus-CDC reduces cutover work but AWS explicitly says CDC is not real-time and offers no latency SLA.
- Parallelism can improve throughput while weakening or changing consistency boundaries if related tables are split across tasks; throughput and correctness are therefore separate decision axes.
- A completed snapshot, backfill, or replication task is not source-target equivalence evidence without validation.
- CDC does not remove the need for compatible schema/application sequencing when both old and new versions overlap.

No primary-source contradiction was found among the claims written here. Apparent differences are retained as product-specific semantics rather than normalized into a false common guarantee.

## 8. Residual unresolved frontier

Still unresolved or only partially represented:

- quantitative lock/resource/lag budgets that can be generalized across engines and workloads;
- replication and failover behavior during live schema changes beyond product-specific documented cases;
- CDC-assisted dual-write cutovers with independently verified reconciliation/rollback procedures;
- additional backfill/online-schema systems such as engine-native or distributed-SQL implementations;
- direct AI systems with independently evidenced authority to execute production backfills or cutovers and deterministic safety boundaries.
