# ML data quality, feature stores, and orchestration

Verification date: 2026-08-20

Scope: representative, primary-source-backed baseline for three distinct ML lifecycle planes that were previously open in `COVERAGE.md`: data validation, feature management/serving, and workflow orchestration. This is not an exhaustive catalog of MLOps systems.

## Baseline separation

These planes solve different problems and must not be treated as interchangeable:

1. **Data validation** checks whether data satisfies explicit or inferred expectations and can surface drift/skew/anomalies.
2. **Feature store** manages feature definitions and retrieval across training and serving contexts; it does not automatically implement every transformation or model-serving function.
3. **Workflow orchestration** defines and executes dependency-aware tasks/pipelines; a successful workflow run does not prove that its data, model, or business outcome is correct.
4. **Metadata/lineage** records executions/artifacts and their relationships; lineage improves traceability but is not itself a correctness proof.

## 1. Data validation — TensorFlow Data Validation

### Verified implementation

TensorFlow Data Validation (TFDV) is a library for exploring and validating ML data. The maintainer repository lists **TFDV 1.21.0** as the latest release on 2026-06-11. The release adds Python 3.12/3.13 support, drops Python 3.9, and scopes TensorFlow to `>=2.21,<2.22`.

Current official TFX documentation verifies that TFDV can:

- compute descriptive statistics;
- infer a schema describing expected feature presence, type, cardinality/presence and domains;
- validate dataset statistics against that schema and emit anomalies;
- validate examples individually;
- use schema environments to distinguish training-versus-serving expectations;
- detect training-serving skew and data drift.

### SDLC / ML lifecycle role

Use a data-validation plane before or during training, before promotion of new datasets, and where appropriate on serving/ingestion data. The evidence produced should be machine-readable enough for a pipeline gate rather than relying only on visual inspection.

### Selection criteria

- supported input/data representation and scale;
- schema/anomaly model required by the project;
- drift/skew requirements;
- compatibility with the selected TensorFlow/TFX/Python dependency set;
- batch/distributed execution requirements;
- whether per-example validation is required;
- platform support demonstrated for the exact release.

### Integration and automation

A deterministic automation path is:

`dataset -> statistics -> schema/expectations -> validation -> anomaly artifact -> explicit pass/fail policy -> training/promotion`

Schema inference is a bootstrap mechanism, not evidence that inferred expectations are semantically correct. Human/domain review remains necessary before treating a generated schema as policy.

### Caveats / unresolved

- TFDV 1.21.0 has explicit dependency bounds; compatibility outside those bounds is not assumed.
- Older TFDV releases deprecated Windows support. The checked 1.21.0 release notes do not establish a current Windows-support guarantee, so **TFDV 1.21.0 Windows support remains unresolved** in this baseline.
- Statistical drift/skew detection identifies distribution change according to configured methods/thresholds; it does not by itself establish harmful model impact or root cause.

## 2. Feature store — Feast

### Verified implementation

Current Feast documentation describes an architecture with:

- a registry for version-controlled feature definitions;
- an offline-store interface for historical feature retrieval and point-in-time-correct training datasets;
- an online store for low-latency retrieval of the latest feature values per entity;
- `feast apply` for publishing feature definitions/infrastructure state;
- `feast materialize` for loading feature values from offline to online storage;
- SDK/server paths for historical and online feature retrieval;
- optional push/stream paths and feature transformation mechanisms.

The official architecture explicitly states that Feast does **not** perform every batch/stream transformation itself: separate transformation engines may be required, and model deployment itself is outside Feast's responsibility.

### SDLC / ML lifecycle role

A feature store provides a controlled interface between feature definitions/data sources and model training/inference. Its baseline value is reproducible feature definition, historical retrieval for training, and consistent online retrieval semantics for serving.

### Selection criteria

- offline-store/data-source compatibility;
- online serving latency and availability needs;
- point-in-time correctness requirements;
- registry/version-control workflow;
- materialization versus push/stream ingestion model;
- transformation-engine requirements outside the feature store;
- supported SDK/client languages;
- access-control requirements;
- operational ownership of offline/online infrastructure.

### Integration and automation

Representative deterministic path:

`versioned feature definitions -> feast apply -> historical retrieval/training dataset -> training -> materialize/push -> online retrieval -> serving`

CI can validate and apply version-controlled feature definitions; schedulers can automate materialization. Those actions must remain separate from assertions that the underlying feature values are statistically valid or that a model using them is correct.

### Caveats

- The online store retains the latest feature values per entity rather than general historical history; historical training retrieval is an offline-store concern.
- Feast's documentation recommends domain expertise when integrating data sources because write patterns and latency/consistency tradeoffs vary.
- A feature store does not replace upstream data-quality checks, general ETL/ELT, model training, model registry/evaluation, or model serving.

## 3. ML-first orchestration — Kubeflow Pipelines

### Verified implementation

Current Kubeflow Pipelines (KFP) documentation defines a pipeline as a graph of components with execution order/conditions, parameter passing, artifact flow, retries, caching, resource requests, and exit handling. The backend translates pipeline runs into Kubernetes resources/Pods that execute component containers.

KFP components have explicit inputs/outputs and implementation/runtime definitions. Pipeline runtime metadata records task status, executions and artifacts and can expose lineage across runs. Current KFP documentation notes that **KFP 2.15** introduced a metadata-backend database-index migration for upgrades from pre-2.15 and states that the migration does not support rollback; production database backup is therefore advised before that upgrade.

### SDLC / ML lifecycle role

Use KFP when the lifecycle requires repeatable, dependency-aware ML workflows with artifact passing, resource/GPU constraints, experiment/run history, retries/caching and Kubernetes-native execution.

### Selection criteria

- Kubernetes availability and operational cost;
- need for ML-specific artifacts/metadata/lineage;
- container/runtime isolation requirements;
- CPU/GPU/resource scheduling needs;
- caching and retry semantics;
- portability of component definitions;
- metadata-store upgrade/recovery requirements.

### Integration and automation

Representative pipeline:

`ingest -> validate -> transform/features -> train -> evaluate -> register/promote`

Each component should emit artifacts/metrics that a later deterministic gate can inspect. Orchestration automates sequencing and execution; it does not turn a successful task status into evidence that the model meets quality, safety, security or business thresholds.

### Caveats

- KFP is Kubernetes-oriented; this operational dependency is material when selecting it for small/local workflows.
- Cache hits can skip re-execution according to KFP caching semantics, so pipeline design must ensure cache keys/inputs correspond to the intended reproducibility boundary.
- The documented KFP 2.15 metadata migration rollback limitation must be handled as an operational upgrade risk, not hidden by workflow-level retry logic.

## 4. General batch orchestration — Apache Airflow

### Verified implementation

Apache Airflow **3.3.0** official documentation defines Airflow as a platform for developing, scheduling and monitoring **batch-oriented** workflows. Workflows are Python-defined Dags containing tasks, schedules, dependencies, callbacks and runtime behavior such as retries/timeouts. Airflow can orchestrate arbitrary technologies through providers/operators or shell/Python execution.

### SDLC / ML lifecycle role

Airflow is a representative general-purpose option when ML/data work is fundamentally batch-oriented and benefits from workflow-as-code, scheduling, retries, monitoring and integration with heterogeneous systems.

### Selection criteria

- batch/scheduled versus continuously streaming workload shape;
- provider/operator availability;
- executor/deployment scale;
- workflow observability and retry requirements;
- whether ML-specific artifact/lineage semantics are needed beyond general orchestration.

### Caveats

Airflow documentation explicitly positions it around batch workflows with a clear start/end. It should not be presented as the default solution for continuously running streaming/event-processing systems merely because it can trigger external systems.

## AI-driven automation possibilities

Evidence-backed deterministic capabilities above create safe integration points for AI assistance without assigning the model unsupported authority. AI systems may assist with research, pipeline/component/Dag authoring, configuration explanation, failure-log triage, documentation and proposed remediation where an independently verified AI capability exists. For ML lifecycle actions, the authoritative gate should remain tool output such as:

- TFDV anomaly/schema validation results;
- feature-definition/config validation and retrieval/materialization results;
- pipeline task status plus produced artifacts/metrics;
- model evaluation/registry criteria already documented elsewhere in this baseline.

No AI system is inferred here to have autonomous production data/model promotion authority. Such authority remains unresolved unless a product's current primary documentation proves both the action and its verification/approval boundary.

## Contradiction / deduplication rules

- **TFDV != feature store:** validating data does not establish training/serving feature retrieval consistency.
- **Feast != transformation engine:** Feast explicitly relies on separate engines for important transformation cases.
- **Feast != model deployment:** deployment is outside Feast's documented responsibility.
- **KFP/Airflow != validator:** workflow success means tasks executed according to workflow semantics, not that their domain outputs are correct.
- **KFP != Airflow equivalence:** KFP is ML/Kubernetes-oriented with artifact/metadata concepts; Airflow is a general batch workflow platform. Selection is workload/operations dependent.
- **Lineage != correctness:** knowing which execution produced an artifact does not prove the artifact is valid.
- **Schema inference != policy proof:** inferred schemas require domain review before becoming authoritative expectations.

## Sources

| ID | Source | Type | Verified | Scope / caveat |
|---|---|---|---|---|
| TFDV-1 | https://github.com/tensorflow/data-validation/releases | Maintainer release repository | 2026-08-20 | TFDV 1.21.0 latest release; Python/TensorFlow dependency scope |
| TFDV-2 | https://www.tensorflow.org/tfx/data_validation/get_started | Official TensorFlow/TFX docs | 2026-08-20 | statistics, schema inference, anomaly/per-example validation, environments |
| TFDV-3 | https://www.tensorflow.org/tfx/guide/tfdv | Official TensorFlow/TFX guide | 2026-08-20 | schema validation, training-serving skew, drift |
| FEAST-1 | https://docs.feast.dev/getting-started/components/overview | Official project docs | 2026-08-20 | apply/materialize, registry, online/offline store, retrieval, transformation/deployment boundaries |
| FEAST-2 | https://docs.feast.dev/reference/offline-stores/overview | Official project docs | 2026-08-20 | point-in-time historical retrieval and materialization interface |
| FEAST-3 | https://docs.feast.dev/getting-started/components/online-store | Official project docs | 2026-08-20 | latest-value online-store semantics |
| KFP-1 | https://www.kubeflow.org/docs/components/pipelines/concepts/pipeline/ | Official Kubeflow docs | 2026-08-20 | pipeline graph, artifacts, retries, caching, resources |
| KFP-2 | https://www.kubeflow.org/docs/components/pipelines/concepts/component/ | Official Kubeflow docs | 2026-08-20 | component interfaces/runtime/dependencies |
| KFP-3 | https://www.kubeflow.org/docs/components/pipelines/concepts/metadata/ | Official Kubeflow docs | 2026-08-20 | execution/artifact metadata, lineage, KFP 2.15 migration rollback caveat |
| AIRFLOW-1 | https://airflow.apache.org/docs/apache-airflow/stable/ | Apache official docs | 2026-08-20 | Airflow 3.3.0, batch workflow role, workflow-as-code |
| AIRFLOW-2 | https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html | Apache official docs | 2026-08-20 | Dag tasks/dependencies/schedule/retries/timeouts |

## Residual frontier

This representative baseline does not close the open ML ecosystem. Remaining useful research includes:

- independent data-validation systems and semantic/data-contract tooling outside TFDV;
- feature-store alternatives and cross-store consistency/latency evidence;
- stream-first orchestration/processing systems;
- dataset/version lineage and reproducibility systems beyond the KFP metadata representative;
- quantitative feature freshness/skew/availability SLOs;
- data-labeling/human-feedback lifecycle;
- model monitoring, drift-to-model-impact linkage and automated retraining/promotion governance;
- independently documented AI-native ML orchestration/remediation systems with explicit production authority and verification gates.
