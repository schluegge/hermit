# SLDC-KNOWLEDGE

Evidence-based, language-agnostic software-development lifecycle knowledge for this repository.

## Evidence policy

- Never infer a tool, capability, compatibility claim, or best practice without evidence.
- Prefer current official documentation, specifications, maintainer repositories, and reproducible repository evidence.
- Record verification date, source type, version/scope when material, and caveats.
- Distinguish finite required-category coverage from open-ended discovery. The open universe of AI automation is never marked exhaustive.
- `complete` means the category has: baseline definition, SDLC role, representative verified implementation/tool classes, selection criteria, integration points, automation possibilities, and evidence.
- `partial` means useful verified material exists but the completion criteria are not yet fully satisfied.
- `unresolved` means evidence is insufficient or contradictory.

## Required named categories

The audited status is maintained in [`COVERAGE.md`](./COVERAGE.md).

Required categories: debuggers; linters; formatters; testers; runners; LSP/language servers; language-specific best practices; libraries/package ecosystems; AI-SDLC; tools that help AI code; AI DevOps; AI CI/CD; memory; context management; MCP; A2A; ACP; AI-driven automation.

## Files

- `COVERAGE.md` — finite required-category audit and completion criteria plus non-exhaustive expansion coverage.
- `core-toolchain.md` — language-agnostic baseline for debugging, linting/static analysis, formatting, testing, runners/build execution, LSP, best practices, and package/library ecosystems.
- `language-domain-matrix.md` — verified implementations for JS/TS/Node, JVM/Java, C/C++, .NET/C#, Android, embedded/HIL, data/ML and games.
- `domain-expansion-2026-08.md` — additional primary-source-backed domain baselines for Apple/iOS/Xcode, Unreal Engine, MLflow and ESP-IDF.
- `ml-data-feature-orchestration.md` — ML data-validation, feature-store and orchestration baseline covering TFDV, Feast, Kubeflow Pipelines and Apache Airflow with explicit correctness/authority boundaries.
- `data-versioning-lineage.md` — data/dataset versioning and lineage baseline covering DVC, lakeFS and OpenLineage, with explicit distinctions among version identity, lineage, orchestration, correctness and recovery.
- `lakehouse-table-history.md` — transactional lakehouse table-history baseline for Apache Iceberg, Delta Lake and Apache Hudi, covering native historical identity, time travel, retention/cleanup, reproducibility and automation boundaries.
- `ml-monitoring-retraining-governance.md` — production model monitoring, alert/event-driven retraining initiation, model-version approval/promotion governance, and explicit automation/authority boundaries across current Azure, Vertex AI and SageMaker evidence.
- `godot-engine-baseline.md` — Godot 4.7.x game-engine baseline covering CLI/headless execution and export, debugging, profiling, GDScript typing/warnings, test-framework boundaries and GUT 4.7.x-compatible CI testing.
- `performance-profiling-tracing.md` — language-agnostic profiling/tracing baseline, Perfetto, Go pprof/PGO, JFR, Windows ETW/WPR/WPA, Linux `perf`/eBPF continuous profiling and bounded AI-assisted interpretation.
- `performance-platform-ci.md` — Apple Instruments/`xctrace`, NVIDIA Nsight Systems/Compute, and reproducible/statistical performance-CI evidence and gating boundaries.
- `gpu-vendor-profiling.md` — current AMD ROCprofiler-SDK/`rocprofv3` and ROCm Compute Profiler, Intel VTune GPU analysis, Intel GPA EOL boundary, and cross-vendor metric-mapping rules.
- `supply-chain-security-fuzzing.md` — SLSA provenance/build guarantees, Sigstore/Cosign signing and attestations, OpenSSF Scorecard posture checks, OSS-Fuzz/CIFuzz, and bounded AI-assisted fuzzing evidence.
- `language-native-fuzzing.md` — language/ecosystem-native fuzzing baseline for LLVM libFuzzer, Go native fuzzing, Rust `cargo-fuzz`, and JVM Jazzer, including regression preservation and platform/tool-lifecycle caveats.
- `application-security-sbom-policy.md` — SPDX/CycloneDX SBOMs, dependency vulnerability/license policy, secret scanning, SAST, DAST, runtime security, and deployment policy as code.
- `vulnerability-intelligence-sbom-consumers.md` — OSV vulnerability-data/schema semantics, OSV-Scanner direct CI/SBOM consumption, Dependency-Track v5 portfolio analysis/policy gating, and explicit inventory/matching/triage/authority boundaries.
- `container-iac-cloud-mobile-security.md` — container/image and repository scanning, IaC scanning, cloud security posture, mobile AppSec and bounded AI-assisted security remediation.
- `release-deployment-progressive-delivery.md` — release/deployment evidence planes, Kubernetes rollout verification/rollback, GitHub environment gates, Argo Rollouts/Flagger progressive delivery, and bounded AI-assisted deployment operations.
- `release-safety-flags-database-nonk8s.md` — feature flags/kill switches, database migration validation/recovery boundaries, and representative non-Kubernetes delivery/rollback semantics.
- `zero-downtime-database-evolution.md` — expand/contract schema evolution, mixed-version compatibility, PostgreSQL 18 concurrent/deferrable validation primitives, MySQL 8.4 online-DDL boundaries, and deterministic migration gates.
- `database-backfill-cdc.md` — long-running data backfills, CDC-assisted convergence, snapshot/stream overlap, validation and cutover boundaries.
- `store-and-fleet-release-safety.md` — App Store/Google Play phased and staged rollout semantics plus AWS IoT Jobs and Azure Device Update fleet rollout, abort and rollback boundaries.
- `firmware-anti-rollback-automotive.md` — firmware security-counter/downgrade protection, MCUboot candidate-image fallback, ESP-IDF eFuse anti-rollback, and Uptane automotive multi-ECU update-security boundaries.
- `slo-error-budget-release-gates.md` — SLI/SLO/error-budget policy, OpenSLO SLO-as-code, Grafana/Datadog reliability signals, Harness SLO-driven deployment governance/rollback, and bounded AI SRE integration.
- `desktop-update-security.md` — desktop updater trust/signing/freshness, Windows MSIX/App Installer update+downgrade semantics, Sparkle 2 signing/update boundaries, and explicit rollback caveats.
- `linux-desktop-updates.md` — Linux desktop update-channel baseline covering Flatpak, Snap and AppImage/AppImageUpdate, with explicit trust, refresh, downgrade/revert, data-state and automation boundaries.
- `distribution-linux-package-management.md` — distribution-native Linux package-management baseline for APT/dpkg, DNF5/RPM, Zypper/Snapper/transactional-update, and Pacman, with explicit trust, transaction, downgrade, recovery, and automation boundaries.
- `immutable-transactional-linux-os.md` — immutable/transactional Linux OS baseline for rpm-ostree, bootc bootable-container images and NixOS generations, with explicit activation, retention, rollback, mutable-state, trust and post-boot-health boundaries.
- `ubuntu-core-update-governance.md` — Ubuntu Core 26 update/recovery baseline covering snap revisions, refresh control, validation sets, essential-snap remodel boot verification, component revert and recovery-mode boundaries.
- `agent-protocols.md` — MCP, A2A, ACP and their distinct integration roles.
- `ai-sdlc.md` — cross-vendor AI-SDLC baseline, coding-tool taxonomy, verified automation classes, selection criteria and non-exhaustive research frontier.
- `ai-ops-memory-context.md` — AI DevOps, AI CI/CD, agent memory, and context-management baseline with cross-vendor primary evidence.
- `checkpoints/` — append-only research-run checkpoints.

## Scope

The taxonomy is intended to apply from small scripts/static websites through services, desktop/mobile applications, infrastructure, data/ML, embedded systems, and games. Product-domain-specific tooling is added only when supported by evidence.

The 18 explicitly required category baselines can be complete while discovery continues. A `complete` category is not an exhaustive catalog of every language, tool, vendor, domain, or future AI capability.

The language/domain coverage is intentionally representative rather than prescriptive. A verified implementation demonstrates how a category is realized in an ecosystem; it does not imply that the implementation is the only or universally best choice for that ecosystem.