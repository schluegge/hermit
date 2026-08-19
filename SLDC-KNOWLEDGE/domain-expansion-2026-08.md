# Domain expansion — Apple, Unreal, MLflow, ESP-IDF

Verification date: 2026-08-19

Purpose: resolve four previously open language/domain expansion fronts with current primary-source evidence. These are representative baselines, not exhaustive vendor/ecosystem catalogs.

## 1. Apple / iOS / Xcode

**Distinct lifecycle needs.** Apple-platform development adds simulator and physical-device execution, platform signing/distribution constraints, UI/performance testing, platform-specific debugging/profiling, and CI/distribution integration.

**Verified toolchain components.** Apple documents Xcode as the integrated environment for devices and Simulator, debugging, performance/metrics, testing, distribution, and Xcode Cloud. Xcode debugging includes the Xcode debugger, Organizer, Metal debugger and Instruments. Swift Testing integrates with Xcode projects and Swift Package Manager, supports parameterization and concurrency, and can run from the command line through Swift Package Manager. XCTest remains relevant, including repeatable performance tests. Xcode Cloud can automatically build, test and distribute applications.

**Selection/integration criteria.** Treat simulator and physical-device runs as different evidence surfaces; choose Swift Testing/XCTest according to project/platform compatibility; preserve Instruments/performance-test evidence for performance claims; keep signing/distribution credentials isolated from ordinary build/test automation; pin the Xcode/toolchain version used in CI when reproducibility matters.

**Automation possibilities.** Build/test through Xcode/Xcode Cloud or command-line Swift Package Manager where applicable; execute test matrices across devices/languages; collect test artifacts and performance measurements; automate distribution only through appropriately permissioned CI. Successful simulator tests do not prove physical-device behavior, and passing tests do not prove performance without measured evidence.

Evidence:
- Xcode overview — https://developer.apple.com/documentation/xcode (Apple official docs; verified 2026-08-19).
- Xcode debugging — https://developer.apple.com/documentation/xcode/debugging (Apple official docs; verified 2026-08-19).
- Swift Testing — https://developer.apple.com/documentation/testing (Apple official docs; verified 2026-08-19).
- Testing/performance overview — https://developer.apple.com/documentation/technologyoverviews/testing-and-performance (Apple official docs; verified 2026-08-19).
- Performance tests — https://developer.apple.com/documentation/xcode/writing-and-running-performance-tests (Apple official docs; verified 2026-08-19).

## 2. Games — Unreal Engine

**Distinct lifecycle needs.** Unreal adds engine/editor state, content/assets, packaged builds, gameplay/system tests, rendering comparisons, multi-instance/network testing, and build/cook/package automation.

**Verified toolchain components.** Unreal Engine 5.8 documents an Automation Test Framework for unit, feature, smoke, content-stress and screenshot-comparison tests. Tests can run from the editor, Session Frontend, Unreal Frontend or command line; command-line runs can export JSON plus HTML results. Epic's Automation Tool scripts unattended processes including building, cooking, running games and automation tests. Current documentation also exposes an experimental `UAutomationTestToolset` that allows MCP clients to discover, run and retrieve test results; because the API is experimental, it is recorded as a capability with stability caveat rather than a baseline dependency.

**Selection/integration criteria.** Separate low-level tests from gameplay/content tests; make tests state-independent and cleanup-safe as Epic recommends; preserve screenshot baselines and exported reports when visual correctness matters; use packaged/client/device runs for target-specific behavior rather than assuming Editor success generalizes.

**Automation possibilities.** Execute named/grouped tests from command line, export machine-readable reports, distribute tests across instances/devices, automate build/cook/package/test sequences through Automation Tool, and optionally expose automation through the experimental MCP-facing toolset. Engine/editor success alone is not evidence that packaged builds or target devices behave identically.

Evidence:
- Automation Test Framework, Unreal Engine 5.8 — https://dev.epicgames.com/documentation/en-us/unreal-engine/automation-test-framework-in-unreal-engine (Epic official docs; verified 2026-08-19).
- Running automation tests — https://dev.epicgames.com/documentation/en-us/unreal-engine/run-automation-tests-in-unreal-engine (Epic official docs; verified 2026-08-19).
- Automation Tool overview — https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-automation-tool-overview-for-unreal-engine (Epic official docs; verified 2026-08-19).
- `UAutomationTestToolset` — https://dev.epicgames.com/documentation/unreal-engine/API/Plugins/AutomationTestToolset/UAutomationTestToolset (Epic official API docs; Unreal Engine 5.8; experimental; verified 2026-08-19).

## 3. Data / ML lifecycle — MLflow

**Distinct lifecycle needs.** ML systems require experiment/run provenance, metrics/artifact tracking, model evaluation, model lineage/versioning and controlled promotion/deployment in addition to ordinary software tests.

**Verified toolchain components.** MLflow 3.14.0 documentation describes MLflow Tracking for runs, parameters, code versions, metrics and artifacts; Model Registry for centralized model lifecycle management with versions, aliases, tags and lineage; and evaluation APIs for automated metrics/visualizations and threshold validation. The documentation explicitly separates classic ML evaluation (`mlflow.models.evaluate`) from GenAI/LLM evaluation (`mlflow.genai.evaluate`): their metric/scorer systems are not interoperable.

**Selection/integration criteria.** Record dataset/workload, code/model version and environment with each run where reproducibility matters; keep evaluation thresholds explicit and reviewable; choose classic ML versus GenAI evaluation deliberately because the evaluation object models differ; use a remote/database-backed tracking/registry configuration where collaboration and production lifecycle management require it.

**Automation possibilities.** Log experiments and artifacts automatically, validate model metrics against thresholds, register/version models, attach lineage/metadata, and gate promotion/deployment on explicit evaluation results. Registry state or a successful training run is not itself proof of model quality; quality claims require evaluation tied to the measured data/workload.

Evidence:
- MLflow documentation, version 3.14.0 observed — https://mlflow.org/docs/latest/ (MLflow official docs; verified 2026-08-19).
- MLflow Tracking — https://mlflow.org/docs/latest/ml/tracking/ (MLflow official docs; verified 2026-08-19).
- Model Registry — https://mlflow.org/docs/latest/ml/model-registry/ (MLflow official docs; verified 2026-08-19).
- Model Evaluation — https://mlflow.org/docs/latest/ml/evaluation/ (MLflow official docs; verified 2026-08-19).

## 4. Vendor-specific embedded — Espressif ESP-IDF

**Distinct lifecycle needs.** A vendor MCU stack adds SoC/board-specific configuration, cross-build orchestration, flashing, serial monitoring, on-target debugging and hardware-backed tests.

**Verified toolchain components.** ESP-IDF documents `idf.py` as the project front end orchestrating CMake, Ninja/build tooling and `esptool`; commands include project creation, configuration, build, clean/fullclean and flash. IDF Monitor captures target serial output, can trigger rebuild/flash, save logs and enter GDB-based runtime debugging when configured. ESP-IDF unit-test guidance supports build/flash/on-target test execution and recommends the pytest-based `pytest-embedded` framework for CI or repeated test runs.

**Selection/integration criteria.** Pin ESP-IDF/toolchain and target configuration; distinguish host-build success from flashed/on-device test evidence; retain serial logs/test artifacts for hardware failures; treat `fullclean` as destructive to build outputs and use it only when required; define the exact supported target/board matrix instead of generalizing from one ESP32 device.

**Automation possibilities.** Configure/build/flash/monitor through `idf.py`, automate repeated on-target tests with pytest-embedded, collect serial evidence, and combine build/flash/monitor workflows. Passing on one board/SoC configuration does not prove other targets supported by ESP-IDF.

Evidence:
- `idf.py` front end — https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/tools/idf-py.html (Espressif official docs; verified 2026-08-19).
- IDF Monitor — https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-guides/tools/idf-monitor.html (Espressif official docs; verified 2026-08-19).
- ESP-IDF unit testing v6.0.2 — https://docs.espressif.com/projects/esp-idf/en/stable/esp32/api-guides/unit-tests.html (Espressif official docs; verified 2026-08-19).

## Cross-domain implications

These expansions reinforce the existing language-agnostic baseline rather than changing it. Domain-specific systems add evidence surfaces: Apple adds Simulator/device/signing/performance/distribution; Unreal adds editor/content/packaged-build/visual-test evidence; MLflow adds run/dataset/model/evaluation lineage; ESP-IDF adds board/flash/serial/on-target evidence.

For AI-assisted automation, agents should invoke the authoritative deterministic or machine-readable gates for the target domain and preserve their artifacts. AI-generated code, review, or diagnoses are never substitutes for device/runtime/evaluation evidence.

## Remaining unresolved expansion fronts

- Additional Apple build/signing command-line details beyond the high-level Xcode/Xcode Cloud/Swift Package Manager baseline are not enumerated here.
- Game-engine coverage now has Unity and Unreal representatives, but is not engine-exhaustive; Godot and proprietary engines remain open.
- ML lifecycle coverage now includes PyTorch profiling plus MLflow tracking/registry/evaluation, but data-validation systems, feature stores and additional orchestration systems remain open.
- Embedded coverage now includes Zephyr plus ESP-IDF, but MCU/FPGA/automotive/vendor ecosystems remain open.
