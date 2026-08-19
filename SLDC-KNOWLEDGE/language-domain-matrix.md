# Language and domain toolchain matrix

Verification date: 2026-08-19

Purpose: extend the language-agnostic baseline with representative, currently documented implementations for software ecosystems and product domains that were not covered in the initial Rust/Go/Python examples. This is an evidence-backed expansion, not an exhaustive catalog.

## 1. JavaScript / TypeScript / Node.js

**Baseline role.** Covers browser/server JavaScript and TypeScript projects, from small scripts/static-site tooling to services and application backends.

**Verified toolchain components.** TypeScript `tsc` is the project-aware compiler CLI and can build projects from `tsconfig.json`; the TypeScript standalone server `tsserver` wraps compiler/language-service capabilities for editor/IDE use. Node.js 26.7.0 documents a stable built-in `node:test` runner with filtering, watch mode, coverage, mocking, snapshots, reporters, rerun-failure state and non-zero failure exit codes. Node.js also includes the `node inspect` command-line debugger.

**Selection/integration criteria.** Pin the runtime/compiler version used by CI; keep compiler/typechecking separate from runtime tests; expose test and typecheck commands through project scripts; use editor language services only as an acceleration layer, not as the sole CI verifier.

**Automation possibilities.** Agents/CI can run `tsc`, Node tests and debugger/probe workflows; deterministic exit codes make compilation and tests suitable as gates. `tsserver` is useful for editor/symbol context but is not equivalent to a full build/test pass.

Evidence:
- TypeScript `tsc` CLI — https://www.typescriptlang.org/docs/handbook/compiler-options.html (official TypeScript docs; verified 2026-08-19).
- TypeScript standalone server — https://github.com/microsoft/TypeScript/wiki/Standalone-Server-%28tsserver%29 (maintainer documentation; verified 2026-08-19).
- Node.js test runner v26.7.0 — https://nodejs.org/api/test.html (official Node.js docs; verified 2026-08-19).
- Node.js debugger v26.7.0 — https://nodejs.org/api/debugger.html (official Node.js docs; verified 2026-08-19).

## 2. JVM / Java

**Baseline role.** Covers JVM services, command-line applications, desktop/server software and libraries.

**Verified toolchain components.** JDK 26 documents `javac` for compilation, `jdb` for debugging, JShell as a REPL/prototyping tool, dependency-analysis tooling in `jdk.jdeps`, Java Debug Interface/JDWP support, and JDK Flight Recorder APIs. Current JUnit documentation resolves to JUnit 6.1.3; JUnit Platform launches JVM test frameworks and provides a command-line Console Launcher plus build-tool/IDE integrations.

**Selection/integration criteria.** Pin the JDK/toolchain version; choose a build system independently of the test framework; keep tests executable from command line/CI; use JFR/JVM diagnostics for performance/runtime evidence instead of guessing from source structure.

**Automation possibilities.** Compile, test, package and diagnostic collection are suitable for CI/agent execution; JShell is exploratory and must not substitute for repository tests. Debugger/profiler evidence should be preserved when used for failure or performance claims.

Evidence:
- JDK 26 documentation index — https://docs.oracle.com/en/java/javase/26/index.html (Oracle official docs; verified 2026-08-19).
- `javac` — https://docs.oracle.com/en/java/javase/26/docs/specs/man/javac.html (Oracle official docs; verified 2026-08-19).
- `jdb` — https://docs.oracle.com/en/java/javase/26/docs/specs/man/jdb.html (Oracle official docs; verified 2026-08-19).
- JShell — https://docs.oracle.com/en/java/javase/26/jshell/ (Oracle official docs; verified 2026-08-19).
- JUnit 6.1.3 overview — https://docs.junit.org/current/user-guide/ (JUnit project docs; verified 2026-08-19).

## 3. C / C++

**Baseline role.** Covers native applications, systems software, libraries, performance-sensitive software, game engines and embedded/native components.

**Verified toolchain components.** LLVM documents `clang-tidy` as an extensible C++ linter/static-analysis framework with automated parallel and diff-oriented runners; `clang-format` formats C/C++ and related languages; `clangd` provides language-server functionality; LLDB provides native debugging. CMake/CTest supply build-system integration and a command-line test driver with deterministic failure exit status.

**Selection/integration criteria.** Preserve the real compile command database (`compile_commands.json`) for semantic tooling; choose compiler/debugger by target/platform support; separate format/lint/test gates; do not use diff-only static analysis as the only full verification because Clang explicitly documents that changed-line reporting can miss diagnostics caused elsewhere.

**Automation possibilities.** Generate compile databases, run `clang-tidy` in parallel, verify formatting, build with CMake and execute CTest in CI/agents. Full-project or affected-file analysis should remain available for merge/release gates.

Evidence:
- clang-tidy — https://clang.llvm.org/extra/clang-tidy/ (LLVM official docs; verified 2026-08-19; page currently built from 24.0.0git docs).
- clang-format — https://clang.llvm.org/docs/ClangFormat.html (LLVM official docs; verified 2026-08-19).
- clangd — https://clangd.llvm.org/ (LLVM official docs; verified 2026-08-19).
- LLDB — https://lldb.llvm.org/ (LLVM official docs; verified 2026-08-19).
- CTest — https://cmake.org/cmake/help/latest/manual/ctest.1.html (CMake official docs; verified 2026-08-19; current page observed as CMake 4.4.2).

## 4. .NET / C#

**Baseline role.** Covers services, desktop applications, libraries, tooling and cross-platform .NET software.

**Verified toolchain components.** `.NET` includes Roslyn analyzers in the SDK for C#/VB quality/style analysis; `dotnet format` applies EditorConfig formatting/static-analysis recommendations and can verify no changes with non-zero failure; `dotnet test` builds and executes tests through VSTest or Microsoft Testing Platform depending on configuration/version.

**Selection/integration criteria.** Pin SDK and target frameworks; configure analyzer severity deliberately; keep formatting verification separate from semantic tests; record test-platform choice because .NET 10 adds explicit runner selection while earlier SDKs use VSTest through `dotnet test`.

**Automation possibilities.** `dotnet format --verify-no-changes`, analyzers and `dotnet test` are command-line CI/agent gates. Treat automatic analyzer fixes as reviewable changes because formatter/analyzer execution can load trusted project/build components.

Evidence:
- .NET code analysis — https://learn.microsoft.com/en-us/dotnet/fundamentals/code-analysis/overview (Microsoft official docs; verified 2026-08-19).
- `dotnet format` — https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-format (Microsoft official docs; verified 2026-08-19).
- `dotnet test` — https://learn.microsoft.com/en-us/dotnet/core/tools/dotnet-test (Microsoft official docs; verified 2026-08-19).

## 5. Mobile — Android

**Distinct lifecycle needs.** Mobile adds build variants, packaging/signing, emulator/physical-device execution, instrumentation tests, platform/API compatibility and device performance profiling.

**Verified toolchain components.** Android applications are typically built with Gradle plus the Android Gradle Plugin (AGP); Android Lint provides static checks for correctness, security, performance, usability, accessibility and internationalization; tests can run from IDE or command line including instrumented/device configurations; Android Studio Profiler records CPU/memory/graphics/battery-related performance evidence.

**Automation possibilities.** Use the Gradle wrapper for reproducible build/lint/test tasks; run `gradlew lint` explicitly in CI because Android documentation states lint is not automatically run as part of every build; run emulator/device matrices where platform behavior matters; preserve profiler traces for performance claims.

Evidence:
- Gradle build overview — https://developer.android.com/build/gradle-build-overview (Android official docs; updated 2026-08-04; verified 2026-08-19).
- Android Lint — https://developer.android.com/studio/write/lint (Android official docs; verified 2026-08-19).
- Android testing — https://developer.android.com/studio/test (Android official docs; verified 2026-08-19).
- Android profiling — https://developer.android.com/studio/profile (Android official docs; updated 2026-03-06; verified 2026-08-19).

## 6. Embedded / hardware-in-the-loop — Zephyr example

**Distinct lifecycle needs.** Embedded systems add cross-compilation, board configuration, flashing, target/debug probes, emulation/simulation and physical-device test orchestration.

**Verified toolchain components.** Zephyr `west build`, `west flash`, `west debug`, `west debugserver` and `west attach` cover build/target/debug workflows. Twister discovers/builds/runs test applications across board configurations, simulation/emulation and real hardware, can use hardware maps, and produces result artifacts such as `twister.json`.

**Automation possibilities.** Run build-only matrices early, simulation/emulation when available, then device testing/HIL for target-specific behavior. Hardware maps can drive multiple devices. Zephyr explicitly states Twister's default coverage cannot guarantee success in the entire build environment, so HIL/simulation evidence must not be generalized beyond the tested matrix.

Evidence:
- Zephyr build/flash/debug — https://docs.zephyrproject.org/latest/develop/west/build-flash-debug.html (Zephyr official docs; verified 2026-08-19).
- Zephyr Twister — https://docs.zephyrproject.org/latest/develop/test/twister.html (Zephyr official docs; verified 2026-08-19).

## 7. Data / ML — PyTorch example

**Distinct lifecycle needs.** Data/ML software adds model/data versioning concerns, accelerator/runtime variability, numerical/performance verification and training/inference profiling beyond ordinary unit tests.

**Verified toolchain component.** `torch.profiler` collects execution/performance metrics for training and inference, including operator cost, shapes, stacks, device kernel activity and execution traces; PyTorch distributed documentation also supports profiling collective communication.

**Automation possibilities.** Agents/CI can run deterministic code tests plus bounded model/data checks and capture profiler traces for regressions. Performance conclusions should be tied to hardware/runtime/input conditions; a profiler trace is evidence for the measured workload, not all workloads.

Evidence:
- PyTorch profiler — https://docs.pytorch.org/docs/main/profiler (PyTorch official docs; updated 2026-05-11; verified 2026-08-19).
- PyTorch distributed profiling — https://docs.pytorch.org/docs/stable/distributed.html (PyTorch official docs; verified 2026-08-19).

## 8. Games — Unity example

**Distinct lifecycle needs.** Games add frame-time/rendering/physics performance, play-mode/editor-mode behavior, platform builds, asset/content pipelines and engine-specific test harnesses.

**Verified toolchain components.** Unity 6 documentation exposes the Unity Test Framework/performance testing package and the Unity Profiler for frame/module inspection and performance evidence.

**Automation possibilities.** Run engine-supported tests and performance tests as separate gates; collect profiler captures for frame-time/performance investigations; do not infer runtime performance from successful compilation or unit tests.

Evidence:
- Unity performance testing API — https://docs.unity3d.com/6000.0/Manual/com.unity.test-framework.performance.html (Unity official docs; Unity 6.0 / package 3.2.0 observed; verified 2026-08-19).
- Unity Profiler navigation — https://docs.unity3d.com/6000.0/Manual/profiler-window-navigating.html (Unity official docs; Unity 6.0; verified 2026-08-19).

## Cross-domain baseline derived from the verified matrix

The common SDLC categories remain stable across ecosystems: build/runner, debugger, static analysis/lint, formatter/style enforcement, test execution, language/editor intelligence, dependencies/packages, performance/profiling, and CI/release integration. Product domains add **extra evidence surfaces** rather than replacing the baseline: Android adds variant/device/instrumentation evidence; embedded adds board/emulator/HIL evidence; ML adds workload/hardware-sensitive model and profiler evidence; games add engine/frame/performance evidence.

For AI-assisted development, the safe integration rule is therefore: expose each domain's authoritative command-line or machine-readable gates to the agent; preserve target/runtime evidence; and never let an AI completion/review result substitute for the domain's actual build, test, static-analysis, device, or profiler evidence.

## Unresolved / intentionally not generalized

- No single formatter/linter/test/debugger choice is universal within JavaScript/TypeScript, JVM, C/C++ or .NET; this matrix records representative verified implementations, not mandates.
- Apple/iOS-specific tooling is not yet covered here.
- Game-engine coverage currently has one verified representative (Unity), not an engine-wide catalog.
- Data/ML coverage currently uses PyTorch as a representative implementation; data validation, experiment tracking and model registry systems remain open research.
- Embedded coverage uses Zephyr as a representative RTOS/toolchain; vendor-specific MCU/FPGA/automotive toolchains remain open research.
