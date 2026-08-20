# Zero-downtime database schema evolution

Verification date: 2026-08-20

This document extends the existing database-migration baseline with evidence for backward-compatible schema evolution while old and new application versions can overlap. It does not redefine generic migration history, validation, undo, or repair semantics already documented in `release-safety-flags-database-nonk8s.md`.

## 1. Baseline definition and SDLC role

Zero-downtime schema evolution is not a property of a migration tool alone. It is a deployment pattern in which database changes, application behavior changes, data backfill, and destructive cleanup are sequenced so that supported old/new application versions remain compatible with the database state during rollout.

The primary cross-engine pattern verified in current documentation is **expand -> migrate behavior/data -> contract**:

1. **Expand:** introduce new schema without removing the old representation.
2. **Migrate behavior/data:** deploy code that can coexist with both representations, dual-write or otherwise bridge them where needed, backfill historical data, then switch reads/writes.
3. **Contract:** remove the obsolete representation only after old application versions are no longer using it.

This pattern reduces compatibility risk but does not prove that an individual DDL operation is lock-free, instant, cheap, reversible, or safe for every engine/version.

## 2. Cross-engine implementation evidence — Redgate Flyway

### Scope

Redgate's current Flyway production-fleet guidance, last updated 2026-05-13, explicitly requires forward-compatible schema changes during mixed-version rollout and names the expand/contract pattern.

The documented sequence is:

- add new structure without removing the old;
- make new columns nullable or default-valued when needed for compatibility;
- update application behavior to write old and new forms and then read the new form;
- backfill historical data;
- remove the old structure only after application instances have moved to the new path.

The same guidance explicitly warns not to schedule expand and contract in the same release. It also states that renames, type changes, and adding `NOT NULL` to existing columns should follow this compatibility pattern.

Flyway's fleet tutorial adds a material engine caveat: transactional behavior differs by DBMS. Its documented example says failed transactional migrations on PostgreSQL, SQL Server, and Oracle can leave the target at the previous version, while MySQL/MariaDB DDL cannot be assumed to roll back in the same way; those changes should be designed to be small and individually recoverable.

### Selection and integration implications

- Migration tooling must preserve deterministic ordering and migration identity, but release design must additionally model application/schema compatibility across versions.
- A fleet or rolling deployment must account for targets and application instances being temporarily on different versions.
- Generated migration scripts still require review and production-like testing; generation is not correctness evidence.
- Drift checks and migration history are complementary to runtime compatibility testing.

### Sources

- Source type: official vendor documentation.
- Flyway production-fleet rollout / expand-contract guidance, updated 2026-05-13: https://documentation.red-gate.com/flyway/deploying-database-changes-using-flyway/rolling-out-updates-from-a-single-schema-to-multiple-production-databases
- Flyway fleet rollout tutorial, updated 2026-05-13: https://documentation.red-gate.com/flyway/deploying-database-changes-using-flyway/rolling-out-updates-from-a-single-schema-to-multiple-production-databases/tutorial-fleet-rollout-with-migrations-based-deployment
- Flyway supported databases/versions, updated 2026-07-27: https://documentation.red-gate.com/flyway/getting-started-with-flyway/system-requirements/supported-databases-and-versions

## 3. Concrete multi-release compatibility evidence — GitLab

GitLab's current development documentation provides implementation-level examples of avoiding downtime in its database migrations.

For dropping a column, GitLab documents a three-release sequence because running processes can still depend on cached schema information and destructive removal is difficult to roll back:

1. ignore the column in release M;
2. drop it in release M+1;
3. remove the ignore rule in release M+2.

For data-format migration, GitLab documents a staged approach in which a new column is added, existing data is copied, application code is deployed against the new representation, and remaining data is migrated afterward. The documentation explicitly states there is no one-size-fits-all solution.

This is independent corroboration of the compatibility principle, but it is GitLab-specific operational evidence rather than a universal recipe for every framework or database.

### Source

- Source type: official maintainer documentation.
- GitLab avoiding downtime in migrations, verified 2026-08-20: https://docs.gitlab.com/development/database/avoiding_downtime_in_migrations/

## 4. PostgreSQL 18 online-evolution primitives

Current PostgreSQL 18 documentation provides engine-specific primitives that can reduce blocking for particular schema operations.

### `CREATE INDEX CONCURRENTLY`

PostgreSQL documents that `CREATE INDEX CONCURRENTLY` builds an index without locks that prevent concurrent inserts, updates, or deletes. This is useful for production systems, but it has important caveats:

- it performs more work and can take longer than a standard index build;
- it waits on relevant transactions/snapshots;
- only one concurrent index build can run on a table at a time;
- it cannot run inside a transaction block;
- failure can leave an **invalid index** that must be cleaned up or rebuilt;
- partitioned-table handling has additional restrictions.

Therefore `CONCURRENTLY` means a different locking/concurrency profile, not "no operational impact".

### `NOT VALID` + `VALIDATE CONSTRAINT`

PostgreSQL documents that adding supported constraints with `NOT VALID` avoids the initial full-table validation scan. New rows are constrained while pre-existing rows can be validated later using `VALIDATE CONSTRAINT`. Validation uses a `SHARE UPDATE EXCLUSIVE` lock rather than a lock that blocks all concurrent updates.

This separates **constraint introduction** from **historical-data validation**, which can be useful in compatibility-first migration sequencing. It does not eliminate all locking or guarantee validation will succeed.

### Sources

- Source type: official PostgreSQL 18 documentation.
- `CREATE INDEX`, including `CONCURRENTLY`: https://www.postgresql.org/docs/current/sql-createindex.html
- `ALTER TABLE`, including `NOT VALID` / `VALIDATE CONSTRAINT`: https://www.postgresql.org/docs/current/sql-altertable.html

## 5. MySQL 8.4 online-DDL primitives

MySQL 8.4 InnoDB documents `ALGORITHM` and `LOCK` controls for online DDL, but support is **operation-specific**.

Examples from the current reference manual include:

- adding a secondary index can use an in-place operation while permitting concurrent DML;
- some column operations can use `ALGORITHM=INSTANT`;
- other operations rebuild the table even when concurrent DML is permitted;
- some operations do not permit concurrent DML at all;
- requesting `LOCK=NONE` or an incompatible `ALGORITHM` causes the statement to fail instead of silently satisfying an impossible concurrency request.

The failure-condition documentation also lists lock acquisition, disk-space requirements, online-log exhaustion, and concurrent writes that violate the new definition as possible reasons for online-DDL failure.

This is direct evidence against treating the label "online DDL" as synonymous with instant execution, zero locking, zero resource impact, or guaranteed success.

### Sources

- Source type: official Oracle/MySQL 8.4 reference documentation.
- InnoDB and Online DDL: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl.html
- Online DDL operations matrix: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-operations.html
- Online DDL failure conditions: https://dev.mysql.com/doc/refman/8.4/en/innodb-online-ddl-failure-conditions.html

## 6. SQL Server online and resumable DDL primitives

Current Microsoft documentation provides operation-specific online and resumable mechanisms for SQL Server, Azure SQL Database, Azure SQL Managed Instance, and related SQL services. These mechanisms reduce or bound maintenance disruption for supported operations; they do not make arbitrary `ALTER TABLE` statements nonblocking.

### Online index operations

Microsoft documents `ONLINE = ON` for supported index create/rebuild/drop operations and explicitly lists unsupported index types and other restrictions. Even when an index operation is online:

- the underlying table cannot be altered, truncated, or dropped while the operation is in progress;
- additional temporary/data-file space and version-store capacity can be required;
- deadlocks or uniqueness conflicts can still make the operation fail;
- some operations and data types cannot be performed online;
- online-index availability depends on SQL Server edition/version for on-premises deployments.

`WAIT_AT_LOW_PRIORITY` provides a bounded policy for lock acquisition during supported online index operations. Depending on the configured `ABORT_AFTER_WAIT`, the operation can continue waiting, abort itself, or terminate blocking user transactions. Therefore this setting is an explicit availability/authority decision and not merely a performance flag.

### Resumable index operations

For supported versions, `RESUMABLE = ON` together with `ONLINE = ON` allows index create/rebuild to pause and resume, including recovery after interruption or failover. Microsoft documents that a paused operation still consumes storage and requires both old and new index structures to be maintained by DML; update-heavy workloads can therefore degrade while the operation is paused.

### Online/resumable table constraints and online alter-column

Current `ALTER TABLE` documentation shows `ALTER COLUMN ... WITH (ONLINE = ON)` for supported SQL Server/Azure SQL versions. SQL Server 2022 and later also support resumable online addition of `PRIMARY KEY` and `UNIQUE` constraints with `RESUMABLE = ON`; Microsoft explicitly states that this resumable constraint capability does **not** cover foreign keys.

Generic `ALTER TABLE` still acquires schema-modification (`Sch-M`) locks for changes that require them. Online index operations may need a short `Sch-M` lock at completion. This is direct evidence that SQL Server "online" is operation-specific and can still include critical lock windows.

### Sources

- Source type: official Microsoft documentation.
- Guidelines for online index operations, current SQL Server documentation, verified 2026-08-20: https://learn.microsoft.com/en-us/sql/relational-databases/indexes/guidelines-for-online-index-operations?view=sql-server-ver17
- `ALTER TABLE` lock/online/resumable semantics, verified 2026-08-20: https://learn.microsoft.com/en-us/sql/t-sql/statements/alter-table-transact-sql?view=sql-server-ver17
- Resumable add table constraints, SQL Server 2022+ scope, verified 2026-08-20: https://learn.microsoft.com/en-us/sql/relational-databases/security/resumable-add-table-constraints?view=sql-server-ver17

## 7. Oracle AI Database 26 online table redefinition

Oracle AI Database 26 documents `DBMS_REDEFINITION` as an online table-redefinition mechanism for changing table structure and storage while preserving user access for most of the operation.

### Online redefinition workflow

The current administrator documentation exposes two main forms:

- `REDEF_TABLE` for supported single-step storage-property changes;
- the multi-procedure workflow using `CAN_REDEF_TABLE`, `START_REDEF_TABLE`, optional `SYNC_INTERIM_TABLE`, dependent-object handling, and `FINISH_REDEF_TABLE` for broader transformations.

During multi-step online redefinition, changes are synchronized between the original and interim table. Oracle documents that the original table is locked exclusively only for a small window near `FINISH_REDEF_TABLE`; the `dml_lock_timeout` parameter can bound how long the finish step waits for required locks before failing.

### Monitoring, restart and rollback

Oracle 26 exposes `V$ONLINE_REDEF` and `DBA_REDEFINITION_STATUS` for progress/status inspection, including restartability and errors. The documentation states that failed online redefinition can often be corrected and restarted from the last stopped point.

Oracle also documents an optional post-redefinition rollback path. When `enable_rollback => TRUE` is set during `START_REDEF_TABLE`, the system retains the interim structures needed to return the table to its original definition while preserving subsequent DML changes. This capability is opt-in; the default is false. It is not evidence that arbitrary application-side semantic changes, external side effects, or every schema transformation are automatically reversible.

### Limits and selection implications

- Candidate eligibility and redefinition method must be checked rather than assumed.
- Dependent objects and materialized views have explicit handling requirements and restrictions.
- Additional storage is needed for interim structures and synchronization.
- A short exclusive lock window still exists at finalization.
- Rollback semantics are specific to online table redefinition and do not replace application compatibility tests or backups/recovery planning.

### Sources

- Source type: official Oracle AI Database 26 documentation.
- Managing tables / online redefinition / rollback, verified 2026-08-20: https://docs.oracle.com/en/database/oracle/oracle-database/26/admin/managing-tables.html
- `DBMS_REDEFINITION` package reference, verified 2026-08-20: https://docs.oracle.com/en/database/oracle/oracle-database/26/arpls/DBMS_REDEFINITION.html
- `DBA_REDEFINITION_STATUS`, verified 2026-08-20: https://docs.oracle.com/en/database/oracle/oracle-database/26/refrn/DBA_REDEFINITION_STATUS.html
- `V$ONLINE_REDEF`, verified 2026-08-20: https://docs.oracle.com/en/database/oracle/oracle-database/26/refrn/V-ONLINE_REDEF.html

## 8. Selection criteria

For a zero-downtime database-evolution strategy, select and validate against:

1. application versions that may overlap during rollout;
2. read/write compatibility of each intermediate schema state;
3. target DBMS/version/edition and exact DDL concurrency semantics;
4. table size, write rate, replication/topology and lock-time sensitivity;
5. whether DDL is transactional or restartable on the target engine/operation;
6. data-backfill cost, batching, idempotency and restart behavior;
7. constraint/index creation and validation behavior;
8. migration-tool history/validation/drift capabilities;
9. destructive cleanup timing and proof that old code paths are gone;
10. recovery strategy: forward fix, application rollback, engine-specific resumable/rollback mechanism, snapshot/restore, or separately tested undo where safe.

Do not select an approach merely because a migration framework supports the target database. Framework compatibility and operation-level availability are different claims.

## 9. Integration and automation possibilities

A bounded automated pipeline can:

1. classify migrations as additive, behavioral/backfill, or destructive;
2. reject same-release expand+contract when the compatibility policy forbids it;
3. inspect target-engine/version/edition support for requested online/resumable-DDL options;
4. run migrations against a production-like dataset/topology;
5. test old-app/new-schema and new-app/intermediate-schema compatibility where rolling overlap is possible;
6. run backfills in resumable batches with measured progress and error counts;
7. verify new indexes/constraints/redefinitions are valid before switching behavior;
8. capture engine-specific operation status such as SQL Server resumable-index state or Oracle redefinition status;
9. gate contract/destructive cleanup on evidence that old application versions and old read/write paths are gone;
10. preserve migration ID/checksum, engine/version/edition, DDL algorithm/lock/resumable options, execution time, lock/wait evidence, validation results, backfill progress and application-compatibility test results.

AI can assist with migration-plan generation, change classification, SQL review, test generation, log/status interpretation, and candidate remediation. Generated output remains untrusted until the deterministic database and application gates above succeed.

## 10. Contradiction and deduplication pass

- Generic Flyway migrate/validate/repair/undo semantics already exist in `release-safety-flags-database-nonk8s.md`; they are not duplicated here.
- Flyway and GitLab support the expand/contract compatibility principle, but neither makes every DDL operation zero-impact.
- PostgreSQL's `CREATE INDEX CONCURRENTLY` reduces write blocking but can leave invalid indexes after failure and performs extra work.
- PostgreSQL `NOT VALID` defers validation; it does not mean the constraint is fully validated at creation time.
- MySQL's "online DDL" is operation-specific; some operations rebuild tables or disallow concurrent DML.
- SQL Server online/resumable support is operation-, version-, and sometimes edition-specific; supported operations can still require lock windows, space and version-store resources, and resumable pauses can affect DML throughput.
- Oracle `DBMS_REDEFINITION` allows DML for most of the workflow but still requires a short exclusive-lock window at finish; optional rollback is not a universal rollback mechanism for application state.
- Transactional/restart/rollback behavior cannot be generalized across engines.
- "Zero downtime" is therefore treated as an end-to-end compatibility/availability objective, not a boolean capability bit on a migration tool or DBMS.

No primary-source contradiction was found for the claims written in this revision. Apparent differences between engines are retained as scoped capabilities rather than normalized into a false cross-engine equivalence.

## 11. Residual unresolved frontier

The following remain unresolved or only partially represented:

- large-scale backfill frameworks and change-data-capture-assisted migrations;
- quantitative lock-time/resource budgets and automated abort thresholds across engines;
- replication/failover interactions during schema evolution beyond the restart/failover behavior explicitly documented for individual operations;
- additional engines such as Db2 and distributed/NewSQL systems;
- direct AI systems with authority to execute production database migrations and independently evidenced safety boundaries.
