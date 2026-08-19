# Store and device-fleet release-safety baseline

Verification date: 2026-08-20

This file adds representative, primary-source-backed release-safety evidence for mobile/app-store distribution and device-fleet/OTA update systems. It complements `release-deployment-progressive-delivery.md` and `release-safety-flags-database-nonk8s.md` without treating store rollout control, fleet abort, or rollback as equivalent mechanisms.

## 1. Baseline definition and SDLC role

Store and fleet delivery systems distribute versioned software beyond a conventional server deployment. A baseline should distinguish at least:

1. **release eligibility and targeting** — which users/devices can receive the version;
2. **rollout progression** — how exposure increases over time or across groups;
3. **observation** — crash, health, compliance, install, or failure evidence used during rollout;
4. **halt/abort** — whether further distribution can be stopped;
5. **recovery semantics** — what happens to recipients that already installed the version;
6. **fallback/rollback** — whether the platform can actively return devices to a selected known-good version;
7. **manual-install/out-of-band behavior** — whether users can bypass the controlled automatic rollout path.

These planes are not interchangeable. Stopping new recipients is not the same as reverting already-updated recipients, and a device-fleet rollback policy is not evidence that every application/data side effect is reversible.

## 2. Apple App Store phased releases

### Verified implementation

Apple App Store Connect documents phased release for version updates on iOS, macOS, and tvOS. The update is gradually made available to a random sample of users with automatic updates enabled over seven days: 1%, 2%, 5%, 10%, 20%, 50%, then 100%.

Apple also documents two material control boundaries:

- the phased release can be paused for a cumulative total of up to 30 days and later resumed from the day where it stopped;
- users can manually download the version from the App Store at any point during the phased release.

A phased release therefore controls the automatic-update path, not universal exposure. Apple also allows releasing to all users immediately.

### Selection and integration criteria

For App Store rollout evidence, preserve the app/version identity, phased-release state, rollout day/percentage, pause/resume actions, and post-release crash/quality evidence used for the decision. Automation must not infer that pausing the phased release removes the version from devices that already installed it.

### Automation possibilities

App Store Connect and its API can be used to create, inspect, pause, resume, or complete phased releases. Monitoring can trigger a human or deterministic policy decision to pause further automatic rollout. Because manual downloads remain possible, incident procedures should include a forward-fix/new-version path rather than relying on pause as a complete rollback mechanism.

### Sources

- Apple Developer, App Store Connect Help, `Release a version update in phases`: https://developer.apple.com/help/app-store-connect/update-your-app/release-a-version-update-in-phases
- Apple Developer, App Store Connect API `PhasedReleaseState`: https://developer.apple.com/documentation/appstoreconnectapi/phasedreleasestate

Source type: official vendor documentation. Verified: 2026-08-20. Scope: current App Store Connect phased-release documentation surfaced on the verification date.

## 3. Google Play staged rollouts and halt semantics

### Verified implementation

Google Play Console documents staged rollouts for app updates in production and test tracks. The operator selects a percentage of users; unlike Apple's fixed seven-day schedule, the percentage does not increase automatically. Staged rollout can also target selected countries.

Google documents that halting a staged rollout prevents additional users from receiving that release, while users that already received it remain on that version. The recommended remediation for a faulty bundle is to create and roll out a new fixed release.

Google additionally documents halting a release that has already reached 100% on eligible tracks. In that case the halted release is no longer served to new/eligible users and a previously live fully rolled-out version can become available instead. This still does not state that devices already running the halted version are forcibly downgraded.

### Selection and integration criteria

Preserve release-track identity, app bundle/version, rollout percentage, country scope, halt/resume actions, and crash/user-feedback evidence. Treat rollout halt as **distribution containment**, not as proof of installed-version rollback. Recovery plans should retain a verified previous release and a forward-fix path.

### Automation possibilities

Play release APIs/console controls can start, expand, halt, or resume rollout. Release automation can stop percentage expansion when crash/quality gates fail and publish a corrected release. Do not model a halt as an uninstall or downgrade operation unless a separate platform mechanism proves that behavior.

### Sources

- Google Play Console Help, `Release app updates with staged rollouts`: https://support.google.com/googleplay/android-developer/answer/6346149
- Google Play Console Help, `Halting a fully rolled-out release`: https://support.google.com/googleplay/android-developer/answer/16285429

Source type: official vendor documentation. Verified: 2026-08-20. Scope: Google Play staged/full rollout controls as documented on the verification date.

## 4. AWS IoT Jobs — staged fleet rollout and abort

### Verified implementation

AWS IoT Jobs defines remote operations targeted at one or more IoT devices. Job rollout configuration controls how many targets are notified per minute. AWS documents both constant and exponential rollout rates; exponential rollout can increase when configured notification/success criteria are met.

AWS also documents abort configuration for canceling a rollout when configured failure criteria are reached. This is intended to avoid sending a bad update to the entire fleet.

The control plane therefore provides **progressive notification plus abort**. The documentation does not by itself establish a universal device-side rollback mechanism for arbitrary firmware/application state.

### Selection and integration criteria

Record job document/version, target thing/group identities, base/rate configuration, rate-increase criteria, failure/abort thresholds, execution status, and device telemetry needed to determine real health. Device-side update design must separately prove atomicity, power-loss behavior, boot fallback, and persistence/data compatibility where relevant.

### Automation possibilities

Automation can create staged or exponential fleet rollouts, stop further targeting after threshold failures, retry according to explicit policy, and feed job-execution status into release gates. An abort should be followed by inventory/compliance checks because some devices may already have completed the operation before cancellation.

### Sources

- AWS IoT Core, `What is AWS IoT Jobs?`: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-what-is.html
- AWS IoT Core, `How job configurations work`: https://docs.aws.amazon.com/iot/latest/developerguide/jobs-configurations-details.html
- AWS IoT API, `ExponentialRolloutRate`: https://docs.aws.amazon.com/iot/latest/apireference/API_ExponentialRolloutRate.html

Source type: official vendor documentation/API reference. Verified: 2026-08-20.

## 5. Azure Device Update for IoT Hub — grouped OTA and automatic rollback

### Verified implementation

Microsoft documents Device Update for IoT Hub as an OTA update platform for device fleets. Deployments target device groups, can be scheduled, and report per-device deployment state.

Current documentation describes automatic rollback policy using both a minimum failed-device count and failed-device percentage threshold. When the trigger is reached, devices in the group can be rolled back to a selected update version. Microsoft also documents grouping as a mechanism for gradual update rollout and recommends test/flight groups before broad production rollout.

This is stronger rollback evidence than store pause/halt controls because the service explicitly models a rollback target version. It still depends on compatible device/update handlers and does not prove that arbitrary external state or data migrations are reversible.

### Selection and integration criteria

Preserve update identity and compatibility metadata, device-group identity, schedule, failure thresholds, rollback target, per-device status, and compliance evidence. Select a fleet updater only after verifying its device-side update handler, boot/recovery strategy, connectivity-loss behavior, storage requirements, and rollback compatibility for the actual hardware/software stack.

### Automation possibilities

Azure CLI/API can create deployments, schedule them, configure automatic rollback thresholds, query status, and retry failed devices. Group-based flighting can separate test/evaluation populations from production. Automated rollback should be followed by compliance and application/device-health verification rather than assuming rollback completion equals restored correctness.

### Sources

- Microsoft Learn, `What is Device Update for IoT Hub?`: https://learn.microsoft.com/en-us/azure/iot-hub-device-update/understand-device-update
- Microsoft Learn, `Update deployments`: https://learn.microsoft.com/en-us/azure/iot-hub-device-update/device-update-deployments
- Microsoft Learn, `Device groups`: https://learn.microsoft.com/en-us/azure/iot-hub-device-update/device-update-groups
- Microsoft Learn, `Deploy an update`: https://learn.microsoft.com/en-us/azure/iot-hub-device-update/deploy-update

Source type: official vendor documentation. Verified: 2026-08-20. Caveat: some Microsoft Learn deployment pages surfaced with authorization banners; claims here use content returned from those official pages and the public overview/group documentation.

## 6. Language-agnostic store/fleet selection baseline

For software distributed through stores or to fleets, preserve at least:

1. immutable source/build/artifact/update identity;
2. release channel/track/group and eligibility scope;
3. rollout progression rule and current exposure;
4. health/crash/compliance signals and thresholds;
5. exact semantics of pause, halt, cancel, and abort;
6. whether already-updated recipients remain on the version;
7. rollback/fallback target and whether rollback is platform-controlled or device/application-controlled;
8. post-recovery verification and population/version inventory;
9. manual-download or out-of-band update paths;
10. actor/automation identity and timestamps.

For firmware/embedded systems additionally verify power-loss safety, boot fallback, storage partitioning, signed-update policy, anti-rollback requirements where applicable, and data/schema compatibility. None of those properties is inferred from a cloud rollout controller alone.

## 7. Contradictions and limits preserved

- **Store pause/halt ≠ installed-device downgrade.** Apple phased-release pause and Google staged-rollout halt primarily limit further distribution; already-updated recipients can remain on the new version.
- **Apple phased release ≠ complete exposure control.** Manual App Store downloads remain possible during phased release.
- **Google staged rollout ≠ automatic schedule.** The documented percentage does not increase automatically.
- **Fleet abort ≠ device rollback.** AWS IoT Jobs can cancel further rollout on configured failures, but that alone does not prove prior targets revert.
- **Fleet rollback target ≠ arbitrary state restoration.** Azure Device Update can target a selected fallback update, but application data, external effects, boot behavior, and hardware-specific recovery still require separate evidence.
- No claim is made that Apple, Google, AWS, or Azure are universally best; they are representative implementations of distinct distribution/recovery semantics.

## 8. Remaining unresolved expansion

- desktop distribution outside app stores, including updater trust/signing and rollback semantics;
- additional independent OTA/fleet systems and automotive/MCU-specific recovery mechanisms;
- anti-rollback/security-counter interactions for signed firmware;
- app-store release automation that directly consumes crash/SLO signals for promotion decisions;
- SLO/error-budget-driven release gates across observability stacks;
- release-specific AI systems with documented authority, evidence inputs, and deterministic verification boundaries.