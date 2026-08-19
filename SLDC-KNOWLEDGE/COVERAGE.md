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
| AI-SDLC | partial | `ai-sdlc.md` | Verified examples exist; cross-vendor lifecycle baseline still incomplete |
| Tools that help AI code | partial | `ai-sdlc.md` | Verified GitHub capabilities exist; broader representative set pending |
| AI DevOps | partial | `ai-sdlc.md` | Some automation stages verified; operations/deployment baseline incomplete |
| AI CI/CD | partial | `ai-sdlc.md` | CI-linked review/runner evidence verified; generalized CI/CD model incomplete |
| Memory | partial | `ai-sdlc.md` | Category defined; durable/episodic/semantic implementations need primary-source comparison |
| Context management | partial | `ai-sdlc.md`, `agent-protocols.md` | MCP and repository-context mechanisms verified; general selection guidance incomplete |
| MCP | complete | `agent-protocols.md` | Current official protocol role, primitives, transport direction, selection/integration documented |
| A2A | complete | `agent-protocols.md` | Official v1.0 role, interoperability scope, selection/integration documented |
| ACP | complete | `agent-protocols.md` | Official Zed role, editor-agent interoperability and selection/integration documented |
| AI-driven automation | partial | `ai-sdlc.md` | Verified coding/review/test/lint/context automation; open-ended SDLC discovery remains ongoing |

## Finite Definition of Done

A required category may be marked `complete` only when all six are present and evidenced:

1. Baseline definition.
2. Role in the SDLC.
3. Representative verified tool classes or implementations.
4. Selection criteria.
5. Integration points.
6. Relevant automation possibilities.

This table covers all 18 named required categories. Coverage of the names is finite; discovery of additional tools and AI automation capabilities is intentionally open-ended.