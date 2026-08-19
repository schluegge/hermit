# SLO, error-budget and reliability-gate baseline

Verification date: 2026-08-20

This file adds a representative, evidence-backed baseline for using service-level objectives (SLOs), error budgets and burn-rate signals in release/deployment governance. It complements `release-deployment-progressive-delivery.md`: progressive-delivery controllers decide how a rollout advances, while this file focuses on the reliability evidence and policy that may authorize, pause, deny, or roll back change.

A green SLO/reliability gate is evidence only for the configured indicator, objective, window and policy. It is not proof that a release is correct or safe in every unmeasured dimension.

## 1. Baseline definition and SDLC role

A language-agnostic reliability-governance baseline separates at least these concepts:

1. **SLI (service-level indicator)** — a measured signal representing user-visible service behavior, such as availability or latency.
2. **SLO (service-level objective)** — a target for an SLI over a defined time window.
3. **Error budget** — the allowed unreliability implied by the SLO target; for a percentage objective it is commonly expressed as `100% - SLO target`.
4. **Burn rate** — how quickly the error budget is being consumed relative to the objective/window.
5. **Error-budget policy** — an agreed rule that maps SLO/error-budget state to actions such as reliability work, release freeze, review, or exception handling.
6. **Release/deployment gate** — an enforceable decision point in CI/CD or deployment control that consumes defined reliability evidence and produces an auditable allow/deny/pass/fail decision.
7. **Post-deployment rollback policy** — a rule that can revert a recent deployment when specified reliability conditions are breached after release.

These are related but not interchangeable. Measuring an SLO does not itself freeze deployments; an alert is not automatically an authorization gate; and a rollback trigger does not prove that the rollback restored service health.

## 2. Error-budget policy foundation — Google SRE

### Verified evidence

Google's published SRE Workbook example error-budget policy explicitly uses error-budget exhaustion to control releases. In the example, if a service exceeds its error budget over the preceding four-week window, changes/releases are halted except for specified high-priority or security exceptions until the service is back within its SLO. The Workbook also describes a production freeze as a mechanism that halts certain changes until sufficient error budget exists again.

The same material emphasizes stakeholder agreement on the SLO and error-budget policy. This is important because the release decision is a policy choice applied to measured reliability evidence, not an intrinsic property of the SLO calculation itself.

### Selection and integration criteria

An error-budget policy should define at minimum:

- the SLI and SLO target;
- the evaluation window and budgeting method;
- the threshold that changes release behavior;
- allowed exception classes and who can authorize them;
- how disputed/misclassified failures are handled;
- when normal release activity resumes;
- how the policy is reviewed and changed.

Do not copy Google's example thresholds mechanically. The Workbook presents an example policy, not a universal numeric standard.

### Source record

- Source: Google SRE Workbook, `Example Error Budget Policy`
- Source type: primary maintainer/publication
- URL: https://sre.google/workbook/error-budget-policy/
- Published scope: example policy published 2018-02-19
- Verified: 2026-08-20
- Caveat: canonical policy guidance, but the example's concrete thresholds/windows are illustrative rather than current product defaults or universal requirements.

- Source: Google SRE Workbook, `Implementing SLOs`
- Source type: primary maintainer/publication
- URL: https://sre.google/workbook/implementing-slos/
- Verified: 2026-08-20

## 3. SLOs as code — OpenSLO v1 and `oslo`

### Verified implementation

OpenSLO's official specification defines a vendor-agnostic `openslo/v1` YAML model with object kinds including `SLO`, `SLI`, `AlertPolicy`, `AlertCondition`, `AlertNotificationTarget`, `DataSource`, and `Service`. The SLO schema records time windows, budgeting method, objectives, indicators and alert policies. Alert conditions include burn-rate conditions with a threshold and lookback window.

The OpenSLO project also maintains the `oslo` CLI. Its documented `oslo validate -f ...` command validates OpenSLO YAML/JSON documents, and `oslo fmt` formats them. This provides a concrete CI/GitOps validation point for reliability policy definitions before runtime evaluation.

### SDLC role

SLO-as-code makes reliability intent versionable and reviewable alongside software/configuration. It can support pull-request review, schema validation, change history and policy ownership independently of the eventual monitoring vendor.

### Selection and integration criteria

Choose a declarative SLO format when portability, code review, version history or multi-vendor tooling matters. Validate syntax/schema in CI, but separately verify that the target runtime actually implements the selected data-source/query semantics. OpenSLO intentionally excludes platform-specific implementation details, so schema validity is not evidence that a referenced metric query is semantically correct in a particular backend.

### Automation possibilities

- validate SLO manifests in CI;
- format/deduplicate declarations deterministically;
- require code review for objective/window/policy changes;
- generate or synchronize implementation-specific SLO configuration where a verified adapter exists;
- reject malformed SLO policy before deployment configuration is applied.

### Source record

- Source: OpenSLO official specification repository
- Source type: primary specification repository
- URL: https://github.com/OpenSLO/OpenSLO
- Scope: `openslo/v1`; v2 is described separately as work in progress
- Verified: 2026-08-20

- Source: OpenSLO `oslo` CLI repository
- Source type: primary maintainer repository
- URL: https://github.com/OpenSLO/oslo
- Verified: 2026-08-20
- Caveat: repository currently lists v0.13.0 as its latest tagged release surfaced during verification; validation of OpenSLO syntax does not validate a monitoring backend's metric semantics.

## 4. Reliability signal implementation — Grafana SLO

### Verified implementation

Current Grafana SLO documentation defines targets and error budgets, exposes remaining error budget and burndown, and can generate burn-rate alert rules. Grafana documents fast- and slow-burn alert classes based on error-budget burn rate. Its current plugin documentation surfaced version `v1.94.0` as latest during this verification run.

Grafana also documents event-based and time-based SLI calculation. Event-based SLIs are recommended in most cases; Grafana cautions that time-based SLIs weight each time slice equally, so low-traffic failure intervals can have the same SLO impact as peak-traffic intervals.

### Important data-quality caveat

Grafana documents that newly created SLO recording rules do not backfill historical data. Some burndown/remaining-budget panels can therefore remain incomplete until an entire SLO window has elapsed. A release gate must not treat an uninitialized or partial SLO window as equivalent to healthy full-window evidence.

Grafana maintenance windows also intentionally omit generated SLI samples and do not backfill them later. A gate consuming those recording rules must preserve maintenance-window state and no-data semantics rather than silently interpreting missing samples as success.

### Selection and integration criteria

Record the exact SLI query, data source, objective, window, burn-rate rule, no-data semantics and initialization state. For release policy, prefer user-impacting signals over infrastructure-only proxies where feasible. Verify that maintenance and missing-data behavior cannot accidentally fail open.

### Automation possibilities

- generate SLO recording/alert rules;
- alert on fast/slow error-budget burn;
- expose SLO/budget state to an external deployment protection rule or policy engine;
- route breach evidence into incident/reliability workflows.

The last integration requires a separately verified consumer; Grafana SLO by itself is a measurement/alerting system, not proof that a deployment gate is enforced.

### Source record

- Source: Grafana SLO documentation
- Source type: official vendor documentation
- URL: https://grafana.com/docs/plugins/grafana-slo-app/latest/
- Scope observed: plugin docs `v1.94.0 (latest)`
- Verified: 2026-08-20

- Source: Grafana burn-rate notifications
- Source type: official vendor documentation
- URL: https://grafana.com/docs/plugins/grafana-slo-app/latest/set-up/configure-burn-rate-notifications/
- Verified: 2026-08-20

- Source: Grafana SLO troubleshooting
- Source type: official vendor documentation
- URL: https://grafana.com/docs/grafana-cloud/alerting-and-irm/slo/troubleshooting/
- Verified: 2026-08-20

- Source: Grafana SLO maintenance windows
- Source type: official vendor documentation
- URL: https://grafana.com/docs/grafana-cloud/observe-and-act/alert-and-measure-reliability/slo/maintenance-windows/
- Verified: 2026-08-20

## 5. Direct SLO-driven deployment governance — Harness SRM

### Verified implementation

Harness documents direct SLO-driven governance for pipelines. Its `SLO-Driven Governance` documentation states that OPA/Rego policies can prevent pipelines from deploying when an SLO limit is breached, an SLO is not configured for the monitored service, or the configured error budget is depleted. Example policy inputs include `sloErrorBudgetRemainingPercentage` and monitored-service SLO configuration state.

Harness also documents SLO-driven automated deployment rollback. A rollback policy can be added to an SLO error-budget policy; when the configured SLO notification condition is breached within the rollback window, Harness can roll back the specified environment/infrastructure deployment. The documentation requires correct environment/infrastructure configuration and instructs users to verify the resulting rollback.

This is direct evidence for two different control points:

- **pre/deployment governance** — reliability state can deny a pipeline/deployment;
- **post-deployment recovery** — reliability breach can trigger rollback of a recent deployment.

### Selection and integration criteria

For any SLO-driven enforcement implementation, preserve:

- monitored service and environment identity;
- SLO/SLI identity and target;
- error-budget state supplied to the policy;
- policy version and exact threshold;
- allow/deny result and policy evaluation evidence;
- exception/reset actor and reason, if supported;
- deployment/version identity;
- rollback window, rollback target and post-rollback health verification.

Error-budget reset/override must be privileged and auditable. Harness documents role control and reset history for error-budget resets; such resets change policy state and must not be treated as evidence that reliability improved.

### Automation possibilities

- block deployment when reliability policy fails;
- require SLO configuration before production deployment;
- deny deployment below a configured remaining-budget threshold;
- automatically roll back a recent deployment when an SLO condition breaches;
- notify responders on budget percentage, remaining minutes or burn-rate conditions.

### Source record

- Source: Harness `SLO-Driven Governance`
- Source type: official vendor documentation
- URL: https://developer.harness.io/docs/service-reliability-management/slo-driven-deployment-governance/
- Last-updated metadata observed: 2025-09-04
- Verified: 2026-08-20

- Source: Harness `Automated Deployment Rollbacks`
- Source type: official vendor documentation
- URL: https://developer.harness.io/docs/service-reliability-management/manage-slo/automated-deployment-rollback/
- Last-updated metadata observed: 2025-07-03
- Verified: 2026-08-20

- Source: Harness `Reset error budget`
- Source type: official vendor documentation
- URL: https://developer.harness.io/docs/service-reliability-management/manage-slo/reset-error-budget/
- Last-updated metadata observed: 2023-12-27
- Verified: 2026-08-20
- Caveat: reset behavior documented only for SLOs with Calendar time-period type on the inspected page.

## 6. Datadog SLO signals and Deployment Gates — verified boundary

### Verified implementation

Datadog currently documents:

- SLO error-budget alerts based on percentage of budget consumed;
- SLO burn-rate alerts based on sustained budget-consumption rate;
- SLO alerts as a Datadog monitor type;
- Deployment Gates, currently marked **Preview**, that evaluate one or more rules and return an asynchronous `pass` or `fail` result;
- Deployment Gate Monitor rules that fail if matching monitors are in `ALERT` or `NO_DATA`, with a configurable evaluation period.

Deployment Gates can automatically halt a release when configured monitor/APM evidence indicates a problem.

### Explicit unresolved integration claim

The inspected official documentation does **not** explicitly state that every Datadog `SLO Alert` monitor is supported as a Deployment Gate Monitor rule target, nor does it provide a documented SLO-alert-to-Deployment-Gate recipe. The two capabilities are compositionally compatible at the taxonomy level (`SLO Alert` is a monitor type; Deployment Gates consume monitor state), but direct compatibility was not independently verified in this run.

Therefore:

**Datadog SLO → Deployment Gate enforcement is recorded as `unresolved`, not as a verified direct SLO release gate.**

The independently verified facts remain useful: Datadog can generate SLO budget/burn-rate monitor signals, and Datadog Deployment Gates can enforce release decisions from supported monitor/APM rules.

### Source record

- Source: Datadog `SLO Alerts`
- Source type: official vendor documentation
- URL: https://docs.datadoghq.com/monitors/types/slo/
- Verified: 2026-08-20

- Source: Datadog `Error Budget Alerts`
- Source type: official vendor documentation
- URL: https://docs.datadoghq.com/service_level_objectives/error_budget/
- Verified: 2026-08-20

- Source: Datadog `Burn Rate Alerts`
- Source type: official vendor documentation
- URL: https://docs.datadoghq.com/service_level_objectives/burn_rate/
- Verified: 2026-08-20

- Source: Datadog `Deployment Gates`
- Source type: official vendor documentation
- URL: https://docs.datadoghq.com/deployment_gates/
- Product state observed: Preview
- Verified: 2026-08-20

- Source: Datadog `Set Up Deployment Gates`
- Source type: official vendor documentation
- URL: https://docs.datadoghq.com/deployment_gates/setup/
- Product state observed: Preview
- Verified: 2026-08-20

## 7. AI-assisted reliability response — bounded Harness AI SRE evidence

### Verified current capability

Harness documentation updated July/August 2026 describes a direct Harness SLO integration for AI SRE. SLO error-budget, remaining-budget and burn-rate notifications can be delivered through a generated AI SRE webhook integration. Harness AI SRE can route/enrich alerts, create incidents, associate or trigger runbooks, and its RCA Change Agent analyzes recent deployments, pull requests and change events to produce root-cause theories with confidence scores.

This supports AI-assisted incident/reliability response around SLO breaches. It does **not** establish that the AI agent should own the release authorization threshold or replace the deterministic SLO/error-budget policy. SLO-driven deployment allow/deny and rollback remain separately verifiable control mechanisms.

### Safe automation boundary

AI may:

- summarize and correlate SLO breach alerts;
- connect breaches with recent deployment/change evidence;
- produce ranked root-cause theories;
- route alerts/incidents and associate runbooks;
- assist responders with remediation context.

Release authorization should remain an explicit policy evaluation over versioned evidence. AI-generated theories or summaries are investigation inputs, not a substitute for the deterministic gate result or post-rollback verification.

### Source record

- Source: Harness `Harness SLO Integration` for AI SRE
- Source type: official vendor documentation
- URL: https://developer.harness.io/3k-docs/ai-sre/alerts/alerts/integrations/monitoring/harness-slo/
- Last-updated metadata observed: 2026-07-02
- Verified: 2026-08-20

- Source: Harness AI SRE overview / RCA Change Agent
- Source type: official vendor documentation
- URLs:
  - https://developer.harness.io/docs/ai-sre/get-started/overview/
  - https://developer.harness.io/3k-docs/ai-sre/ai-agent/rca-change-agent/
- Last-updated metadata observed: 2026-08-07 / 2026-07-02 respectively
- Verified: 2026-08-20

## 8. Language-agnostic release-gate evidence contract

For a decision-grade SLO/error-budget gate, preserve at least:

1. source commit and immutable release/artifact identity;
2. target service/environment identity;
3. SLI definition and exact query/data source;
4. SLO target, budgeting method and evaluation window;
5. error-budget/burn-rate calculation state;
6. no-data, maintenance and initialization semantics;
7. gate policy version and threshold(s);
8. decision result (`allow`/`deny`, `pass`/`fail`) with timestamp;
9. exception/reset state, actor, reason and authorization if applicable;
10. deployment revision and rollout status;
11. post-deployment SLO/service-health evidence;
12. rollback trigger, target and post-rollback verification when recovery occurs.

This contract is intentionally tool-neutral. A static site, backend service, mobile API, game backend, ML inference endpoint or fleet-management service may expose different SLIs, but the evidence chain remains auditable when the identities, queries, windows, policies and decisions are preserved.

## 9. Selection criteria

Choose SLO/error-budget release governance based on:

- whether the SLI reflects user experience rather than only infrastructure state;
- data completeness, latency and no-data behavior;
- rolling versus calendar window semantics;
- burn-rate versus absolute budget thresholds;
- ability to version/review policy as code;
- integration with CI/CD/deployment authorization;
- dry-run/shadow evaluation before enforcement;
- exception/override RBAC and audit history;
- post-deployment evaluation and rollback semantics;
- availability of immutable release/version correlation;
- vendor portability and declarative interfaces where required;
- explicit handling of maintenance windows and SLO corrections/resets.

## 10. Contradiction and deduplication results

- **SLO measurement ≠ release enforcement.** Grafana/Datadog can produce SLO/budget signals; a separately verified policy consumer is required to turn a signal into a deployment decision.
- **Alert ≠ gate.** Notification is evidence delivery, not deployment authorization.
- **Gate passed ≠ release correct.** Only configured indicators/policies were checked.
- **Budget reset/correction ≠ restored reliability.** Such operations alter accounting/policy state and require audit evidence.
- **Maintenance exclusion ≠ healthy traffic.** Excluded/no-data periods must not silently become proof of success.
- **Rollback triggered ≠ rollback succeeded.** Deployment and service health must be re-verified after rollback.
- **Google's example thresholds ≠ universal standard.** They are policy examples.
- **Datadog SLO Alert → Deployment Gate direct compatibility remains unresolved.** No unsupported composition claim was promoted to verified status.
- **AI investigation ≠ release authority.** AI-generated RCA/context is advisory evidence unless a separate deterministic policy explicitly authorizes action.
- Existing Kubernetes, Argo Rollouts, Flagger and GitHub environment-gate mechanics remain in `release-deployment-progressive-delivery.md`; they were not duplicated here.

## 11. Remaining unresolved expansion

- additional independent SLO/error-budget policy engines and observability stacks;
- direct verified SLO-to-deployment-gate integrations for Grafana and Datadog rather than only signal/gate building blocks;
- quantitative evaluation of false-positive/false-negative and delayed-metric behavior for reliability gates;
- release policy under multiple/conflicting SLOs and composite objectives;
- error-budget policy for batch, ML, mobile/offline, embedded and intermittently connected systems where request-based SLIs may not fit;
- automated promotion/rollback driven by app-store crash telemetry and fleet health signals;
- further AI-assisted reliability systems with explicit authority boundaries and deterministic verification outputs.
