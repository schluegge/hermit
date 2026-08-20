# Language-native fuzzing baseline

Verification date: 2026-08-20

This file extends the existing fuzzing baseline with representative language/toolchain-native implementations. It is intentionally language-agnostic at the process level: fuzz targets, corpus/seeds, instrumentation, execution budget, failure artifact, reproduction, minimization and regression preservation are separate evidence planes regardless of implementation language. It does not claim that these four implementations exhaust the fuzzing ecosystem.

## 1. Baseline definition and SDLC role

Language-native or ecosystem-native fuzzing integrates coverage-guided or mutation-driven input generation with the language's normal build/test/package workflow. Its SDLC role is to explore input/state spaces that example-based tests may miss, preserve discovered failures as regression artifacts, and provide reproducible evidence for debugging and security/stability remediation.

A useful baseline separates:

1. **Target/harness** — the deterministic entrypoint that turns generated data into behavior under test.
2. **Seed/corpus** — known inputs used to bootstrap or replay exploration.
3. **Instrumentation/guidance** — coverage or comparison signals that steer mutations.
4. **Execution budget** — time/iterations/workers; a bounded run is evidence only for that run.
5. **Failure artifact** — crashing/failing input plus diagnostics.
6. **Reproduction/minimization** — prove the failure is repeatable and reduce the input when supported.
7. **Regression preservation** — keep the discovered case in normal tests/corpus so the fix remains checked.
8. **Long-running fuzzing** — CI smoke fuzzing and continuous fuzzing are complementary, not equivalent.

A green fuzz run is never proof that no defect exists. Evidence is limited by target quality, reachable code, corpus, instrumentation, sanitizer coverage, platform, runtime budget and nondeterminism.

## 2. C/C++ — LLVM libFuzzer

### Verified implementation

LLVM documents libFuzzer as an in-process, coverage-guided evolutionary fuzzing engine. A target exposes `LLVMFuzzerTestOneInput`; the engine mutates corpus inputs and uses SanitizerCoverage feedback to retain inputs that reach new behavior. Clang can link libFuzzer with `-fsanitize=fuzzer`, commonly combined with AddressSanitizer and/or UndefinedBehaviorSanitizer.

The official documentation recommends fuzz targets that are fast, deterministic, tolerant of malformed inputs and free of persistent state where possible. Crash/sanitizer artifacts are written to disk, corpus minimization is supported, and saved inputs can be replayed without generating new mutations for regression use.

### Lifecycle/status caveat

LLVM currently states that libFuzzer's original authors stopped active feature work and moved to Centipede. Important bugs are still expected to be fixed, but major new features or non-bugfix code review should not be expected. libFuzzer also requires a matching Clang version. Therefore it remains a supported implementation, but not an actively feature-expanding engine baseline.

### Selection and integration criteria

Use libFuzzer when the code can expose a fast in-process byte-oriented target and Clang/SanitizerCoverage integration is acceptable. Pair memory-unsafe native code with appropriate sanitizers. Prefer narrow deterministic targets and preserve crash inputs as regression evidence. For long-running or fleet-scale fuzzing, use a continuous service/framework rather than treating a short local run as sufficient.

### Automation possibilities

- build fuzz targets with compiler instrumentation and sanitizers;
- run bounded PR smoke fuzzing and longer scheduled/continuous fuzzing;
- persist corpus and crash artifacts;
- automatically replay/minimize failures;
- fail CI only on reproducible qualifying findings according to project policy.

### Primary sources — verified 2026-08-20

- LLVM libFuzzer documentation (official project documentation): https://llvm.org/docs/LibFuzzer.html
- LLVM SanitizerCoverage documentation (official project documentation): https://clang.llvm.org/docs/SanitizerCoverage.html

## 3. Go — native `testing.F` fuzzing

### Verified implementation

Go supports fuzzing in the standard toolchain beginning with Go 1.18. Fuzz tests are `FuzzXxx` functions in `_test.go` files and execute through `go test`. In normal test mode, seed-corpus and previously discovered failing inputs are replayed; fuzzing mode is enabled with `go test -fuzz=...`.

The Go documentation states that fuzzing is coverage-guided. When a failing input is found, the tool writes it into the fuzz test's seed corpus; after a fix, the same input is run by ordinary `go test`, turning a discovered fuzz failure into regression evidence. Execution can be bounded with `-fuzztime`; worker count is controlled with `-parallel`.

### Platform scope

Current Go documentation states that coverage-instrumented fuzzing is available on AMD64 and ARM64. This is a material execution constraint for CI/runner selection and must not be generalized to every Go-supported architecture.

### Selection and integration criteria

Prefer native Go fuzzing when the project already uses `go test` and target inputs fit the supported fuzz argument types. Keep targets fast, deterministic and independent of persistent global state. Use the normal unit-test path to replay seeds/failures, and use OSS-Fuzz or another continuous system when bounded local/CI fuzzing is insufficient.

### Automation possibilities

- execute fuzz targets through the normal Go test runner;
- bound PR fuzzing with `-fuzztime`;
- store failing inputs under `testdata/fuzz` as regression cases;
- parallelize within supported architectures;
- promote selected projects to continuous fuzzing without rewriting the target model.

### Primary sources — verified 2026-08-20

- Go fuzzing documentation (official language documentation): https://go.dev/doc/security/fuzz/
- Go fuzzing tutorial (official language documentation): https://go.dev/doc/tutorial/fuzz

## 4. Rust — `cargo-fuzz` / libFuzzer

### Verified implementation

The Rust Fuzz Book describes `cargo-fuzz` as the recommended Rust fuzz-testing tool and explains that `cargo-fuzz` is a Cargo helper around libFuzzer through `libfuzzer-sys`. The current maintainer release page identifies `cargo-fuzz` 0.13.2 as the latest release, dated 2026-06-09. The current changelog records a new `--fuzz-engine` option for `cargo fuzz init`, but the current Fuzz Book still describes libFuzzer as the supported engine; no broader engine-compatibility claim is made here.

The maintained workflow includes `cargo fuzz init`, target creation, `cargo fuzz run`, crash-input minimization (`tmin`), corpus minimization (`cmin`) and coverage generation. The Rust Fuzz Book also documents bounded CI smoke fuzzing and artifact upload on failure.

### Required toolchain caveat

Current maintainer material consistently requires a nightly Rust toolchain because sanitizer-related compiler flags are unstable.

### Unresolved platform contradiction

Current primary maintainer sources conflict on Windows support:

- the `rust-fuzz/cargo-fuzz` repository README says libFuzzer support works on x86-64/AArch64 Unix-like systems **and not Windows**;
- the Rust Fuzz Book setup page says sanitizer support works on x86-64 Linux, x86-64 macOS, Apple-Silicon macOS **and Windows via MSVC AddressSanitizer**.

Because both are first-party maintained sources and the discrepancy was not independently resolved in this run, Windows support for the current `cargo-fuzz` baseline is **unresolved**. Do not encode Windows compatibility into automated environment selection until a reproducible current test or maintainer clarification resolves it.

### Selection and integration criteria

Use `cargo-fuzz` when Rust code can be isolated into deterministic fuzz targets and nightly/libFuzzer dependencies are acceptable. Pin the `cargo-fuzz` version in CI, retain crash artifacts, and treat bounded CI execution as a smoke test rather than continuous-coverage proof.

### Automation possibilities

- generate/build fuzz targets from Cargo workflows;
- run time-bounded fuzz jobs in CI;
- upload crash artifacts automatically;
- minimize failing inputs and corpora;
- generate coverage reports;
- feed the same targets into longer-running fuzzing where supported.

### Primary sources — verified 2026-08-20

- Rust Fuzz Book, `cargo-fuzz` (maintainer documentation): https://rust-fuzz.github.io/book/cargo-fuzz.html
- Rust Fuzz Book setup (maintainer documentation): https://rust-fuzz.github.io/book/cargo-fuzz/setup.html
- Rust Fuzz Book CI guidance (maintainer documentation): https://rust-fuzz.github.io/book/cargo-fuzz/ci.html
- `rust-fuzz/cargo-fuzz` repository README (maintainer repository): https://github.com/rust-fuzz/cargo-fuzz
- `cargo-fuzz` changelog (maintainer repository): https://github.com/rust-fuzz/cargo-fuzz/blob/main/CHANGELOG.md
- `cargo-fuzz` releases (maintainer repository): https://github.com/rust-fuzz/cargo-fuzz/releases

## 5. JVM — Jazzer + JUnit

### Verified implementation

Jazzer is a coverage-guided in-process JVM fuzzer maintained by Code Intelligence and based on libFuzzer concepts. Current maintainer documentation supports Linux x86_64/arm64, macOS 12+ x86_64/arm64 and Windows x86_64. The recommended integration uses `jazzer-junit` with JUnit 5.9.0 or newer and works with Maven, Gradle and Bazel.

A method annotated with `@FuzzTest` can run in two modes:

- **regression mode** (default in JUnit integration): replay stored crashing inputs like ordinary tests;
- **fuzzing mode** (`JAZZER_FUZZ=1`): generate/mutate inputs to increase coverage and discover failures.

New coverage inputs are stored in a generated corpus; failing inputs are stored for later replay. This gives a direct path from discovery to regression preservation. Jazzer also exposes instrumentation/hooks and optional sanitizer-style bug detectors for selected JVM vulnerability classes.

The current maintainer release page identifies Jazzer v0.30.0 as the latest release observed in this run. Version-specific behavior must still be pinned in reproducible CI rather than relying on an unversioned `LATEST` dependency.

### Selection and integration criteria

Use Jazzer when JVM code can run under its instrumentation model and JUnit/build-tool integration is desirable. Prefer JUnit regression mode for normal CI replay and explicitly opt into bounded fuzzing jobs. Pin the Jazzer version and preserve failing inputs with the test sources/resources.

### Automation possibilities

- run replay/regression fuzz tests inside ordinary Maven/Gradle/Bazel test jobs;
- enable bounded fuzzing as a dedicated CI job;
- persist generated corpus/crash inputs;
- use instrumentation/hooks to surface selected security-relevant behavior;
- integrate eligible JVM targets with OSS-Fuzz for longer-running fuzzing.

### Primary sources — verified 2026-08-20

- Jazzer maintainer repository/documentation: https://github.com/CodeIntelligenceTesting/jazzer
- Jazzer arguments/configuration: https://github.com/CodeIntelligenceTesting/jazzer/blob/main/docs/arguments-and-configuration-options.md
- Jazzer releases: https://github.com/CodeIntelligenceTesting/jazzer/releases

## 6. Cross-language selection matrix

| Need | Representative implementation | Integration plane | Material constraint |
|---|---|---|---|
| Native C/C++ in-process coverage-guided fuzzing | LLVM libFuzzer | Clang + SanitizerCoverage + sanitizers | matching Clang; maintenance/bugfix-oriented lifecycle |
| Go project with standard-toolchain tests | Go `testing.F` | `go test` | coverage fuzzing currently AMD64/ARM64 |
| Rust Cargo project | `cargo-fuzz` | Cargo + nightly + libFuzzer | nightly required; Windows support unresolved from conflicting maintainer docs |
| JVM/JUnit project | Jazzer | JUnit/Maven/Gradle/Bazel | pin current Jazzer/JUnit/platform support |

Selection should follow project language/runtime, target shape, sanitizer/instrumentation requirements, platform constraints, reproducibility needs and whether bounded CI or continuous fuzzing is required. Do not select a fuzzer solely because it reports a coverage percentage; different instrumentation and target boundaries can make raw percentages non-comparable.

## 7. Integration with the existing continuous/AI fuzzing baseline

This file does not replace `supply-chain-security-fuzzing.md`:

- this file defines representative language/ecosystem-native target and runner integrations;
- `supply-chain-security-fuzzing.md` covers OSS-Fuzz/CIFuzz continuous execution and bounded LLM-assisted target generation/fix proposals.

A safe automation chain is:

`language-native target -> deterministic build/instrumentation -> bounded CI replay/fuzz -> persist reproducer -> continuous fuzzing where justified -> deterministic fix/regression gates`.

AI may propose targets or fixes where independently supported, but compiler/test/sanitizer/fuzz/reproduction evidence remains authoritative. No language-native tool documented here grants AI release or merge authority.

## Contradiction / deduplication boundaries

- libFuzzer remains supported for important fixes but is not an actively feature-expanding LLVM fuzzer; do not describe it as under active feature development.
- Go native fuzzing and OSS-Fuzz are complementary: local/CI `go test -fuzz` does not imply continuous OSS-Fuzz service coverage.
- `cargo-fuzz` is a Cargo integration/helper; the current baseline still routes actual fuzz execution through libFuzzer.
- `cargo-fuzz` Windows compatibility is unresolved because current first-party sources disagree.
- Jazzer's regression mode replays known findings; fuzzing mode performs exploration. A passing regression run says nothing about unexplored inputs.
- Language-native fuzzing does not replace property tests, unit/integration tests, static analysis or security review.
- No raw coverage number is treated as a cross-tool quality score without matching target and instrumentation semantics.
