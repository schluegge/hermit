# Cross-vendor GPU profiling baseline — AMD and Intel

Verification date: 2026-08-20

This document extends `performance-platform-ci.md` with current AMD and Intel GPU-native profiling evidence. It complements the existing NVIDIA Nsight baseline; it does not define vendor-neutral counter equivalence.

## 1. Taxonomy and SDLC role

GPU performance diagnosis needs multiple evidence planes that must not be collapsed into one number:

1. **host/device timeline and API activity** — where CPU submission, runtime calls, transfers and GPU work occur over time;
2. **kernel/dispatch evidence** — which GPU kernels or dispatches dominate measured work;
3. **hardware-counter evidence** — architecture-specific events and derived metrics used to diagnose utilization, stalls, memory behavior or execution efficiency;
4. **workload-level outcome** — latency, throughput, frame time or another externally meaningful benchmark metric.

Vendor profilers supply different subsets of these planes. Selection must follow the target GPU/runtime and the diagnostic question rather than assuming one profiler or metric vocabulary is portable across vendors.

## 2. AMD ROCm — ROCprofiler-SDK / `rocprofv3`

### Verified current implementation

AMD's current ROCprofiler-SDK documentation describes it as profiling infrastructure for general-purpose GPU compute applications on ROCm. It supports application tracing for the broad execution picture and kernel counter collection for low-level hardware details. Runtime-independent APIs cover runtime-call tracing plus asynchronous GPU activities such as kernel dispatches and memory moves.

The current `rocprofv3` CLI can trace applications and collect kernel counters without source modification. Current quick-reference documentation includes capability discovery (`rocprofv3 --list-avail` / `rocprofv3-avail`) and basic tracing of HIP APIs, kernel dispatches and memory operations.

### Deprecation boundary

AMD's legacy ROCProfiler documentation now explicitly marks ROCProfiler, ROCTracer, `rocprof` and `rocprofv2` deprecated and strongly recommends ROCprofiler-SDK plus `rocprofv3`. AMD anticipates end of support for the legacy line by the end of 2026 Q2. Therefore new baseline automation should not select legacy `rocprof` merely because older examples remain discoverable.

### Selection / integration criteria

Use ROCprofiler-SDK/`rocprofv3` when the target is a supported ROCm compute workload and the question requires HIP/runtime tracing, dispatch timing, memory-operation activity or supported performance counters. Preserve at minimum:

- ROCm and ROCprofiler-SDK versions;
- exact GPU model/architecture and driver/runtime context;
- workload binary/source revision and input;
- profiler command and selected tracing/counter configuration;
- `rocprofv3 --list-avail` or equivalent capability evidence for the target;
- raw trace/counter output and any derived report.

Do not assume a counter exists on every AMD GPU. Capability discovery is part of the evidence because available hardware counters are device-specific.

## 3. AMD ROCm Compute Profiler

### Verified current implementation

ROCm Compute Profiler is AMD's kernel-level profiler for ML/HPC workloads on AMD Instinct GPUs. Current documentation states that it is built on ROCprofiler-SDK and acquires hardware performance counters, providing analyses such as System Speed-of-Light, hardware-block-level Speed-of-Light, memory analysis, roofline analysis and baseline comparisons.

Current scope primarily targets Instinct MI300, MI200 and MI100 series. AMD documents Radeon/RDNA support as development in progress, so this baseline does not claim current feature parity across Instinct and Radeon hardware.

### Automation surface

`rocprof-compute profile` collects workload profiling data and can automate configured counter collection. Current documentation supports machine-processable raw output formats including CSV and ROCPD; filtering can reduce profiling scope/time. Baseline comparisons are supported for evaluating optimization changes.

### Selection / integration criteria

Use ROCm Compute Profiler after a workload has been narrowed to kernel/hardware behavior on a supported AMD Instinct target. Preserve accelerator model, profiler version, selected metric blocks/counters, replay/filter configuration, workload inputs, raw counter artifacts, analysis output and comparison baseline.

Because counter collection and derived models are architecture-specific, do not normalize an AMD Speed-of-Light or roofline-derived metric directly to a similarly named NVIDIA or Intel metric without a separately verified semantic mapping.

## 4. Intel — VTune Profiler GPU analysis

### Verified current implementation

Intel VTune Profiler's current 2026 documentation provides GPU Offload analysis to correlate CPU and GPU execution and determine whether a workload is CPU- or GPU-bound. It supports GPU usage/timeline evidence and tracing of programming APIs including SYCL, Level Zero and OpenCL on supported Intel graphics targets. The analysis can also collect hardware-event-derived information such as data-transfer/bandwidth evidence when the required driver/support is present.

For GPU-bound workloads, Intel documents GPU Compute/Media Hotspots for more detailed kernel-level investigation, including execution per code line and performance issues associated with memory latency or inefficient kernel algorithms. Some accelerator-analysis capabilities are preview features in current documentation and must be recorded as such rather than treated as stable contractual interfaces.

### Selection / integration criteria

Use VTune GPU analysis when the target is supported Intel GPU compute/offload and the question requires host↔device correlation, queue/utilization evidence or focused kernel analysis. Preserve:

- VTune version and whether a used analysis type is production or preview;
- CPU/GPU model, driver and OS;
- runtime/API (for example SYCL, Level Zero or OpenCL) and compiler/debug-info flags where required;
- exact analysis type, knobs, target GPU and collection command;
- raw VTune result plus exported reports;
- workload revision/input and benchmark outcome.

Tracing programming APIs can perturb CPU-side performance; such collection overhead is a caveat in comparisons.

## 5. Intel GPA status — historical/specialized, not the current default baseline

Intel Graphics Performance Analyzers historically supplied System Analyzer, Graphics Trace Analyzer, Graphics Frame Analyzer and a scriptable framework for graphics/game profiling. However, Intel's current product page states that **Intel GPA 2025.1 is the final version**, with no further feature improvements or security fixes and discontinuation in 2026. Intel directs GPU compute profiling users toward VTune.

Consequences for the baseline:

- do not present Intel GPA as an actively evolving default toolchain in 2026;
- existing GPA 2025.1 evidence remains relevant for supported legacy graphics workflows, but version/support status must be preserved;
- new Intel compute-profiling decisions should evaluate current VTune capabilities first;
- an EOL profiler may still produce useful evidence, but maintenance/security/support status becomes part of selection criteria.

## 6. Cross-vendor metric mapping rules

The repository now has verified native profiler families for NVIDIA, AMD and Intel. This is **coverage of representative implementations**, not evidence that their counters or derived metrics are numerically interchangeable.

Required rules:

- Map first by **question/phenomenon**, not by metric name: e.g. host/device overlap, transfer activity, kernel duration, occupancy/utilization, cache/memory pressure, instruction/execution stalls.
- Preserve the vendor's exact counter/metric identifier, GPU architecture, profiler version and derivation/model where available.
- Do not compare a derived utilization/Speed-of-Light/occupancy percentage across vendors unless definitions, denominators, sampling/replay behavior and target architecture semantics have been independently reconciled.
- Prefer workload-level benchmark outcomes for cross-vendor product comparisons; use vendor-native counters to explain each target's bottlenecks locally.
- If semantic equivalence cannot be proven, record the mapping as `unresolved` rather than inventing a common metric.

## 7. Automation possibilities

Deterministic automation can:

- discover target-supported profiler capabilities/counters;
- collect traces and kernel/counter profiles with pinned configurations;
- export machine-readable artifacts where supported;
- identify candidate hot kernels/dispatches from measured evidence;
- compare repeated workload outcomes before and after a change;
- retain vendor-native evidence alongside benchmark results.

AI may summarize traces/counters, suggest likely bottlenecks, choose the next profiler evidence plane, or propose a candidate optimization. AI-generated interpretation is not raw profiler evidence and should stay behind repeatable benchmark/profile gates before any release or performance claim.

## 8. Contradiction / deduplication pass

- NVIDIA Nsight remains documented in `performance-platform-ci.md`; this file adds AMD/Intel instead of duplicating its detailed NVIDIA section.
- Legacy AMD `rocprof` examples were not treated as current default guidance because AMD now deprecates that tool line.
- ROCprofiler-SDK/`rocprofv3` broad tracing/counter collection was not conflated with ROCm Compute Profiler's higher-level kernel/performance-model analysis.
- AMD Instinct support was not generalized to Radeon/RDNA where current AMD documentation says support is still in progress.
- Intel GPA capability was not removed from history, but its 2025.1 final-version/EOL status was preserved and it was not presented as a maintained 2026 default.
- Intel preview analysis features were not promoted to stable guarantees.
- Similar metric names across NVIDIA/AMD/Intel were not treated as equivalent without semantic evidence.

## 9. Unresolved / open discovery

- exact counter-by-counter semantic mappings across NVIDIA, AMD and Intel architectures;
- independent cross-tool profiler overhead/accuracy comparisons;
- current Radeon/RDNA coverage as ROCm Compute Profiler support evolves;
- Intel graphics/game profiling replacement paths beyond EOL GPA, including third-party tools, with independent capability verification;
- hardware-normalized/distributed performance thresholds and environmental-noise policy;
- direct verified autonomous `profile -> patch -> repeated benchmark` systems with explicit authority boundaries.

## Sources

All sources are primary vendor documentation, verified 2026-08-20.

### AMD

- ROCprofiler-SDK 1.3.2 documentation: https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/
- `rocprofv3` usage: https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/how-to/using-rocprofv3.html
- ROCprofiler-SDK quick reference: https://rocm.docs.amd.com/projects/rocprofiler-sdk/en/latest/quick-reference/quick_guide.html
- Legacy ROCProfiler deprecation notice: https://rocm.docs.amd.com/projects/rocprofiler/en/latest/
- ROCm Compute Profiler current documentation: https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/
- ROCm Compute Profiler overview: https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/what-is-rocprof-compute.html
- ROCm Compute Profiler profile mode: https://rocm.docs.amd.com/projects/rocprofiler-compute/en/latest/how-to/profile/mode.html

### Intel

- VTune Profiler 2026 GPU Offload Analysis: https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2026-0/gpu-offload-analysis.html
- VTune Profiler accelerator analyses: https://www.intel.com/content/www/us/en/docs/vtune-profiler/user-guide/2026-0/accelerators-group.html
- Intel Graphics Performance Analyzers product/EOL notice: https://www.intel.com/content/www/us/en/developer/tools/graphics-performance-analyzers/overview.html
- Intel GPA 2025.1 documentation: https://www.intel.com/content/www/us/en/docs/gpa/user-guide/2025-1/overview.html
