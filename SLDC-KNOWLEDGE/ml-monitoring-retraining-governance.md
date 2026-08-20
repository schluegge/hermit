# ML model monitoring and governed retraining

Verification date: 2026-08-20

Status: **verified representative** for production model monitoring, alert-driven retraining initiation, model-version governance, and bounded promotion authority. This is not an exhaustive MLOps catalog and does not establish a universal retraining or deployment policy.

## Baseline definition

Production ML monitoring is the evidence plane that observes deployed-model behavior after release and compares production signals against explicit references, thresholds, or quality targets. Governed retraining is the controlled path that may turn a monitoring signal into a new candidate model while keeping candidate generation, evaluation, registration, approval, deployment, and post-deployment verification as separate gates.

A robust lifecycle therefore distinguishes:

1. **Production observation** — capture inputs, outputs, ground truth where available, operational metrics, and/or quality signals.
2. **Detection** — compute drift, data-quality, model-quality, bias/attribution, or custom signals against explicit baselines.
3. **Alert/event** — emit evidence that a threshold or anomaly condition was reached.
4. **Retraining initiation** — start a training workflow using identified data and configuration.
5. **Candidate evaluation** — compare the candidate against task-specific acceptance criteria and a known baseline/champion.
6. **Version registration** — create a traceable model version with artifacts and metadata.
7. **Approval/promotion decision** — apply deterministic policy and, where required, human approval before production eligibility.
8. **Deployment** — release using the deployment-safety mechanisms appropriate to the platform.
9. **Post-deployment verification** — continue monitoring the newly deployed version and preserve rollback/containment options.

These stages are related but not interchangeable. A drift alert is not proof that retraining is required; successful retraining is not proof that the new model is better; registration is not approval; approval is not a successful deployment; and deployment is not proof of sustained production quality.

## Role in the SDLC

This evidence plane closes the feedback loop between production operation and model development. It belongs across operations, maintenance, experimentation, CI/CD, governance, and release management rather than only inside training code.

Typical integration points include:

- production inference logging/data collection;
- monitoring jobs and alerting/event systems;
- feature/data pipelines and ground-truth ingestion;
- training/orchestration pipelines;
- evaluation/validation jobs;
- model registries and lineage stores;
- approval workflows and CI/CD;
- progressive/shadow deployment;
- SLO/incident systems and audit logs.

## Representative implementation 1 — Azure Machine Learning model monitoring

**Source type:** current official Microsoft Learn documentation.

**Scope verified:** Azure Machine Learning SDK/CLI v2 production model monitoring; documentation last updated 2026-02-11 for the implementation guide and current concept documentation available 2026-08-20.

Primary sources:

- https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-monitoring?view=azureml-api-2
- https://learn.microsoft.com/en-us/azure/machine-learning/how-to-monitor-model-performance?view=azureml-api-2

Verified capabilities:

- continuous/scheduled monitoring of production models;
- production inference data versus reference data such as training, validation, or ground-truth data;
- built-in signals including data drift and model-performance monitoring plus configurable custom signals/metrics;
- user-configured thresholds and alerting;
- Azure Event Grid integration for programmatic downstream action;
- models outside Azure Machine Learning can be monitored if production inference data is supplied to the monitoring system.

The current Azure documentation gives an explicit automation example: if production classification accuracy falls below a configured threshold, an Event Grid event can start a retraining job using collected ground-truth data.

### Boundary

That example proves **monitoring event -> retraining-job initiation**. It does not prove that the resulting candidate should be automatically promoted to production. Candidate evaluation, registration, approval, deployment, and post-deployment verification remain distinct gates.

## Representative implementation 2 — Vertex AI Model Monitoring v2

**Source type:** current official Google Cloud documentation.

Primary source:

- https://cloud.google.com/vertex-ai/docs/model-monitoring/set-up-model-monitoring

Verified current scope:

- a model must be registered in Vertex AI Model Registry before a v2 model monitor is associated with a model version;
- monitoring configuration can include feature fields, prediction fields, ground-truth fields, training/reference data, notification settings, monitoring objectives, metrics, and alert thresholds;
- models can be hosted on Vertex AI or other serving infrastructure;
- monitoring results can be exported to configured Cloud Storage.

### Material caveat — Preview and tabular-only

The current Model Monitoring v2 setup documentation marks the feature as **Preview / Pre-GA** and states that v2 supports only tabular models. No baseline claim should generalize this v2 path to all model modalities or treat Preview behavior/SLA as equivalent to GA production guarantees.

## Representative implementation 3 — Amazon SageMaker Model Monitor and Model Registry

**Source type:** current official AWS documentation.

Primary sources:

- https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html
- https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality.html
- https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html
- https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-approve.html

### Monitoring scope verified

For existing eligible customers, SageMaker Model Monitor documents monitoring of:

- data quality;
- model quality;
- bias drift;
- feature-attribution drift;
- real-time endpoints and scheduled/batch monitoring paths;
- alerts when configured deviations or quality thresholds are reached.

Model-quality monitoring can compare captured predictions with later ground-truth labels and compute task-specific quality metrics.

### Material lifecycle caveat — new-customer closure

AWS currently states that **new customer access to SageMaker Model Monitor closed on 2026-07-30**. Existing customers can continue using the service, but AWS says it does not plan new features. Therefore Model Monitor is valid current evidence for existing deployments but should not be selected as a greenfield universal recommendation without checking account eligibility and product direction.

### Registry / promotion governance verified

SageMaker Model Registry provides versioned model packages, lineage/metadata, approval state, deployment integration, and CI/CD integration. AWS documents these approval states and behaviors:

- a newly registered version can remain `PendingManualApproval`;
- evaluation can be performed before promotion;
- `Approved` can initiate CI/CD deployment when the project/event integration is configured;
- `Rejected` prevents that candidate from being selected as approved;
- approval may be set manually or by pipeline logic based on evaluation results.

This is direct evidence that **candidate version + evaluation + approval + deployment eligibility** can be represented as separate lifecycle controls.

## Selection criteria

Choose a monitoring/retraining architecture based on evidence for the actual workload, not product category names alone.

Evaluate at least:

- **signal availability:** input features, predictions, labels/ground truth, latency/cost, safety or business outcomes;
- **label latency:** whether ground truth arrives immediately, eventually, sparsely, or never;
- **model modality:** tabular, vision, NLP, ranking, forecasting, GenAI/agentic systems;
- **baseline semantics:** training set, validation set, recent production window, champion model, business target;
- **statistical semantics:** metric definition, windowing, confidence/noise behavior, drift test, minimum sample size;
- **event integration:** alert-only versus machine-readable event capable of initiating controlled workflows;
- **lineage:** ability to trace production version, training data, code/config, evaluation artifact, and deployment;
- **authority:** who/what may trigger retraining, approve a candidate, and deploy it;
- **rollback/containment:** whether bad candidates can be stopped, shadowed, rolled back, or traffic-shifted;
- **service lifecycle:** GA/Preview/deprecation/new-customer restrictions and support horizon;
- **cost and data governance:** retained production data, PII/sensitive fields, residency, sampling, and storage.

## Integration and deterministic gates

A representative governed automation path is:

```text
production inference
    -> capture / ground truth / operational telemetry
    -> monitoring job
    -> threshold/anomaly event
    -> retraining workflow
    -> candidate evaluation
    -> registry version
    -> approval gate
    -> shadow/canary/progressive deployment
    -> post-deployment monitoring
    -> promote, hold, or roll back
```

Minimum evidence that should be attached to an automated promotion decision where applicable:

- exact production model/version being replaced;
- training data/version and time range;
- code/config/environment identity;
- reason retraining was initiated;
- monitoring metric definition and observed value/window;
- candidate evaluation dataset/version;
- candidate-versus-baseline metrics and thresholds;
- approval actor/policy result;
- deployment identity and traffic state;
- post-deployment health/quality result.

## AI-driven automation possibilities

Evidence supports AI/automation assistance around this lifecycle, but authority must remain explicit.

Safe representative uses include:

- summarizing monitoring anomalies and affected features;
- correlating drift with upstream data/code/deployment changes;
- proposing candidate retraining hypotheses;
- generating investigation queries or reports;
- assisting with evaluation-result comparison;
- drafting remediation or rollback recommendations;
- orchestrating already-authorized deterministic jobs/tools through agent protocols;
- maintaining traceable knowledge about recurring incidents and model behavior.

AI-generated interpretation should not replace the underlying metric, dataset, evaluation, registry, approval, or deployment evidence. No checked primary source establishes a universal rule that an AI agent should autonomously promote a retrained production model.

## Contradiction / deduplication rules

- **Drift != quality loss.** Input/prediction distribution change can be a useful signal but does not by itself prove degraded task or business performance.
- **No drift != correctness.** Stable distributions do not prove the model remains safe or useful.
- **Alert != diagnosis.** A threshold crossing identifies a condition, not necessarily its root cause.
- **Retraining != remediation.** Retraining on unsuitable, stale, biased, or incorrectly labeled data can preserve or worsen the problem.
- **Evaluation != production impact.** Offline acceptance must be complemented by deployment/runtime evidence where material.
- **Registry alias/status != runtime state.** A version being named or approved does not prove which binary/model is serving requests.
- **Automation != authority.** A workflow can execute automatically while approval remains human or policy-controlled.
- **Monitoring service != lifecycle platform.** Monitoring, orchestration, registry, CI/CD, and deployment are separate evidence planes even when one vendor integrates them.

## Explicit unresolved items

As of 2026-08-20, this baseline does **not** establish:

- a universal metric or drift threshold that should trigger retraining across workloads;
- a universal minimum sample size/lookback window for reliable promotion decisions;
- that any one monitored drift metric causally predicts business impact;
- a cross-vendor portable semantic mapping among Azure, Vertex, AWS and other monitoring metrics;
- a turnkey current Vertex v2 monitor -> retrain -> evaluate -> approve -> deploy chain for all model types;
- that SageMaker Model Monitor is available to new customers after 2026-07-30;
- autonomous AI authority to approve or promote production models;
- safe automatic retraining when labels are delayed, sparse, adversarial, or absent;
- a universal rollback mechanism for model behavior that has already caused external side effects.

## Sources

All sources were independently read from current vendor/maintainer documentation on 2026-08-20. Repeated vendor pages are treated as one upstream evidence family, not independent corroboration.

1. Microsoft Learn — Azure ML model monitoring concept: https://learn.microsoft.com/en-us/azure/machine-learning/concept-model-monitoring?view=azureml-api-2
2. Microsoft Learn — monitor model performance: https://learn.microsoft.com/en-us/azure/machine-learning/how-to-monitor-model-performance?view=azureml-api-2
3. Google Cloud — Vertex AI Model Monitoring v2 setup: https://cloud.google.com/vertex-ai/docs/model-monitoring/set-up-model-monitoring
4. AWS — SageMaker Model Monitor: https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor.html
5. AWS — SageMaker model-quality monitoring: https://docs.aws.amazon.com/sagemaker/latest/dg/model-monitor-model-quality.html
6. AWS — SageMaker Model Registry: https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry.html
7. AWS — model approval status: https://docs.aws.amazon.com/sagemaker/latest/dg/model-registry-approve.html
