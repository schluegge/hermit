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
| AI-driven automation | complete | `ai-sdlc.md`, `ai-ops-memory-context.md`, `agent-protocols.md` | Finite baseline has definition, lifecycle role, representative verified classes, selection, integration and automation possibilities; open-ended capability discovery explicitly remains non-exhaustive |

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
