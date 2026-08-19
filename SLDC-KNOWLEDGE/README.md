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
- `supply-chain-security-fuzzing.md` — SLSA provenance/build guarantees, Sigstore/Cosign signing and attestations, OpenSSF Scorecard posture checks, OSS-Fuzz/CIFuzz, and bounded AI-assisted fuzzing evidence.
- `agent-protocols.md` — MCP, A2A, ACP and their distinct integration roles.
- `ai-sdlc.md` — cross-vendor AI-SDLC baseline, coding-tool taxonomy, verified automation classes, selection criteria and non-exhaustive research frontier.
- `ai-ops-memory-context.md` — AI DevOps, AI CI/CD, agent memory, and context-management baseline with cross-vendor primary evidence.
- `checkpoints/` — append-only research-run checkpoints.

## Scope

The taxonomy is intended to apply from small scripts/static websites through services, desktop/mobile applications, infrastructure, data/ML, embedded systems, and games. Product-domain-specific tooling is added only when supported by evidence.

The 18 explicitly required category baselines can be complete while discovery continues. A `complete` category is not an exhaustive catalog of every language, tool, vendor, domain, or future AI capability.

The language/domain coverage is intentionally representative rather than prescriptive. A verified implementation demonstrates how a category is realized in an ecosystem; it does not imply that the implementation is the only or universally best choice for that ecosystem.
