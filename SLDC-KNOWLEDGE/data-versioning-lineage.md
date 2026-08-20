# Data versioning and lineage baseline

Verification date: 2026-08-20

Status: **verified representative**

## Baseline definition

Data versioning and data lineage solve different lifecycle problems and must not be collapsed into one control plane.

- **Data versioning** creates durable references to historical dataset/object states so a prior state can be restored, compared, reproduced, or promoted.
- **Data lineage** records how data-processing jobs/runs consume and produce datasets and associated metadata so dependency and provenance relationships can be inspected.
- **Pipeline orchestration** schedules or executes work; it is not, by itself, proof that the input/output data state is versioned or that lineage is complete.

A software-development baseline should therefore preserve at least four distinct evidence planes:

1. code/config revision;
2. data/dataset revision;
3. execution/run identity;
4. lineage/provenance metadata connecting jobs/runs to inputs and outputs.

## Role in the SDLC

Versioned data and lineage support reproducibility, debugging, regression investigation, review, controlled promotion, incident analysis, auditability, ML experiment reconstruction, and safer data/ML pipeline evolution. They become especially important when code can remain unchanged while training data, fixtures, generated assets, schemas, or upstream datasets change.

## Representative implementation 1 — DVC 3.67.1

Source type: official maintainer documentation and primary GitHub release repository.

Current verified scope:

- DVC release `3.67.1` is the latest release shown by the maintainer repository as of the verification date.
- `dvc add` tracks data files/directories through DVC metadata and cache rather than requiring large artifacts to live directly in Git.
- `dvc push` / `dvc pull` synchronize tracked artifacts with configured remote storage.
- `dvc.yaml` can declare pipeline dependencies and outputs.
- `dvc repro` can reproduce pipeline stages based on declared dependencies/outputs.
- `dvc get --rev <commit|branch|tag>` can retrieve a tracked artifact from a selected repository revision.

Primary sources:

- https://dvc.org/doc/command-reference/
- https://dvc.org/doc/command-reference/get
- https://github.com/iterative/dvc/releases

Material caveats:

- DVC tracking does not make the underlying data semantically correct, representative, licensed for the intended use, or free of leakage.
- A Git commit alone does not prove the remote artifact is still available; reproducibility also depends on retained DVC objects/remotes and environment/tool compatibility.
- DVC pipeline metadata is not equivalent to a cross-system lineage standard.

## Representative implementation 2 — lakeFS 1.84.1

Source type: official lakeFS documentation and primary GitHub release repository.

Current verified scope:

- lakeFS release `v1.84.1` is the latest release shown by the maintainer repository as of the verification date.
- lakeFS provides Git-like data operations including branch, commit, merge, revert and tag over object-store data.
- Creating a branch is documented as a metadata/zero-copy operation rather than copying all objects.
- Commits are immutable checkpoints; merges atomically update a destination branch.
- Branch protection can prevent direct writes/commits and require changes to arrive through merges.
- Pre-merge hooks can run validations before protected data reaches important branches.

Primary sources:

- https://docs.lakefs.io/latest/understand/glossary/
- https://docs.lakefs.io/latest/understand/data-structure/
- https://docs.lakefs.io/howto/protect-branches/
- https://github.com/treeverse/lakeFS/releases

Material caveats:

- A successful branch/commit/merge operation proves version-control mechanics, not data quality.
- `revert` restores repository data state at the versioning layer; it does not prove external consumers, derived systems, side effects, or already-exported copies were reverted.
- lakeFS and DVC operate at different integration/scaling models; neither is treated as a universally superior replacement for the other.

## Representative implementation 3 — OpenLineage 1.52.0

Source type: official specification/documentation and primary maintainer repository.

Current verified scope:

- OpenLineage `1.52.0` is the latest release shown by the maintainer repository as of the verification date.
- OpenLineage defines an open, extensible model for lineage metadata around **Dataset**, **Job**, and **Run** entities.
- Run events represent execution-state transitions such as `START`, `RUNNING`, `COMPLETE`, `ABORT`, and `FAIL`.
- Jobs are identified by namespace/name and can declare input/output datasets.
- Facets extend the core model with additional metadata without redefining the core entity model.
- The API accepts run-, job-, and dataset-related lineage events.

Primary sources:

- https://openlineage.io/docs/spec/
- https://openlineage.io/docs/spec/facets/job-facets/
- https://openlineage.io/apidocs/openapi/
- https://github.com/OpenLineage/OpenLineage/releases

Material caveats:

- Emitting lineage events does not prove that every transformation, dataset, field, or external side effect was captured.
- `COMPLETE` is an execution-state event, not proof that data quality or business correctness gates passed.
- Lineage metadata can become incomplete or misleading when instrumentation is missing, producers use inconsistent naming, or events are dropped.

## Selection criteria

Choose a data-versioning/lineage stack using evidence for the following project-specific requirements:

- artifact/data size and storage backend;
- local Git-centric versus shared object-store workflows;
- branch/merge/isolation requirements;
- reproducible point-in-time retrieval;
- retention and garbage-collection guarantees;
- offline/local development requirements;
- pipeline-framework and warehouse/lake integrations;
- run/job/dataset naming and identity conventions;
- column/field-level lineage requirements versus dataset-level lineage;
- access control and protected-promotion requirements;
- machine-readable APIs/events needed for CI, observability, audit, or automation;
- recovery semantics and external side effects outside the versioned store.

Do not select a tool from feature-name similarity alone. Demonstrate the exact workflow against representative data volume, storage, failure, and recovery conditions.

## Integration points

A robust integration can connect:

`code revision -> data revision -> pipeline/run identity -> lineage event -> validation evidence -> promoted dataset/model/artifact`

Useful machine-verifiable identifiers include:

- Git commit/tag;
- DVC revision plus tracked artifact metadata/hash;
- lakeFS repository/branch/commit/tag;
- OpenLineage namespace + job + run + dataset identifiers;
- validation/test result identifiers;
- model/package/release identifiers produced downstream.

These identifiers should be persisted together where reproducibility matters. A human-readable dataset name without an immutable or resolvable revision is insufficient evidence for exact reproduction.

## Automation possibilities

Evidence-backed deterministic automation includes:

- checkout/retrieval of a selected DVC revision;
- pushing/pulling versioned DVC artifacts;
- reproducing declared DVC pipeline stages;
- creating isolated lakeFS branches;
- running pre-merge validation hooks before data promotion;
- atomically merging accepted lakeFS data changes;
- emitting and consuming OpenLineage run/job/dataset events;
- traversing lineage metadata to identify upstream/downstream dependencies where instrumentation exists.

AI can assist with interpreting lineage graphs, proposing likely impact sets, preparing validation plans, comparing revisions, or selecting which artifacts/runs to inspect. This is an **inference from the verified machine-readable/versioned interfaces**, not evidence that an AI system should autonomously approve data promotion. Promotion authority remains behind explicit policy and deterministic validation unless a specific implementation proves otherwise.

## Contradiction and deduplication rules

1. **Versioning != lineage.** A retrievable historical dataset does not reveal how it was produced.
2. **Lineage != versioning.** A lineage edge does not guarantee the referenced data can still be restored byte-for-byte.
3. **Lineage != correctness.** Captured dependencies can describe a bad computation perfectly.
4. **Orchestration != lineage completeness.** A successful DAG/run does not prove all external data dependencies were instrumented.
5. **Rollback != side-effect reversal.** Reverting a versioned dataset does not automatically undo downstream copies, notifications, model training, or external writes.
6. **Hash/commit identity != semantic validity.** Immutable identity says which data was used, not whether it should have been used.

## Unresolved / open research

- independent dataset-versioning implementations beyond the DVC/lakeFS representatives;
- Iceberg/Delta/Hudi snapshot/time-travel semantics versus dedicated data-version-control systems;
- column-level and transformation-level lineage completeness across heterogeneous engines;
- quantitative lineage freshness/completeness SLOs and event-loss detection;
- retention/garbage-collection interactions with long-term reproducibility;
- dataset licenses/consent/governance tied to immutable versions;
- feature freshness/availability and dataset-quality SLO integration;
- governed data promotion that combines versioning, lineage, quality checks, privacy/security policy, and downstream impact analysis;
- AI-assisted lineage/impact analysis with independently measured precision/recall and explicit promotion authority boundaries.
