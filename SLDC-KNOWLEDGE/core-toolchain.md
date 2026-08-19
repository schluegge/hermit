# Core software-development toolchain baseline

Verification date: 2026-08-19

## 1. Debuggers

**Definition.** A debugger executes or attaches to software while exposing program state so developers can stop, step, inspect, and continue execution.

**SDLC role.** Fault isolation during development, test failure analysis, incident reproduction, and low-level runtime diagnosis.

**Verified implementation.** Python's standard `pdb` supports breakpoints, stepping, continuing, inspection, and command-line debugging (`python -m pdb`).

**Selection criteria.** Language/runtime support; attach vs launch modes; breakpoint/step support; threads/async/process support; remote debugging; symbol/source mapping; integration with IDE/editor and test runner.

**Integration points.** Test runners, IDEs/editors, crash reproductions, CI artifacts, profilers/tracers.

**Automation.** Automated workflows can launch failing tests under a debugger or collect debugger-adjacent evidence, but interactive state interpretation must not be assumed to be reliable without validation.

Evidence: Python documentation, `pdb` — https://docs.python.org/3/library/pdb.html (official docs; verified 2026-08-19; current page observed as Python 3.14.7).

## 2. Linters and static analyzers

**Definition.** Linters/static analyzers inspect source or intermediate representations without requiring normal program execution to find correctness, suspicious, style, complexity, performance, API, or policy issues.

**SDLC role.** Fast pre-test feedback; CI quality gates; bug prevention; consistency; security/policy enforcement when supported.

**Verified implementations.** Rust Clippy provides correctness, suspicious, style, complexity, performance and other lint groups and can fail CI with `cargo clippy -- -Dwarnings`. Go `gopls` runs analyzers including `go vet` analyzers and optional Staticcheck analyzers and surfaces diagnostics through LSP.

**Selection criteria.** Precision/false-positive rate; categories covered; configurability; autofix quality; incremental speed; CI/editor integration; language-version support.

**Integration points.** Editor diagnostics, pre-commit hooks, CI, code review, build systems.

**Automation.** Run automatically on changes and CI; apply only machine-fixable suggestions under reviewable policy; preserve diagnostics as artifacts.

Evidence: Rust Clippy docs — https://doc.rust-lang.org/stable/clippy/ (official docs; verified 2026-08-19). Clippy CI — https://doc.rust-lang.org/clippy/continuous_integration/index.html. Go gopls analyzers — https://go.dev/gopls/analyzers (official docs; verified 2026-08-19).

## 3. Formatters

**Definition.** Formatters deterministically rewrite source layout to an agreed style without intentionally changing program behavior.

**SDLC role.** Eliminate style churn, reduce review noise, make generated and human-written code converge on one representation.

**Verified implementation.** `rustfmt` is the Rust formatting tool; Rust's Clippy project documentation requires rustfmt formatting before its own PRs can merge and integrates formatting via `cargo dev fmt`.

**Selection criteria.** Determinism/idempotence; language-version support; configuration stability; editor/CI integration; speed; whole-project support.

**Integration points.** Save hooks, pre-commit, CI checks, code generators.

**Automation.** Safe candidate for automatic execution; CI should verify formatting separately from semantic tests.

Evidence: Clippy development docs, rustfmt section — https://doc.rust-lang.org/clippy/development/adding_lints.html (official Rust docs; verified 2026-08-19).

## 4. Testers / test frameworks

**Definition.** Test frameworks discover, execute, isolate, and report automated checks of software behavior.

**SDLC role.** Regression prevention and verification from unit through integration/system layers.

**Verified implementation.** `cargo test` builds and runs Rust unit, integration, documentation, example and benchmark targets according to Cargo target selection.

**Selection criteria.** Test layers supported; fixtures/isolation; parallelism; deterministic reporting; coverage/tool integration; filtering; CI portability.

**Integration points.** Build system, CI, debugger, coverage, fuzzing/property testing, test environments.

**Automation.** Execute on change/PR/release gates; use targeted tests for fast feedback and broader suites for higher-confidence gates.

Evidence: Cargo Book, `cargo test` — https://doc.rust-lang.org/cargo/commands/cargo-test.html (official Rust docs; verified 2026-08-19).

## 5. Runners / build-execution layer

**Definition.** A runner is the execution layer that invokes builds, tests, tools, scripts, examples, benchmarks, or applications in a reproducible project context. This category is distinct from a CI runner host, though CI hosts often invoke project runners.

**SDLC role.** Standardizes how project tasks are executed locally and in automation.

**Verified implementation.** Cargo provides project-aware commands including build, test and Clippy integration; `cargo test` selects and builds appropriate Rust targets.

**Selection criteria.** Reproducibility; dependency/environment resolution; task graph support; cross-platform behavior; exit codes; machine-readable output; CI parity.

**Integration points.** Package manager/build system, test framework, linter, formatter, debugger, CI.

**Automation.** Expose deterministic commands that agents and CI can run without IDE-only state.

Evidence: Cargo Book, `cargo test` — https://doc.rust-lang.org/cargo/commands/cargo-test.html; Clippy usage — https://doc.rust-lang.org/stable/clippy/usage.html (official Rust docs; verified 2026-08-19).

## 6. LSP / language servers

**Definition.** Language servers provide editor-independent language intelligence over the Language Server Protocol or an equivalent editor/server interface.

**SDLC role.** Fast navigation, completion, diagnostics, analysis and refactoring feedback while editing.

**Verified implementation.** `gopls` is the official Go language server, developed by the Go team, and exposes navigation, completion, diagnostics, analysis and refactoring to LSP-compatible editors.

**Selection criteria.** Maintainer status; language-version support; diagnostics/refactoring breadth; latency; workspace/build-system support; editor compatibility.

**Integration points.** Editors/IDEs, analyzers, compiler metadata, formatting, code actions.

**Automation.** Agents may use language-server queries for symbol-aware navigation and diagnostics, but command-line interfaces can be experimental (the `gopls` CLI explicitly is).

Evidence: Go gopls — https://go.dev/gopls/ and CLI caveat https://go.dev/gopls/command-line (official Go docs; verified 2026-08-19).

## 7. Language-specific best practices

**Definition.** Practices that derive from the language's official toolchain, semantics, version policy, ecosystem conventions, or maintainers rather than generic style opinion.

**SDLC role.** Keep code aligned with supported compiler/runtime versions and idiomatic, maintained tooling.

**Verified examples.** Rust Clippy recommends using Clippy from the same toolchain used to compile the crate for compatibility. `gopls` follows the Go release policy and documents its supported Go toolchain/build-system constraints.

**Selection criteria.** Prefer official language/toolchain guidance; pin claims to versions/policies; separate mandatory correctness constraints from stylistic conventions.

**Integration points.** Repository instructions, CI matrices, linter config, package metadata, editor config.

**Automation.** Encode stable official practices in CI/config; avoid converting advisory guidance into hard gates without project intent.

Evidence: Clippy CI — https://doc.rust-lang.org/clippy/continuous_integration/index.html. Go gopls — https://go.dev/gopls/ (official docs; verified 2026-08-19).

## 8. Libraries / package ecosystems

**Definition.** Reusable software libraries plus the package metadata, dependency resolution, versioning, build and distribution ecosystem used to consume them.

**SDLC role.** Reuse, dependency management, reproducible builds, publication, ecosystem interoperability.

**Verified implementation class.** Cargo is the Rust package/build ecosystem entry point used by `cargo test` and Clippy integration; project dependencies and workspace targets are resolved through Cargo.

**Selection criteria.** Maintainer health; provenance; version compatibility; license; security posture; reproducibility/lockfiles; platform support; release cadence; API stability.

**Integration points.** Build, tests, lints, supply-chain scanning, release automation, documentation.

**Automation.** Dependency discovery/update and compatibility checks can be automated, but upgrade safety requires tests and project-specific validation.

Evidence: Cargo Book — https://doc.rust-lang.org/cargo/ (official Rust docs; verified 2026-08-19); Clippy usage — https://doc.rust-lang.org/stable/clippy/usage.html.