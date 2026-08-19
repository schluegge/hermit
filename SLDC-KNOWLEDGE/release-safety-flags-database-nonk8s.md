# Release safety: feature flags, database migrations, and non-Kubernetes delivery

Verification date: 2026-08-19

This document extends the release/deployment baseline with three evidence planes that were previously unresolved: runtime feature-control and kill switches, database/schema migration safety, and a representative non-Kubernetes deployment system. These mechanisms are complementary. A feature rollback does not undo a database migration; a deployment rollback does not necessarily undo deployment-script side effects; and a database history repair is not proof that application behavior is healthy.

## 1. Runtime release control — feature flags and kill switches

### Baseline definition and SDLC role

Feature flags separate deployment of code from activation of behavior. Release flags can expose a new behavior incrementally; kill-switch/circuit-breaker flags provide an operational path to disable behavior without changing code or redeploying.

### Verified implementation — LaunchDarkly

Current LaunchDarkly documentation distinguishes release flags from kill-switch flags:

- release flags are temporary flags used for incremental rollout and are expected to be retired after the release is complete;
- kill-switch flags are normally permanent boolean operational controls used to shut off non-core functionality or third-party integrations during incidents;
- the flag toggle can act as a circuit breaker, disabling a flagged feature without a redeploy;
- percentage/progressive rollout behavior must be configured explicitly; creating a release flag alone does not start a rollout.

LaunchDarkly progressive rollouts increase the served percentage over configured time steps. The documentation explicitly states that ordinary progressive rollouts do not include metric monitoring. Guarded rollouts are a different mechanism: they monitor selected metrics for statistically significant regressions and can automatically roll back. Current guarded-rollout documentation also records minimum-context/sample requirements and automatic rollback behavior for regressions or sample-ratio mismatch.

### Selection criteria

Select a feature-control system based on SDK/platform coverage, server/client evaluation model, targeting semantics, audit history, approval controls, failure/default behavior, observability integration, and whether rollout decisions are time-based or metric-gated. Treat rollout and guardrail semantics as separate capabilities: a staged percentage increase without metric evaluation is not equivalent to a health-gated rollout.

### Integration and automation

CI/CD can deploy dormant code first, then activate it through a release flag. Operations systems can use permanent kill switches as bounded emergency controls. Metric-gated systems can pause or reverse exposure when explicitly configured guardrails fail. Preserve flag version/configuration, environment, rollout schedule, target context, metric definition/version, decision result, actor/automation identity, and final served variation.

### Limits

- Turning off a feature changes runtime exposure; it does not remove the deployed artifact.
- A feature rollback does not undo database/schema changes, external side effects, or messages already emitted.
- A time-based progressive rollout is not automatically a health-gated rollout.
- Automatic rollback is only as complete as the monitored metrics and the rollback scope. LaunchDarkly documents that rolling back a prerequisite flag does not automatically roll back dependent flags.

### Sources

- LaunchDarkly kill-switch flags: https://launchdarkly.com/docs/home/flags/killswitch
- LaunchDarkly release flags: https://launchdarkly.com/docs/home/flags/release
- LaunchDarkly progressive rollouts: https://launchdarkly.com/docs/home/releases/progressive-rollouts
- LaunchDarkly creating/managing progressive rollouts: https://launchdarkly.com/docs/home/releases/create-progressive-rollouts
- LaunchDarkly guarded rollouts: https://launchdarkly.com/docs/home/releases/guarded-rollouts
- LaunchDarkly managing guarded rollouts: https://launchdarkly.com/docs/home/releases/managing-guarded-rollouts

## 2. Database/schema migration safety

### Baseline definition and SDLC role

A database migration changes persistent state or schema and therefore has failure modes that differ from stateless application deployment. A representative baseline needs versioned change artifacts, deterministic ordering, migration history, validation against expected migration state, explicit handling of destructive/non-transactional changes, and an independently verified recovery strategy.

### Verified implementation — Redgate Flyway

Current Flyway documentation defines migrations as version-controlled incremental database changes that are applied consistently across environments. `migrate` compares available migrations with those recorded in the schema history and applies the missing changes.

`validate` checks applied migrations against the available migration set and fails for conditions including changed names/types/checksums, migrations applied in the database that are no longer resolved locally, and locally resolved migrations that have not been applied. Current documentation states that SQL migration checksums are recorded when migrations run and later compared during validation.

`repair` repairs the schema history table. Current documentation explicitly warns that failed-migration user objects may require manual cleanup, and that repair can realign checksums/descriptions/types or mark missing migrations as deleted. Therefore `repair` is a history-maintenance operation, not proof that a partially applied migration left no side effects.

Flyway also supports optional undo migrations in the Teams edition. Its current undo documentation warns that destructive changes such as drop/delete/truncate require special care and that undo assumes the corresponding migration completed successfully. That is material evidence against treating generic rollback as universally safe.

### Selection criteria

Select migration tooling based on target database support, migration-history model, transaction behavior of the target database/DDL, validation semantics, repeatable/idempotent migration support, drift detection, deployment ordering, rollback/undo model, observability, and ability to test against production-like data/scale. Recovery policy must account for data-loss risk and compatibility between old/new application versions and old/new schemas.

### Integration and automation

A deterministic pipeline can:

1. version-control migration artifacts;
2. lint or statically inspect them where supported;
3. apply them to an isolated/representative database;
4. run `validate` and application compatibility tests;
5. capture schema/history state;
6. gate production execution on explicit environment and artifact identity;
7. re-run validation and application-level checks after migration;
8. use an explicitly designed undo, snapshot restore, or forward-fix path when recovery is required.

Automation must not infer that a failed migration is cleanly reversible. Recovery should be tested independently for destructive or non-transactional changes.

### Limits

- `validate` proves consistency with Flyway's migration metadata model, not application correctness or semantic data correctness.
- `repair` changes migration history metadata and may require manual cleanup of database objects.
- Undo availability does not make every migration safely reversible.
- A schema rollback can itself be unsafe after new application versions have written data in a new format.

### Sources

- Flyway migrations: https://documentation.red-gate.com/flyway/flyway-concepts/migrations
- Flyway `migrate`: https://documentation.red-gate.com/flyway/reference/commands/migrate
- Flyway `validate`: https://documentation.red-gate.com/flyway/reference/commands/validate
- Flyway `repair`: https://documentation.red-gate.com/flyway/reference/commands/repair
- Flyway undo migrations: https://documentation.red-gate.com/flyway/flyway-concepts/migrations/undo-migrations

## 3. Representative non-Kubernetes delivery — AWS CodeDeploy

### Baseline definition and SDLC role

A non-Kubernetes delivery system can still implement staged traffic shifting, health constraints, rollback policy, and deployment auditability. The baseline requirement is behavioral rather than orchestration-specific: identify the target set, constrain unavailable capacity/traffic exposure, observe health, and preserve a known recovery revision.

### Verified implementation — AWS CodeDeploy

Current AWS CodeDeploy documentation supports EC2/on-premises, Lambda, and ECS compute platforms with different deployment semantics.

For EC2/on-premises, deployment configurations can constrain the minimum number or percentage of healthy hosts. CodeDeploy supports in-place deployments and, for supported targets, blue/green deployment models.

For Lambda and ECS, AWS documents canary, linear, and all-at-once traffic shifting. Custom canary/linear configurations can specify the traffic percentage and interval. AWS also documents CloudWatch alarm integration and automatic rollback when a deployment fails or a configured monitoring threshold is met.

CodeDeploy rollback semantics are important: for several compute platforms, rollback is implemented as a new deployment/redeployment of a previously known revision, with a new deployment ID. AWS explicitly warns for EC2/on-premises that CodeDeploy does not automatically revert arbitrary side effects performed by deployment scripts. This prevents a false assumption that artifact rollback necessarily restores complete machine/application state.

### Selection criteria

Select a non-Kubernetes deployment system based on target compute support, in-place versus blue/green needs, traffic-shift controls, minimum-health semantics, alarm integration, artifact/revision identity, deployment hooks, rollback mechanics, auditability, and the side effects introduced by lifecycle scripts.

### Integration and automation

Automation can create a deployment with a pinned revision, use health/traffic-shift policy, observe deployment status and alarms, and automatically redeploy the last known good revision on configured failure. Preserve deployment ID, revision/artifact identity, target group, deployment configuration, alarm results, lifecycle-hook results, and rollback deployment ID.

### Limits

- A rollback can be a new deployment rather than restoration of prior host state.
- Deployment scripts can create side effects that the deployment service does not automatically reverse.
- A healthy-host or traffic-shift rule is not proof of business-level correctness.
- Provider-specific rollout modes must not be generalized to unsupported targets; AWS documents different semantics for EC2/on-premises, Lambda, and ECS.

### Sources

- AWS CodeDeploy deployment configurations: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-configurations.html
- AWS CodeDeploy deployment overview: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments.html
- AWS CodeDeploy rollback/redeploy: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployments-rollback-and-redeploy.html
- AWS CodeDeploy advanced deployment-group options: https://docs.aws.amazon.com/codedeploy/latest/userguide/deployment-groups-configure-advanced-options.html

## 4. Cross-plane release-safety baseline

A release that combines application artifacts, flags, and database changes should preserve separate evidence for:

1. immutable application artifact/revision;
2. database migration set and pre/post migration state;
3. migration validation result and recovery plan;
4. deployment target and rollout configuration;
5. deployment health/status and service-level checks;
6. feature-flag configuration/version and exposure state;
7. metric/guardrail definitions when rollout is health-gated;
8. rollback target for application deployment;
9. rollback/forward-fix strategy for database state;
10. kill-switch behavior and known residual side effects;
11. actor/automation identity and timestamps.

The safest general rule supported by these implementations is to avoid collapsing distinct rollback planes into one label. `rollback application`, `disable feature`, and `restore/forward-fix database` are separate operations with different evidence and failure modes.

## 5. Contradiction and deduplication notes

- Existing `release-deployment-progressive-delivery.md` already covers Kubernetes, GitHub environment gates, Argo Rollouts and Flagger; those claims are not duplicated here beyond integration boundaries.
- LaunchDarkly ordinary progressive rollouts are time/percentage based and explicitly lack the metric monitoring available to guarded rollouts.
- Flyway `repair` must not be represented as application/data recovery; its documented role is schema-history repair and it can leave user-object cleanup to the operator.
- AWS CodeDeploy automatic rollback must not be represented as complete state restoration because deployment-script side effects can persist.

## 6. Remaining unresolved expansion

- desktop/mobile app-store phased release and rollback semantics;
- firmware/device-fleet staged rollout and recovery;
- additional independent feature-flag implementations and interoperability/standardization evidence;
- database expand/contract and zero-downtime migration patterns backed by primary implementation evidence across multiple database engines;
- SLO/error-budget-driven release gates across additional observability systems;
- verified AI systems with release-specific authority boundaries beyond CI/CD diagnosis and patch generation.
