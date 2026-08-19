# Release, deployment, rollback and progressive-delivery baseline

Verification date: 2026-08-19

This file adds a representative, evidence-backed baseline for release/deployment control, rollout verification, rollback, and progressive delivery. It complements CI/CD, security, supply-chain, and observability material elsewhere in `SLDC-KNOWLEDGE`. A successful deployment command, a green CI pipeline, or an AI-generated remediation is not treated as proof that a production release is healthy.

## 1. Baseline definition and SDLC role

A release/deployment system moves a versioned artifact and its configuration into an execution environment under explicit policy. A robust baseline separates at least five evidence planes:

1. **pre-deployment authorization/policy** — whether this change is allowed to enter an environment;
2. **deployment execution** — applying the desired artifact/configuration;
3. **rollout state verification** — whether the orchestrator reached the intended state;
4. **service-level validation** — whether the deployed version satisfies health, correctness, latency, error-rate, or business criteria;
5. **rollback/recovery evidence** — whether a failed or degraded release can be returned to a known acceptable state and that recovery is itself verified.

These planes are related but not interchangeable. For example, `kubectl rollout status` verifies rollout completion state, not application correctness; a deployment protection rule authorizes execution, but does not prove the deployed workload is healthy.

## 2. Kubernetes rollout execution, status and rollback

### Verified implementation

Current Kubernetes documentation (modified March 22, 2026 for the generated `kubectl rollout` reference) defines `kubectl rollout` for Deployments, DaemonSets, and StatefulSets. Supported subcommands include history, pause, restart, resume, status, and undo.

For Deployments, Kubernetes documents:

- `kubectl rollout history deployment/<name>` to inspect revisions;
- `kubectl rollout status deployment/<name>` to watch rollout completion;
- `kubectl rollout undo deployment/<name>` to return to the previous revision;
- `kubectl rollout undo deployment/<name> --to-revision=N` for a selected revision;
- a follow-up `kubectl rollout status` to verify the rollback completes.

The current `rollout status` reference also documents `--revision=N`, which is important when automation must pin verification to one revision rather than silently following a newer rollout that starts concurrently.

### Selection and integration criteria

For automated deployment verification, preserve the artifact/image digest, desired revision, environment/cluster identity, deployment command result, and rollout-status result. Pin rollout observation to the intended revision when concurrent changes are possible. Treat orchestrator completion as a deployment-state check only; add application-specific acceptance and telemetry gates separately.

### Automation possibilities

CI/CD can apply manifests, wait for the intended revision, record rollout history/status, and initiate a rollback on explicit failure conditions. A rollback should be followed by the same rollout-status and service-level validation used for forward deployment. Automation should fail closed when the target revision or environment cannot be unambiguously established.

### Sources

- Kubernetes `kubectl rollout` reference: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/
- Kubernetes `kubectl rollout status`: https://kubernetes.io/docs/reference/kubectl/generated/kubectl_rollout/kubectl_rollout_status/
- Kubernetes update/rollback task: https://kubernetes.io/docs/tasks/run-application/update-deployment-rolling/

## 3. Pre-deployment environment gates — GitHub Actions Environments

### Verified implementation

Current GitHub Actions documentation defines deployment protection rules for jobs that reference an environment. Verified controls include:

- required reviewers;
- optional prevention of self-review;
- wait timers;
- branch/tag deployment restrictions;
- custom deployment protection rules backed by GitHub Apps.

GitHub explicitly describes custom protection integrations with systems such as observability, change-management, and code-quality systems to decide whether a deployment may proceed.

### Selection and integration criteria

Use environment gates for authorization and readiness policy, not as a substitute for post-deployment verification. Record which environment protections were active for the deployment. Where custom protection rules depend on an external evidence provider, preserve the provider result and failure semantics so a missing/unreachable gate cannot be mistaken for approval.

### Automation possibilities

Release pipelines can require human approval for high-risk environments, delay releases with wait timers, restrict deployment refs, or query external readiness systems before secrets are exposed and deployment jobs run. Policy should distinguish manual authorization from machine-verifiable readiness; neither alone proves production health.

### Sources

- GitHub deployments and environments: https://docs.github.com/en/actions/reference/workflows-and-actions/deployments-and-environments
- GitHub deploying with Actions: https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/control-deployments
- GitHub reviewing deployments: https://docs.github.com/en/actions/how-tos/deploy/configure-and-manage-deployments/review-deployments

## 4. Progressive delivery — Argo Rollouts

### Verified implementation

Argo Rollouts' current documentation describes `Rollout` as a Kubernetes Deployment replacement with BlueGreen and Canary strategies. `AnalysisTemplate`/`AnalysisRun` can execute metrics-based analysis during delivery and determine whether progression continues or aborts.

For BlueGreen, post-promotion analysis can run after traffic switches to the new version. If the analysis fails or errors, the Rollout enters an aborted state and traffic is switched back to the previous stable ReplicaSet. For canary/blue-green rollback, Argo Rollouts also documents a rollback-window mechanism that can fast-track selected recent revisions rather than replaying all rollout steps.

### Selection and integration criteria

Select progressive-delivery tooling based on supported traffic-routing mechanism, analysis providers, failure/inconclusive semantics, rollback behavior, auditability, and interaction with GitOps/deployment ownership. Analysis thresholds must be explicit and version-controlled. Preserve metric query, time window, sample sufficiency, analysis result, rollout revision, and traffic state so an automatic promotion can be audited.

### Automation possibilities

Automated canary/blue-green flows can pause, measure, promote, abort, or roll back based on deterministic analysis results. Human approval can remain a promotion step for high-risk changes. A metric-gated rollout is only as sound as its selected signals and thresholds; successful analysis is evidence for those checks, not proof that all failure modes are absent.

### Sources

- Argo Rollouts analysis/progressive delivery: https://argo-rollouts.readthedocs.io/en/stable/features/analysis/
- Argo Rollouts FAQ / supported strategies: https://argo-rollouts.readthedocs.io/en/stable/FAQ
- Argo Rollouts rollback window: https://argo-rollouts.readthedocs.io/en/stable/features/rollback/

## 5. Progressive delivery — Flagger

### Verified implementation

Flagger's current documentation describes a control loop for canary releases that gradually shifts traffic while evaluating key performance indicators such as HTTP success rate, request duration, and pod health. Based on configured analysis, the canary is promoted or aborted.

Flagger documents automated rollback behavior: after the configured failed-check threshold is reached, traffic is routed back to the primary workload, the canary is scaled down, and the rollout is marked failed. Custom Prometheus metrics and rollout webhooks can extend the analysis. Its deployment-strategy documentation also describes staged promotion and analysis timing.

### Selection and integration criteria

Flagger is representative of a controller that couples traffic shifting with metric/webhook analysis. Selection should consider supported ingress/service-mesh providers, metric backends, webhook semantics, workload model, and failure threshold behavior. Treat a rollback trigger as a policy decision derived from selected evidence; preserve the failed metric/webhook records and resulting traffic state.

### Automation possibilities

Automation can execute acceptance/load-test webhooks, increment canary traffic, evaluate success/error/latency thresholds, promote on success, and route back on configured failure. The rollback itself must still be observed and service health re-checked.

### Sources

- Flagger deployment strategies: https://docs.flagger.app/main/usage/deployment-strategies
- Flagger NGINX progressive-delivery tutorial: https://docs.flagger.app/main/tutorials/nginx-progressive-delivery

## 6. AI-assisted release and deployment operations — bounded evidence

### Verified current capability

GitLab documents Duo Root Cause Analysis for failed CI/CD jobs and a current Fix CI/CD Pipeline Flow that can inspect a failed pipeline and produce code suggestions or next steps. GitLab also documents deployment jobs as CI/CD jobs that use environments. The Fix Pipeline documentation records material limitations: only the last 150 KiB of job logs are processed by the AI gateway, dependency installation cannot always be verified in the sandbox, and repository instructions are not guaranteed to be followed in every case.

This evidence supports AI assistance for pipeline diagnosis and repair around deployment workflows. It does **not** establish that an AI system should be an autonomous production release authority or that it can independently verify production correctness.

### Safe integration baseline

AI may summarize failed deployment jobs, correlate logs, propose workflow/configuration changes, draft rollback/runbook actions, or prepare a remediation patch. Production execution should remain behind deterministic authorization, artifact identity, deployment-status, service-level, and rollback gates. Any AI-proposed change must be re-run through the normal CI/security/deployment verification path.

### Sources

- GitLab CI/CD jobs and deployment jobs: https://docs.gitlab.com/ci/jobs/
- GitLab Duo Root Cause Analysis use cases: https://docs.gitlab.com/user/gitlab_duo/use_cases/
- GitLab Fix CI/CD Pipeline Flow: https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/fix_pipeline/

## 7. Language-agnostic release/deployment baseline

A representative software-delivery baseline should preserve the following evidence for a release:

1. source commit and immutable artifact identity/digest;
2. build/test/security/provenance gates that produced or approved the artifact;
3. target environment identity and deployment policy decision;
4. exact desired deployment revision/configuration;
5. rollout execution result and orchestrator status tied to that revision;
6. post-deployment acceptance/health/telemetry evidence;
7. promotion decision for progressive delivery, including metric/webhook evidence;
8. rollback target and trigger criteria;
9. rollback execution plus post-rollback verification;
10. actor/automation identity and timestamps sufficient for audit.

The specific tools vary by language and hosting model. Static websites, services, desktop/mobile releases, embedded firmware, ML systems, and games can require different distribution and recovery mechanisms, but the evidence planes above remain useful selection criteria.

## 8. Contradictions and limits preserved

- **Deployment completed ≠ application correct.** Kubernetes rollout status observes rollout state, not domain correctness.
- **Authorization ≠ health.** GitHub environment approval/protection controls whether a job may run; they do not validate the deployed service.
- **Rollback command accepted ≠ recovery verified.** Rollback must be followed by rollout and service-level verification.
- **Progressive-delivery analysis ≠ exhaustive safety proof.** Argo Rollouts/Flagger automate decisions from configured signals; unmeasured failure modes remain possible.
- **AI pipeline repair ≠ autonomous release authority.** Current verified AI evidence is bounded by log/context/runtime limitations and must remain behind deterministic gates.
- No claim is made that Kubernetes, GitHub Actions, Argo Rollouts, Flagger, or GitLab are universally best choices; they are representative current implementations of distinct lifecycle roles.

## 9. Remaining unresolved expansion

- non-Kubernetes progressive-delivery and rollback systems;
- desktop/mobile/store release promotion and rollback semantics;
- firmware/embedded staged rollout and device-fleet recovery;
- database/schema migration safety and rollback/forward-fix strategies;
- feature-flag systems and experiment/kill-switch integration;
- SLO/error-budget-driven deployment gates across additional observability stacks;
- verified AI systems with explicit release/deployment-specific capabilities beyond CI/CD diagnosis/repair.
