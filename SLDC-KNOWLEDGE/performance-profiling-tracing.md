# Performance profiling, tracing, and AI-assisted diagnostics

Verification date: 2026-08-20

This document adds a language-agnostic performance-diagnostics baseline. It complements language/domain-specific profiler examples already present in `language-domain-matrix.md`; it does not replace them.

## 1. Baseline definition and SDLC role

Performance evidence answers questions that build, lint, tests, and functional debugging do not answer: where time/resources are consumed, which execution paths dominate, and why latency or resource regressions occur under a measured workload.

Keep these evidence planes distinct:

- **Metrics** summarize behavior over time and are appropriate for continuous monitoring and regression detection.
- **Profiles** statistically sample resource use (commonly CPU or memory) and aggregate stack/resource attribution.
- **Traces** preserve a time-ordered execution timeline and can correlate application, runtime, OS, scheduler, I/O, and hardware events.
- **Benchmarks/performance tests** measure externally visible outcomes for a controlled workload; they do not by themselves identify the internal cause.

Perfetto's official tracing guidance explicitly distinguishes profiling from tracing and notes that traces provide causal/timeline context while sampling profiles reduce data volume and identify resource-heavy stacks. It also recommends metrics for long-term observation when continuous tracing cost is inappropriate.

## 2. Representative implementation — Perfetto

Perfetto is an open-source tracing/profiling stack maintained by Google. Current documentation covers Android and Linux system tracing, application instrumentation, CPU call-stack sampling, performance counters, heap profiling, and analysis through Trace Processor/PerfettoSQL.

### Verified behavior

- Perfetto can combine multiple data sources in one trace and correlate app events with system data such as scheduling and CPU frequency.
- On Android/Linux it can sample CPU call stacks and performance counters through `perf_event_open`-based mechanisms.
- Trace Processor parses multiple trace/profile formats and exposes structured analysis through PerfettoSQL.
- The documented workflow explicitly supports moving from interactive investigation to programmatic/automated analysis.
- System-level tracing is supported out of the box on Android and Linux; Windows/macOS recording daemons do not provide the same built-in system-level data-source integration. Do not generalize Android/Linux system-trace capabilities to every OS.

### Selection/integration criteria

Choose a tracing/profiling stack based on:

- target OS/runtime and availability of system-level probes;
- CPU, heap, scheduler, GPU, I/O, power, or application-event evidence required;
- sampling frequency and recording overhead;
- symbolization/deobfuscation availability;
- machine-readable query/export support;
- ability to reproduce the measured workload and preserve trace configuration alongside results.

For CI/automation, prefer saved trace configs plus scripted collection and queryable outputs over screenshots alone.

Sources:

- Source type: official project documentation.
- Perfetto overview, verified 2026-08-20: https://perfetto.dev/docs/
- Profiling vs tracing guidance, verified 2026-08-20: https://perfetto.dev/docs/tracing-101
- CPU sampling/performance counters, verified 2026-08-20: https://perfetto.dev/docs/quickstart/callstack-sampling
- System tracing and OS-scope caveat, verified 2026-08-20: https://perfetto.dev/docs/getting-started/system-tracing
- Automated analysis / Trace Processor, verified 2026-08-20: https://perfetto.dev/docs/quickstart/trace-analysis

## 3. Runtime-native profiling — Go pprof

Go's official diagnostics documentation provides a concrete runtime-native profiling implementation.

### Verified behavior

Go exposes CPU, heap, thread-creation, goroutine, block, and mutex profiles through runtime/pprof and `net/http/pprof`, with `go tool pprof` for analysis. The documentation states that production profiling is possible but adds cost, and recommends measuring profiler overhead before enabling it broadly. It also warns that profiling mechanisms can interfere with each other; for example, precise memory profiling can skew CPU profiling.

Go additionally supports profile-guided optimization (PGO) using CPU pprof profiles. The official PGO workflow treats profile representativeness as a first-class requirement: an unrepresentative profile may provide little or no production benefit, and production profiles are preferred when feasible.

### Baseline implication

A profile is evidence for the sampled workload, runtime configuration, hardware, and time interval. It is not evidence that all workloads have the same hot paths. Store enough workload/version metadata to judge representativeness before using a profile for optimization or automated build decisions.

Sources:

- Source type: official language documentation.
- Go diagnostics/pprof, verified 2026-08-20: https://go.dev/doc/diagnostics
- Go profile-guided optimization, verified 2026-08-20: https://go.dev/doc/pgo

## 4. Low-overhead continuous/runtime recording — JDK Flight Recorder

Java SE 26 provides Flight Recorder (JFR) as a runtime-native event recording and profiling mechanism.

### Verified behavior

- JFR provides configurable event recording for JVM/application/OS behavior.
- Oracle documents `default.jfc` as intended for continuous recording with a typical overhead below 1%, while `profile.jfc` records more events for profiling.
- Oracle's performance-troubleshooting guide states that actual overhead varies by application and should be measured with the application's own performance tests.
- Some event sets materially alter the measured system: Heap Statistics can trigger old garbage collections and add significant pause overhead.
- JFR method evidence is sampling-based; low sample counts can make attribution inaccurate.

### Baseline implication

“Low overhead” is configuration- and workload-dependent, not a universal guarantee. Record the JDK version, JFR configuration, duration, workload and enabled high-cost events with the evidence.

Sources:

- Source type: Oracle official JDK 26 documentation.
- Flight Recorder configurations, verified 2026-08-20: https://docs.oracle.com/en/java/javase/26/jfapi/flight-recorder-configurations.html
- JFR performance troubleshooting/overhead caveats, verified 2026-08-20: https://docs.oracle.com/en/java/javase/26/troubleshoot/troubleshoot-performance-issues-using-jfr.html
- JFR API programmer guide, release 26, verified 2026-08-20: https://docs.oracle.com/en/java/javase/26/jfapi/index.html

## 5. OS-wide Windows evidence — WPR/WPA/ETW

Microsoft's Windows Performance Toolkit provides Windows Performance Recorder (WPR) and Windows Performance Analyzer (WPA). WPR records Event Tracing for Windows (ETW) system/application events; WPA analyzes resulting ETL recordings.

WPR supports command-line capture and built-in/custom recording profiles, making capture configuration scriptable. WPA provides timeline/table analysis over ETL evidence. This is materially different from a language-only profiler because ETW can correlate process/runtime behavior with broader Windows system activity.

Sources:

- Source type: Microsoft official documentation.
- Windows Performance Toolkit, verified 2026-08-20: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/
- Introduction to WPR, verified 2026-08-20: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/introduction-to-wpr
- Windows Performance Analyzer, verified 2026-08-20: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/windows-performance-analyzer

## 6. AI-assisted trace analysis — Microsoft ETW MCP Early Preview

Microsoft's current documentation (last updated 2026-08-14) describes **ETW MCP** as an Early Preview local/headless MCP server that exposes ETL trace processing/query tools to GitHub Copilot or other MCP-capable AI assistants.

### Verified automation possibilities

The official preview documents:

- natural-language querying of ETL traces;
- process/time-range filtering and CPU analysis;
- hot-stack inspection when symbols are available;
- baseline-vs-trial trace comparison;
- critical-path analysis;
- batch/ranking workflows across trace sets;
- repeated investigations in CI or scripts.

The server uses Microsoft's TraceProcessing data layer and exposes structured tool calls rather than streaming raw event data directly to the model.

### Hard authority boundary

Microsoft explicitly states that the resulting interpretation still comes from an LLM, can vary between runs, and may be incomplete or wrong. The documentation instructs users to validate important conclusions against the underlying trace tables, graphs, time ranges and call stacks before engineering/product/release decisions.

Therefore AI-assisted profiling is classified as **investigation and evidence-navigation automation**, not an autonomous performance-correctness oracle. Deterministic thresholds or release gates must consume verifiable measured data and preserve the raw trace/query evidence used for the decision.

The capability is also **Early Preview**: behavior, availability, supported scenarios and tooling may change before general availability.

Source:

- Source type: Microsoft official documentation; Early Preview.
- ETW MCP Early Preview, last updated 2026-08-14; verified 2026-08-20: https://learn.microsoft.com/en-us/windows-hardware/test/wpt/etw-mcp-early-preview-july-2026

## 7. Selection criteria for a general SDLC baseline

Before selecting or automating a profiler/tracer, document:

1. **Question/evidence type:** CPU, memory, lock contention, scheduler, I/O, GPU, power, network, startup, build performance, or end-to-end latency.
2. **Scope:** function/runtime, process, machine/OS, device, distributed request, or hardware interaction.
3. **Collection mode:** sampling, instrumentation, event tracing, counters, or mixed.
4. **Overhead budget:** measured effect of collection under the target workload.
5. **Representativeness:** exact workload, build, flags, environment and hardware represented by the recording.
6. **Symbols/context:** whether stacks can be symbolized and mappings preserved.
7. **Automation surface:** CLI/API/query format, deterministic exit/threshold behavior and artifact retention.
8. **Privacy/security:** traces may contain process names, paths, payload-adjacent metadata or other sensitive environment information; treat trace artifacts as potentially sensitive until inspected.

## 8. Integration and automation pattern

A bounded automated performance loop is:

`reproducible workload -> capture config -> raw profile/trace -> symbolization -> structured query/metric -> baseline comparison -> threshold/evidence gate -> human/agent diagnosis -> candidate change -> repeat measurement`

AI may assist with selecting queries, explaining deltas, identifying candidate hot paths and proposing changes. It must not replace the measured before/after comparison.

For regression gates:

- pin workload and environment as far as practical;
- retain raw artifacts and capture configuration;
- define tolerances before evaluating the result;
- account for warmup/noise/sampling uncertainty;
- repeat measurements when variance can change the decision;
- separate “performance improved in this measured scenario” from a universal performance claim.

## 9. Contradictions/non-equivalences retained

- Profiling and tracing are related but not interchangeable.
- Runtime-native profiles do not necessarily expose OS/hardware causal context.
- System traces can provide broad context but may cost much more data than metrics or samples.
- “Production-safe” profiling still has non-zero/configuration-dependent overhead that should be measured.
- A representative profile can guide optimization; an unrepresentative profile can mislead it.
- AI-assisted trace analysis can accelerate investigation but remains model-generated interpretation and must be checked against source evidence.

## 10. Unresolved / open discovery

- cross-platform continuous profiling systems and independently measured overhead/accuracy comparisons;
- Linux `perf`/eBPF and macOS Instruments as dedicated general-system baselines;
- GPU/vendor-native profilers beyond existing Android/Unity/PyTorch domain evidence;
- statistical methodology for noisy performance CI and hardware-normalized thresholds;
- direct evidence for autonomous AI performance changes that close the loop from profile to patch to repeated benchmark while preserving an explicit approval/authority boundary.
