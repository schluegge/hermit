# Platform performance profiling and performance-CI expansion

Verification date: 2026-08-20

This document extends `performance-profiling-tracing.md` with platform-specific macOS/iOS and GPU evidence plus a reproducible performance-regression/CI baseline. It does not replace the language-agnostic taxonomy in that file.

## 1. Apple Instruments / `xctrace`

### SDLC role

Apple Instruments is the platform-native performance investigation layer for Apple application/device workloads. Current Xcode documentation places Instruments under performance and metrics and documents CPU, memory, responsiveness, graphics, energy and framework-specific analysis.

### Verified implementation and automation surface

- Xcode's command-line tool reference documents `xctrace` for recording, importing, exporting and symbolication of Instruments `.trace` files.
- Instruments provides templates such as Time Profiler and system/application-specific traces; current Metal guidance documents Game Performance and Game Memory templates that correlate CPU threads, scheduler/system calls, GPU activity, display timing, memory and Metal resource events.
- Current Core AI Instruments guidance can correlate model activity across CPU, GPU and Neural Engine and explicitly recommends real-device profiling for the most accurate device-performance evidence.

### Selection / integration criteria

Use Instruments when the target is an Apple platform and the question depends on Apple runtime, scheduler, power, Metal/GPU, Neural Engine, memory or device-specific evidence. Preserve Xcode version, OS/device model, build, symbols, template/configuration, target workload and raw `.trace` artifact.

For automation, prefer `xctrace`-produced trace artifacts and exported/symbolicated data over screenshots alone. Do not generalize an Instruments result from one Apple device class to all Apple hardware without repeated measurements.

### Caveats

- `xctrace` is an Apple/Xcode toolchain capability, not a cross-platform profiler.
- Simulator evidence is not interchangeable with physical-device performance evidence when hardware-specific behavior matters.
- A trace explains the measured run; it does not prove a universal bottleneck or improvement.

Sources:

- Source type: Apple official Xcode documentation.
- Xcode command-line tool reference (`xctrace`), verified 2026-08-20: https://developer.apple.com/documentation/xcode/xcode-command-line-tool-reference
- Xcode performance and metrics, verified 2026-08-20: https://developer.apple.com/documentation/xcode/performance-and-metrics
- Metal app performance / Game Performance Instruments template, verified 2026-08-20: https://developer.apple.com/documentation/xcode/analyzing-the-performance-of-your-metal-app/
- Metal developer workflows, verified 2026-08-20: https://developer.apple.com/documentation/Xcode/Metal-developer-workflows
- Core AI Instruments profiling, verified 2026-08-20: https://developer.apple.com/documentation/CoreAI/analyzing-model-runtime-performance-with-instruments

## 2. GPU-native profiling — NVIDIA Nsight Systems and Nsight Compute

### SDLC role

GPU performance work needs at least two distinct questions:

1. **system/timeline question** — how CPU threads, runtime/API calls, memory transfers and GPU work interact over time;
2. **kernel question** — why a specific GPU kernel underperforms at the hardware/metric level.

NVIDIA documents separate tools for these roles.

### Nsight Systems — timeline/system evidence

Current Nsight Systems documentation supports CUDA API tracing plus GPU workload tracing including kernel executions and memory operations, exposing CPU↔GPU timing relationships in one report. Post-collection analysis can be performed through GUI or CLI, and `nsys export` can export report data such as SQLite.

Important compatibility caveat: NVIDIA states that `.nsys-rep` is the forward-compatible report format; exported SQLite schema can change between versions. Automation should therefore retain the original `.nsys-rep` and treat exported schemas as version-scoped interfaces.

### Nsight Compute — kernel evidence

Current Nsight Compute 13.3 documentation describes an interactive and CLI CUDA kernel profiler with detailed metrics, data-collection modes, report comparison, customizable analysis rules and Python/report interfaces. It is appropriate when the bottleneck has been narrowed to CUDA kernel behavior and hardware counters/metrics are needed.

### Selection / integration criteria

Use Nsight Systems first for broad CPU/runtime/GPU timeline questions and Nsight Compute for kernel-level CUDA questions. Preserve GPU model, driver, CUDA/tool versions, clock/power state when relevant, workload, command-line options, NVTX annotations, report artifacts and metric-set configuration.

Do not infer vendor-neutral GPU behavior from NVIDIA-specific metrics. A kernel result on one GPU architecture is not automatically transferable to another GPU generation or vendor.

Sources:

- Source type: NVIDIA official documentation.
- Nsight Systems User Guide, current page verified 2026-08-20: https://docs.nvidia.com/nsight-systems/UserGuide/index.html
- Nsight Systems 2026.4.1 release notes, verified 2026-08-20: https://docs.nvidia.com/nsight-systems/ReleaseNotes/index.html
- Nsight Compute 13.3 documentation, verified 2026-08-20: https://docs.nvidia.com/nsight-compute/
- Nsight Compute Profiling Guide, verified 2026-08-20: https://docs.nvidia.com/nsight-compute/ProfilingGuide/index.html

## 3. Performance CI / noisy-regression baseline — Google Benchmark

### SDLC role

A performance-CI gate answers whether a controlled benchmark changed enough to justify investigation or blocking. It is distinct from a profiler: benchmarks quantify outcome deltas; profiles/traces help explain causes.

### Verified implementation

Google Benchmark's current official documentation provides:

- configurable minimum run time and warmup;
- repeated benchmark runs;
- mean, median, standard deviation and coefficient-of-variation reporting;
- JSON output with host/CPU/context metadata and per-benchmark results;
- random interleaving support and documented variance-reduction guidance;
- `compare.py` for baseline/contender comparison;
- a Mann–Whitney U test when sufficient repetitions are available.

The project's own comparison documentation warns that benchmark results are noisy, that visual inspection is insufficient, and that the U test needs a large repetition count (documented as no less than 9) to be meaningful. It also states that statistical significance does not by itself prove the underlying benchmarks are materially different.

### Deterministic gate requirements

A baseline performance gate should preserve at minimum:

- exact benchmark binary/source revision and compiler/build flags;
- benchmark input/workload;
- host/CPU/GPU/device identity and operating state relevant to the metric;
- warmup and minimum-run-time settings;
- repetition count and all raw per-run results;
- baseline/contender pairing method;
- predeclared practical-effect threshold in addition to any statistical significance threshold;
- raw JSON/report artifacts.

A safe gate should distinguish:

- **statistical signal**: evidence that distributions differ under the measured setup;
- **effect size / practical threshold**: whether the magnitude matters for the project;
- **causal diagnosis**: requires profiler/trace or other evidence and is not supplied by the benchmark comparison alone.

### Automation possibilities

CI can run benchmark suites, emit JSON, compare baseline and contender, compute/report repeated-run statistics, and fail a gate when a predeclared policy is violated. AI may summarize regressions and propose which profile/trace to collect next, but must not substitute generated interpretation for raw benchmark evidence.

Sources:

- Source type: Google Benchmark official project documentation/maintainer repository.
- User Guide, verified 2026-08-20: https://google.github.io/benchmark/user_guide.html
- Benchmark comparison tooling, verified 2026-08-20: https://google.github.io/benchmark/tools.html
- Maintainer repository, verified 2026-08-20: https://github.com/google/benchmark

## 4. Integration pattern

A cross-platform performance loop can now be represented as:

`controlled workload -> benchmark/performance test -> regression signal -> platform/system trace -> focused runtime/GPU profile -> candidate change -> repeat same benchmark -> compare distributions/effect -> retain artifacts`

Representative routing examples:

- Apple app/device issue -> Instruments/`xctrace`;
- Windows system issue -> WPR/WPA/ETW from `performance-profiling-tracing.md`;
- Linux CPU/system issue -> `perf`/Perfetto/eBPF continuous profile from `performance-profiling-tracing.md`;
- CUDA CPU↔GPU scheduling issue -> Nsight Systems;
- CUDA kernel-level issue -> Nsight Compute;
- CI regression detection -> repeated benchmark + machine-readable comparison, followed by profiling only when diagnosis is needed.

## 5. Contradiction / non-equivalence rules

- Instruments is not a generic cross-platform profiler.
- Apple Simulator performance is not equivalent to real-device hardware evidence.
- Nsight Systems timeline analysis and Nsight Compute kernel analysis overlap but are not interchangeable.
- NVIDIA profiler metrics are not vendor-neutral GPU semantics.
- Google Benchmark statistical significance is not practical significance and not causal proof.
- Repetitions reduce uncertainty but do not remove environmental bias; hardware/OS/power/background-load context remains part of the evidence.
- A green performance gate only establishes that the configured measured thresholds passed; it does not establish universal performance correctness.

## 6. Unresolved / open discovery

- independent cross-tool overhead/accuracy comparisons for continuous and platform profilers;
- AMD/Intel GPU-native profiler baselines and cross-vendor metric mapping;
- hardware-normalized and fleet-distributed performance thresholds;
- robust policies for thermal throttling, frequency scaling, noisy-neighbor and virtualization effects;
- direct verified autonomous `profile -> patch -> repeated benchmark` systems with explicit approval and release-authority boundaries.
