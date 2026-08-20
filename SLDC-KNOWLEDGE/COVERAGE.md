# Required-category coverage

Verification date: 2026-08-20

Status semantics are defined in `README.md`.

| Required category | Status | Evidence file | Main reason |
|---|---|---|---|
| Debuggers | complete | `core-toolchain.md` | Definition, role, representative implementation, selection, integration, automation documented |
| Linters | complete | `core-toolchain.md` | Static-analysis/lint role and verified Rust/Go examples documented |
| Formatters | complete | `core-toolchain.md` | Deterministic formatting role and verified Rust implementation documented |
| Testers | complete | `core-toolchain.md` | Test role and verified Rust implementation documented |
| Runners | complete | `core-toolchain.md` | Execution/build/test runner role and Cargo integration documented |
| LSP / language servers | complete | `core-toolchain.md` | Protocol role and official Go language-server implementation documented |
| Language-specific best practices | complete | `core-toolchain.md` | Evidence-backed principle for toolchain-native conventions plus verified Rust/Go examples |
| Libraries / package ecosystems | complete | `core-toolchain.md` | Package/dependency role and Cargo ecosystem integration documented |
| AI-SDLC | complete | `ai-sdlc.md`, `ai-ops-memory-context.md` | Cross-vendor baseline spans planning/requirements, coding, testing, review/security, CI repair, migration/maintenance and operations with selection/integration/verification criteria |
| Tools that help AI code | complete | `ai-sdlc.md`, `core-toolchain.md`, `agent-protocols.md` | Cross-vendor taxonomy covers assistants, coding/planning agents, review/security, CI repair, migration, protocols, instructions, deterministic gates and memory/context |
| AI DevOps | complete | `ai-ops-memory-context.md` | Definition, operations role, AWS/Google implementations, selection, integrations and automation documented with product caveats |
| AI CI/CD | complete | `ai-ops-memory-context.md`, `ai-sdlc.md` | Definition, GitHub/GitLab implementations, runner/workflow integration, pipeline diagnosis/repair, selection and bounded automation documented |
| Memory | complete | `ai-ops-memory-context.md` | Definition, LangGraph/AutoGen implementations, persistence scopes, selection, integrations and automation documented |
| Context management | complete | `ai-ops-memory-context.md`, `agent-protocols.md` | Definition, LangChain/GitLab mechanisms, budget/provenance selection, integrations and automation documented |
| MCP | complete | `agent-protocols.md` | Current official protocol role, primitives, transport direction, selection/integration documented |
| A2A | complete | `agent-protocols.md` | Official v1.0 role, interoperability scope, selection/integration documented |
| ACP | complete | `agent-protocols.md` | Official Zed role, editor-agent interoperability and selection/integration documented |
| AI-driven automation | complete | `ai-sdlc.md`, `ai-ops-memory-context.md`, `agent-protocols.md`, `ml-data-feature-orchestration.md`, `ml-monitoring-retraining-governance.md`, `performance-profiling-tracing.md`, `performance-platform-ci.md`, `gpu-vendor-profiling.md`, `supply-chain-security-fuzzing.md`, `application-security-sbom-policy.md`, `container-iac-cloud-mobile-security.md`, `release-deployment-progressive-delivery.md`, `release-safety-flags-database-nonk8s.md`, `zero-downtime-database-evolution.md`, `database-backfill-cdc.md`, `store-and-fleet-release-safety.md`, `slo-error-budget-release-gates.md`, `desktop-update-security.md` | Finite baseline has definition, lifecycle role, representative verified classes, selection, integration and automation possibilities; open-ended capability discovery explicitly remains non-exhaustive |

## Finite Definition of Done

A required category may be marked `complete` only when all six are present and evidenced:

1. Baseline definition.
2. Role in the SDLC.
3. Representative verified tool classes or implementations.
4. Selection criteria.
5. Integration points.
6. Relevant automation possibilities.

## Completion status

**18 / 18 named required categories satisfy the finite baseline Definition of Done as of 2026-08-20.**

This is a coverage claim about the explicitly named taxonomy only. It is **not** a claim that all software-development tools, languages, domains, AI products, or AI-automation possibilities have been exhaustively enumerated. Open-ended discovery continues and new evidence must be deduplicated into the existing taxonomy.

## Non-exhaustive language/domain expansion

The following expansion rows track whether at least one current, primary-source-backed implementation set has been documented for each high-value ecosystem/domain. `verified representative` means a real toolchain/domain baseline is evidenced; it does **not** mean the ecosystem is exhaustively cataloged.

| Ecosystem / domain | Expansion status | Evidence file | Verified scope |
|---|---|---|---|
| JavaScript / TypeScript / Node.js | verified representative | `language-domain-matrix.md` | Compiler/typecheck, language service, debugger, stable built-in test runner |
| JVM / Java | verified representative | `language-domain-matrix.md` | JDK 26 compiler/debugger/REPL/diagnostics plus current JUnit platform |
| C / C++ | verified representative | `language-domain-matrix.md` | clang-tidy, clang-format, clangd, LLDB, CMake/CTest integration |
| .NET / C# | verified representative | `language-domain-matrix.md` | Roslyn analyzers, `dotnet format`, `dotnet test` |
| Mobile / Android | verified representative | `language-domain-matrix.md` | Gradle/AGP, Android Lint, tests/device execution, profiler |
| Apple / iOS | verified representative | `domain-expansion-2026-08.md` | Xcode devices/Simulator, debugger/Instruments, Swift Testing/XCTest, performance testing, Xcode Cloud |
| Embedded / HIL | verified representative | `language-domain-matrix.md`, `domain-expansion-2026-08.md` | Zephyr west/Twister plus ESP-IDF build/flash/monitor/on-target testing |
| Data / ML | verified representative | `language-domain-matrix.md`, `domain-expansion-2026-08.md`, `ml-data-feature-orchestration.md`, `ml-monitoring-retraining-governance.md` | PyTorch profiling; MLflow tracking/registry/evaluation; TFDV data validation; Feast feature-store semantics; Kubeflow Pipelines/Airflow orchestration; production monitoring and governed retraining/promotion boundaries |
| ML data quality / feature stores / orchestration | verified representative | `ml-data-feature-orchestration.md` | TFDV 1.21.0 schema/statistics/anomaly validation; Feast offline/online retrieval and versioned feature definitions; KFP ML pipelines/metadata/lineage; Airflow 3.3.0 batch workflow orchestration |
| ML model monitoring / governed retraining | verified representative | `ml-monitoring-retraining-governance.md` | Azure ML monitoring + Event Grid retraining trigger; Vertex AI Model Monitoring v2 Preview/tabular scope; SageMaker existing-customer monitoring plus versioned registry approval/CI-CD gates |
| Games | verified representative | `language-domain-matrix.md`, `domain-expansion-2026-08.md`, `godot-engine-baseline.md` | Unity testing/profiler, Unreal automation testing/build automation, and Godot CLI/headless/debug/profile/export/testing baseline |
| Additional game engines | verified representative | `domain-expansion-2026-08.md`, `godot-engine-baseline.md` | Unreal Engine 5.8 plus Godot 4.7.x provide independently documented additional engine implementations |
| Additional ML lifecycle systems | verified representative | `domain-expansion-2026-08.md`, `ml-data-feature-orchestration.md`, `ml-monitoring-retraining-governance.md` | MLflow 3.14.0 tracking/registry/evaluation plus TFDV, Feast, KFP/Airflow and cross-vendor production monitoring/retraining-governance evidence |
| Vendor-specific embedded stacks | verified representative | `domain-expansion-2026-08.md` | ESP-IDF adds vendor-specific build/flash/monitor/debug/on-target-test evidence |
| Performance profiling / tracing / diagnostics | verified representative | `performance-profiling-tracing.md`, `performance-platform-ci.md`, `gpu-vendor-profiling.md` | Perfetto, Go pprof/PGO, JDK 26 JFR, Windows WPR/WPA/ETW, Linux `perf`/eBPF continuous profiling, Apple Instruments/`xctrace`, NVIDIA Nsight Systems/Compute, AMD ROCprofiler-SDK/`rocprofv3` + ROCm Compute Profiler, Intel VTune GPU analysis, repeated/statistical performance-CI evidence, and bounded AI-assisted interpretation |
| Supply-chain integrity / security posture / fuzzing | verified representative | `supply-chain-security-fuzzing.md` | SLSA 1.2 provenance/build levels, Sigstore/Cosign signing+attestation verification, OpenSSF Scorecard checks, OSS-Fuzz/CIFuzz, bounded LLM fuzz-target research |
| Language-native fuzzing | verified representative | `language-native-fuzzing.md`, `supply-chain-security-fuzzing.md` | LLVM libFuzzer, Go native `testing.F`, Rust `cargo-fuzz`, JVM Jazzer; corpus/failure regression preservation, bounded CI versus continuous fuzzing, and explicit platform/tool-lifecycle caveats |
| Application security / SBOM / dependency / deployment policy | verified representative | `application-security-sbom-policy.md` | SPDX 3.0 + CycloneDX 1.7 SBOM, dependency review/alerts, secret scanning, CodeQL/SARIF SAST, ZAP DAST, Falco runtime detection, OPA/Gatekeeper admission policy |
| Container/image + IaC + cloud posture + mobile AppSec | verified representative | `container-iac-cloud-mobile-security.md` | Trivy image/repository scanning, Checkov/Trivy IaC scanning, AWS Security Hub CSPM, OWASP MASVS/MASTG, bounded GitHub/GitLab AI security remediation |
| Release/deployment + rollback + progressive delivery | verified representative | `release-deployment-progressive-delivery.md` | Kubernetes rollout status/history/undo, GitHub environment gates, Argo Rollouts and Flagger metric-gated progressive delivery, bounded GitLab AI pipeline repair |
| Feature flags + database migrations + non-Kubernetes delivery | verified representative | `release-safety-flags-database-nonk8s.md` | LaunchDarkly release/kill-switch/guarded-rollout controls, Flyway migrate/validate/repair/undo boundaries, AWS CodeDeploy canary/linear/health/rollback semantics |
| Zero-downtime database schema evolution | verified representative | `zero-downtime-database-evolution.md` | Flyway/GitLab expand-contract sequencing; PostgreSQL 18, MySQL 8.4, SQL Server, and Oracle AI Database 26 operation-specific online/resumable/redefinition semantics and compatibility gates |
| Large-scale backfill + CDC-assisted migration | verified representative | `database-backfill-cdc.md` | GitLab idempotent/throttled batched backfills; Debezium incremental snapshot + CDC overlap handling; AWS DMS full-load+CDC, transactional-boundary, latency and validation caveats |
| Store/mobile + device/fleet release safety | verified representative | `store-and-fleet-release-safety.md` | Apple phased release, Google Play staged/full rollout halt semantics, AWS IoT Jobs staged/abort controls, Azure Device Update grouped OTA and automatic rollback |
| SLO / error-budget reliability governance | verified representative | `slo-error-budget-release-gates.md` | Google error-budget policy, OpenSLO SLO-as-code validation, Grafana/Datadog SLO signals, Harness direct SLO-driven deployment deny/rollback, bounded Harness AI SRE response |
| Desktop updater trust / signing / downgrade boundaries | verified representative | `desktop-update-security.md` | TUF freshness/rollback-attack defenses, Windows MSIX/App Installer signing and explicit downgrade control, Sparkle 2 signing/appcast/delta update semantics and documented absence of downgrade support |

## Still-open expansion frontier

These are deliberately not marked complete because the discovery universe is open:

- additional Apple command-line build/signing/distribution detail beyond the current representative baseline;
- additional proprietary/closed game engines and deeper Godot platform/export/testing evidence where authoritative sources are available;
- independent ML data-validation systems, feature-store alternatives, stream-first processing/orchestration, dataset lineage/versioning, feature freshness/availability SLOs, data labeling/human feedback, delayed/sparse-label monitoring, drift-to-business-impact causality, quantitative monitoring-window/sample-size policy, cross-vendor metric semantics, independent monitoring systems, and governed promotion/retraining patterns beyond the verified Azure/Vertex/AWS representatives;
- MCU/FPGA/automotive and other vendor-specific embedded ecosystems;
- additional SBOM generators/consumers and vulnerability databases;
- additional container/image scanners and cross-scanner result comparisons;
- additional multi-cloud CSPM/CNAPP implementations and concrete mobile SAST/DAST/runtime tools mapped to MASVS/MASTG;
- additional IaC scanners/policy engines and rule-coverage comparisons;
- additional fuzzing engines/ecosystems beyond the verified C/C++, Go, Rust and JVM representatives; resolution of the current first-party `cargo-fuzz` Windows-support contradiction; exact NVIDIA/AMD/Intel counter-semantic mapping, independent cross-tool profiler overhead/accuracy comparisons, current Radeon/RDNA profiling coverage, Intel graphics/game profiling replacement paths after GPA EOL, hardware-normalized/distributed performance thresholds, and robust handling of thermal/frequency/noisy-neighbor/virtualization effects;
- additional desktop updater frameworks, Windows MSI/EXE updater paths, Linux desktop/self-update mechanisms, first-class automatic post-install rollback/health recovery, additional independent OTA/fleet systems, anti-rollback/security-counter interactions, additional feature-flag implementations, and database-evolution evidence for quantitative lock/resource/lag budgets, replication/failover during schema evolution, CDC-assisted cutover/reconciliation, and additional engines beyond PostgreSQL/MySQL/SQL Server/Oracle;
- additional independent SLO/error-budget policy engines, direct verified Grafana/Datadog SLO-to-deployment-gate integrations, composite/multi-SLO release policy, and quantitative delayed/no-data gate behavior;
- app-store/fleet/desktop promotion automation that directly consumes crash/SLO/update-health evidence for promotion decisions;
- further evidence-backed AI security/fuzzing/performance/release/deployment/incident/database/ML automation, with generated outputs kept behind deterministic verification and explicit authority boundaries.
