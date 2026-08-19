# Required-category coverage

Verification date: 2026-08-19

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
| AI-driven automation | complete | `ai-sdlc.md`, `ai-ops-memory-context.md`, `agent-protocols.md`, `supply-chain-security-fuzzing.md` | Finite baseline has definition, lifecycle role, representative verified classes, selection, integration and automation possibilities; open-ended capability discovery explicitly remains non-exhaustive |

## Finite Definition of Done

A required category may be marked `complete` only when all six are present and evidenced:

1. Baseline definition.
2. Role in the SDLC.
3. Representative verified tool classes or implementations.
4. Selection criteria.
5. Integration points.
6. Relevant automation possibilities.

## Completion status

**18 / 18 named required categories satisfy the finite baseline Definition of Done as of 2026-08-19.**

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
| Data / ML | verified representative | `language-domain-matrix.md`, `domain-expansion-2026-08.md` | PyTorch profiling plus MLflow experiment tracking, model registry and evaluation |
| Games | verified representative | `language-domain-matrix.md`, `domain-expansion-2026-08.md` | Unity testing/profiler plus Unreal automation testing/build automation |
| Additional game engines | verified representative | `domain-expansion-2026-08.md` | Unreal Engine 5.8 adds a second independently documented engine implementation |
| Additional ML lifecycle systems | verified representative | `domain-expansion-2026-08.md` | MLflow 3.14.0 adds tracking, registry, lineage and evaluation lifecycle evidence |
| Vendor-specific embedded stacks | verified representative | `domain-expansion-2026-08.md` | ESP-IDF adds vendor-specific build/flash/monitor/debug/on-target-test evidence |
| Supply-chain integrity / security posture / fuzzing | verified representative | `supply-chain-security-fuzzing.md` | SLSA 1.2 provenance/build levels, Sigstore/Cosign signing+attestation verification, OpenSSF Scorecard checks, OSS-Fuzz/CIFuzz, bounded LLM fuzz-target research |

## Still-open expansion frontier

These are deliberately not marked complete because the discovery universe is open:

- additional Apple command-line build/signing/distribution detail beyond the current representative baseline;
- additional game engines such as Godot and proprietary engines;
- ML data validation, feature stores and additional orchestration/lifecycle systems;
- MCU/FPGA/automotive and other vendor-specific embedded ecosystems;
- SBOM generation/consumption, dependency vulnerability policy, secret scanning, runtime/application security and deployment-policy implementations beyond the representative supply-chain baseline;
- additional fuzzing systems, language-native fuzzers, profiling and deployment systems;
- further evidence-backed AI security/fuzzing/release/deployment automation, with generated outputs kept behind deterministic verification gates.
