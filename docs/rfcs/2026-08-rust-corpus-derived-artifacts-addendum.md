# Addendum: Generated, Embedded, and Compiled Rust Artifacts

Status: Draft roadmap extension  
Date: 2026-08-14  
Parent: `2026-08-rust-corpus-completion-roadmap.md`

## Why this addendum exists

If Hermit's goal is to capture Rust code "in any form", a corpus of checked-in `.rs` files is insufficient.

A meaningful amount of Rust exists only after packaging, code generation, macro expansion, build-script execution, or compilation. Rust can also be embedded inside packages whose primary ecosystem is Python, JavaScript, Java, .NET, Ruby, Conda, Linux distributions, containers, or firmware.

Therefore Hermit must distinguish **authored source**, **published source**, **generated source**, **expanded source**, **compiler-derived representations**, and **compiled evidence** instead of treating all of them as the same artifact.

## Artifact layers

### R0 — authored repository source

Examples:

- checked-in `.rs` files
- Cargo manifests
- tests/examples/benches
- compiler tests
- documentation code blocks

This is the ordinary source corpus described by the parent RFC.

### R1 — published source artifacts

Published packages can differ from their upstream repository.

Examples:

- crates.io `.crate` contents
- source release archives
- distro source packages
- vendored dependency archives
- source distributions from non-Rust package registries

Hermit must compare R1 against R0 and retain publication-only files and modifications.

### R2 — embedded Rust fragments

Rust may be embedded in artifacts whose container is not itself a Rust repository.

Examples:

- Markdown/RST/AsciiDoc fenced code
- HTML `<code>` blocks
- notebooks
- issue/PR/forum snippets
- book/course examples
- shell scripts containing heredoc-generated `.rs`
- templates that emit Rust
- test fixtures

The container artifact and exact block coordinates must remain part of provenance.

### R3 — generated Rust source

Rust source can be produced during configuration/build time and never exist in the repository or published archive.

Common generators include:

- `build.rs`
- bindgen
- protobuf/gRPC generators
- FlatBuffers/Cap'n Proto generators
- OpenAPI generators
- parser generators
- shader/GPU binding generators
- Windows/COM/API binding generators
- database/schema codegen
- template engines
- project-specific generators

Capture requirements:

- generator identity/version
- exact source revision/package version
- toolchain
- target triple
- Cargo features
- environment inputs
- generator inputs and hashes
- generated output path
- generated blob hash
- sandbox/run receipt

Generated code is a derived artifact. Never pretend it was authored upstream.

### R4 — macro-expanded Rust

Declarative macros and proc macros can create substantial code that does not exist textually in the source corpus.

Capture, where technically feasible:

- `macro_rules!` expansion products
- derive macro expansions
- attribute macro expansions
- function-like proc-macro expansions
- expansion call-site provenance
- macro definition provenance
- compiler/toolchain version
- cfg/feature/target context

Expansion output must be keyed by all relevant inputs because the same source can expand differently under features, targets, compiler versions, and environment configuration.

### R5 — compiler-derived representations

These are not raw Rust source but are essential for semantic deduplication and understanding.

Candidate representations:

- token stream
- parsed AST
- expanded AST
- HIR
- THIR where available/useful
- MIR
- borrow-checker facts where exposed
- monomorphization/codegen-unit metadata
- rustdoc JSON/API representations
- rust-analyzer semantic graph

Every representation must preserve the producing toolchain/version and source-artifact identity.

### R6 — compiled Rust evidence

Public binaries may preserve evidence that is absent from available source snapshots.

Examples:

- executables
- dynamic/static libraries
- `.rlib`
- `.rmeta`
- WASM modules
- Python wheels with Rust extensions
- Node native addons
- Android/iOS binaries
- distro binary packages
- container-image layers
- firmware where legally accessible

Extract only evidence that can be obtained lawfully and reproducibly, such as:

- build IDs
- target/architecture
- debug information
- symbol names
- source paths
- crate/package metadata
- panic strings
- compiler/version markers
- dependency fingerprints
- section metadata
- exported ABI
- reproducible-build linkage to known source

Do not label reconstructed/decompiled pseudocode as original Rust source.

### R7 — inferred/reconstructed code

Binary analysis or models may infer higher-level representations.

This must be quarantined from the source corpus and labeled explicitly as inference.

Required fields:

- inference method/tool/model/version
- source binary hash
- confidence
- validation evidence
- known ambiguity

Inferred code can support discovery and clone matching but can never replace original-source evidence.

## Cross-ecosystem package registries

Rust frequently ships through registries other than crates.io. Add source/artifact discovery adapters for at least the following classes:

- PyPI: sdists and wheels, especially maturin/PyO3 packages
- npm: source packages, native addons, napi-rs, Neon, WASM packages
- Maven Central and other JVM registries: JNI/native bundles and source artifacts
- NuGet: native Rust libraries/tools and source packages
- RubyGems: native extensions
- Conda/conda-forge packages and recipes
- Homebrew source references/bottles
- vcpkg ports/source references
- Conan packages/recipes
- Linux distribution source and binary package repositories
- container registries where public images contain Rust source/build artifacts

For each package, preserve both the foreign ecosystem's identity and the underlying Rust crate/repository identity when the relationship can be proven.

## Whole-history requirement

Default branches are not sufficient.

For Git-backed origins, the target evidence universe includes, subject to access and policy:

- all advertised branches
- all tags/releases
- complete reachable commit history
- submodules
- LFS-backed source artifacts where applicable
- publication commits if identifiable
- deleted upstream history preserved by archival sources

Do not multiply physical storage for identical blobs; retain every revision/path occurrence.

## Build-state explosion

Generated and expanded Rust is configuration-dependent. A naive Cartesian product of every toolchain, target, feature set, and environment is unbounded.

Use a tiered state strategy:

1. declared/default build state
2. all explicitly documented CI states
3. all published target/feature states visible in metadata
4. coverage-guided feature/target expansion
5. representative pairwise/combinatorial states
6. exhaustive state enumeration only when the state space is demonstrably finite and tractable

Store untested states explicitly. Never infer that one successful build represents all feature/target combinations.

## Reproducibility manifests

Every derived R3-R7 artifact should be addressable through a manifest containing:

- raw input hashes
- source provenance IDs
- toolchain/tool hashes and versions
- configuration/features/target
- environment variables admitted into the sandbox
- network policy
- execution limits
- command/action identity
- output hashes
- logs
- timestamp

Where possible, produce a Merkle-rooted snapshot manifest over each completed source-universe snapshot so corpus state can be independently verified.

## Hostile-input threat model

Internet-scale ingestion must assume malicious inputs.

Before scaling, implement defenses for:

- archive path traversal
- decompression bombs
- recursive archives
- malformed Git objects
- parser complexity attacks
- oversized files
- malicious Unicode/path tricks
- symlink escapes
- build-script/proc-macro arbitrary code execution
- network exfiltration attempts
- filesystem probing
- fork bombs/resource exhaustion
- compiler/tool crashes
- malicious generated output

Raw acquisition, parsing, and execution need progressively stronger isolation boundaries. Merely "running cargo check" is not a safe ingestion strategy.

## Additional roadmap gates

### Gate A — cross-ecosystem discovery

Prove that Hermit can discover the same Rust project independently through crates.io and at least one foreign package ecosystem and reconcile both to shared source provenance.

### Gate B — generated-source capture

Select representative projects using `build.rs`, bindgen, schema/code generators, and proc macros. Capture generated/expanded Rust with deterministic manifests.

### Gate C — macro expansion corpus

Build item-level provenance from macro invocation -> macro definition -> expanded items for a controlled benchmark set, then scale.

### Gate D — compiled-artifact linkage

Link a known public compiled artifact to exact or candidate source revisions using reproducible evidence. Preserve uncertainty where exact linkage is impossible.

### Gate E — hostile-input validation

Run an adversarial fixture suite proving archive/parser/build isolation before any untrusted bulk execution.

## New hard invariants

1. Checked-in `.rs` files are only one Rust artifact layer.
2. Published package content is independently authoritative evidence and may differ from Git.
3. Generated and macro-expanded code must preserve the exact state that produced it.
4. Compiler IR and binaries are derived evidence, not raw source.
5. Decompiled/inferred code is never represented as original source.
6. Default-branch-only ingestion can never satisfy repository-history completeness.
7. Arbitrary build scripts and proc macros execute only in hardened isolation.
8. Cross-ecosystem package identities are preserved rather than flattened into crates.io identities.
9. Every derived artifact must be reproducible from an explicit manifest or marked non-reproducible with reason.
