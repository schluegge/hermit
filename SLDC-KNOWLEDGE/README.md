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

- `COVERAGE.md` — finite required-category audit and completion criteria.
- `core-toolchain.md` — language-agnostic baseline for debugging, linting/static analysis, formatting, testing, runners/build execution, LSP, best practices, and package/library ecosystems.
- `agent-protocols.md` — MCP, A2A, ACP and their distinct integration roles.
- `ai-sdlc.md` — verified AI-assisted SDLC capabilities and unresolved coverage.
- `checkpoints/` — append-only research-run checkpoints.

## Scope

The taxonomy is intended to apply from small scripts/static websites through services, desktop/mobile applications, infrastructure, data/ML, embedded systems, and games. Product-domain-specific tooling is added only when supported by evidence.