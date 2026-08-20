# Firmware anti-rollback and automotive update-security baseline

Verification date: 2026-08-20

This baseline covers firmware-level downgrade prevention, boot acceptance/recovery, and automotive multi-ECU update security. It complements `store-and-fleet-release-safety.md`, which covers rollout controllers and fleet distribution, by documenting device-local and vehicle-level protections that a cloud rollout service does not prove.

## 1. Baseline definition and SDLC role

Firmware update security should separate at least these evidence planes:

1. **artifact authenticity/integrity** — whether the image is accepted as trusted;
2. **compatibility/target identity** — whether the image is intended for the hardware/ECU;
3. **anti-rollback / downgrade policy** — whether an older but otherwise valid image may execute;
4. **candidate boot / functional acceptance** — whether a newly installed image survives a deterministic self-test or health gate;
5. **fallback/revert** — whether a failed candidate can return to a previous image;
6. **fleet/vehicle consistency** — whether multiple ECUs receive a mutually compatible authorized bundle;
7. **security-counter lifecycle** — how monotonic counters are advanced, stored, exhausted, or intentionally bypassed;
8. **post-update health/state** — whether application, peripheral, persistent-data, and business/device behavior are correct after activation.

These planes are not interchangeable. A signed image can still be an older vulnerable image. Anti-rollback can intentionally prevent recovery to a previously working image. A successful boot does not prove fleet-wide or application-level correctness.

## 2. MCUboot 2.4.0 — security counter plus candidate-image recovery

### Verified implementation

MCUboot is a secure bootloader for 32-bit microcontrollers. The maintainer repository lists **MCUboot v2.4.0** as the current stable release on the verification date.

MCUboot documents two distinct mechanisms that must not be collapsed:

- **test swap / revert**: a candidate image can be booted as a test image and automatically reverted on the next reset unless application firmware marks the image permanent. The documented purpose is to avoid permanently bricking a device when new firmware immediately fails; application firmware can run a self-test before confirming the image.
- **downgrade prevention / rollback protection**: image version or a dedicated security counter can prevent an older image from replacing the active image. Hardware-based rollback protection compares the signed image's security counter against a counter stored in a trusted, non-volatile platform component.

The security counter is deliberately independent from ordinary image version. MCUboot states that it need not increase for every software release and that an older software version can remain acceptable when its security counter is equal to the active security level.

### Selection criteria

Use this model when the product requires both a device-local bootloader and an explicit distinction between **functional fallback** and **security downgrade prevention**. Before selecting the mechanism, verify the actual update mode, flash layout, trusted-counter storage, confirmation/self-test behavior, multi-image behavior, and power-loss characteristics for the target port.

Do not assume every MCUboot mode provides identical downgrade-prevention semantics. The documented software-based option has mode-specific constraints, while hardware rollback protection requires a target implementation of the security-counter interface.

### Integration and automation

A deterministic update pipeline can:

1. sign an image with explicit version and security-counter metadata;
2. verify target hardware/slot compatibility;
3. reject candidates below the device security counter;
4. install the image as a test candidate where the selected MCUboot mode supports that lifecycle;
5. run device self-tests after boot;
6. confirm the image only after deterministic acceptance checks pass;
7. preserve bootloader/update logs and exact image/counter identity;
8. revert an unconfirmed failed test candidate according to the documented boot mode.

AI may assist with log analysis, candidate-test selection, or generation of reviewable update plans. No inspected primary source grants AI authority to lower a security counter, bypass signature/counter checks, confirm a failed candidate, or declare device recovery complete.

### Sources

- MCUboot maintainers, releases: https://github.com/mcu-tools/mcuboot/releases
- MCUboot maintainers, design / downgrade prevention: https://docs.mcuboot.com/design.html
- MCUboot maintainer repository: https://github.com/mcu-tools/mcuboot

Source type: maintainer repository/documentation. Verified: 2026-08-20. Version scope: MCUboot 2.4.0/current documentation surfaced on the verification date.

## 3. ESP-IDF — irreversible eFuse security-version boundary

### Verified implementation

Current ESP-IDF documentation for ESP32 describes application anti-rollback by comparing the application's `security_version` with a security version stored in device eFuse. A bootable application must have a security version greater than or equal to the value programmed in eFuse.

The mechanism is materially different from an ordinary release number:

- anti-rollback is enabled through explicit bootloader configuration;
- OTA rollback and anti-rollback can be used together, but fallback is limited to images whose security version still satisfies the eFuse floor;
- the ESP32 eFuse security-version field has a finite bit budget; the current OTA documentation states a 32-bit limit for the described ESP32 path;
- programmed eFuse bits are irreversible, so advancing the security floor is a security-sensitive lifecycle event rather than a normal version-label update;
- factory/test partitions are not supported by the documented ESP32 anti-rollback scheme.

Espressif's current security overview explicitly explains why signature trust alone is insufficient: a legitimately signed older image may contain a revoked security feature or credential and therefore still need to be rejected.

### Selection and integration criteria

Treat an eFuse security-counter increment as an irreversible production-security action. Define when a release is sufficiently validated before increasing the floor, retain an inventory of device security-version state, and prove that any required emergency fallback image remains at or above the accepted security level.

A release pipeline should fail closed when the candidate version cannot satisfy the device security floor. It should not automatically consume scarce irreversible counter capacity merely because an ordinary application version changed.

### Sources

- Espressif, ESP-IDF latest ESP32 OTA / anti-rollback: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/ota.html
- Espressif, ESP-IDF latest ESP32 security overview: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/security/security.html
- Espressif, eFuse manager secure-version API: https://docs.espressif.com/projects/esp-idf/en/latest/esp32/api-reference/system/efuse.html

Source type: official vendor documentation. Verified: 2026-08-20. Scope: current ESP32 documentation; other Espressif SoCs can have different eFuse/security-version details and must be verified separately.

## 4. Uptane 2.1.0 — automotive multi-ECU update security

### Verified implementation

Uptane is a secure software-update standard designed for automobiles. The official version index identifies **Uptane Standard 2.1.0** as the latest released Standard on the verification date.

The Uptane threat model explicitly includes:

- freeze attacks that continue serving old but valid update metadata;
- rollback attacks that cause an ECU to install a previously valid older software revision;
- partial-bundle installation attacks;
- mix-and-match situations where individually valid images form an incompatible bundle;
- arbitrary-software attacks.

Uptane uses signed metadata and distinct Image/Director repository roles to constrain update authorization. Its deployment best practices document rollback prevention through two independent version planes: metadata versions and per-image **release counters**. By default, older metadata and lower release counters are rejected.

Uptane also preserves an important operational contradiction: an OEM may sometimes need to intentionally install older functional software because a newer release is unreliable. The best-practices document treats this as an exceptional security-sensitive operation, not as an ordinary rollback command. It explains that counter policy determines whether such a downgrade remains possible and warns that never increasing release counters weakens protection if the Director repository is compromised.

### Vehicle-level consistency boundary

Fleet delivery to a vehicle is not only a per-ECU problem. Uptane explicitly models multi-ECU bundle threats. Its best practices discuss retries and, where ECUs have sufficient storage/recovery ability, a possible two-phase-commit-style installation coordinated by a gateway ECU. The same source also makes clear that this technique does not create all other security guarantees and depends on the gateway behaving correctly.

Therefore:

- per-image signature validity does not prove vehicle-wide compatibility;
- per-ECU anti-rollback does not prove atomic multi-ECU installation;
- a gateway-coordinated bundle protocol does not eliminate all compromise or failure modes;
- Uptane does not itself prove that packaged software is free from malware or supply-chain compromise; those concerns are explicitly outside the Standard's core scope and belong to the supply-chain evidence planes already documented elsewhere in this repository.

### Selection and integration criteria

For automotive/vehicle deployments preserve at least:

1. ECU and hardware identity;
2. Image- and Director-repository metadata identities and signatures;
3. metadata versions and expiration/freshness state;
4. image release counters;
5. vehicle/bundle assignment;
6. per-ECU installation result;
7. bundle-consistency/partial-install state;
8. intentionally authorized exceptional rollback decisions;
9. post-install ECU and vehicle health evidence;
10. exact operator/automation identity for security-sensitive counter/policy changes.

### Sources

- Uptane, official versions index: https://uptane.org/docs/latest/all-versions
- Uptane Standard 2.1.0 / current threat model: https://uptane.org/docs/latest/standard/uptane-standard
- Uptane Deployment Best Practices 2.1.0: https://uptane.org/docs/2.1.0/deployment/best-practices

Source type: official standard and deployment guidance. Verified: 2026-08-20. Version scope: Standard 2.1.0; deployment guidance 2.1.0/current surfaced content.

## 5. Language-agnostic firmware/automotive selection baseline

Before declaring an embedded/vehicle update path safe, verify independently:

1. artifact signing/authentication and key lifecycle;
2. hardware/ECU compatibility identity;
3. normal application/version semantics;
4. security-counter / anti-rollback semantics;
5. whether counter storage is trusted and monotonic/irreversible;
6. candidate-image boot and health-confirmation semantics;
7. fallback availability after the security floor advances;
8. power-loss/interruption behavior;
9. storage/slot requirements;
10. multi-image or multi-ECU consistency rules;
11. mutable data/schema/peripheral compatibility;
12. fleet inventory and post-update compliance/health verification.

Security policy should explicitly state which failures justify a forward fix, which permit functional fallback at the same security level, and which older versions are permanently forbidden.

## 6. AI-driven automation opportunities and authority boundary

Evidence-backed mechanisms allow bounded AI assistance for:

- summarizing boot/update/fleet failure evidence;
- proposing self-test or rollout-test coverage;
- correlating image/counter/ECU state across a fleet;
- drafting human-reviewable recovery or staged-rollout plans;
- detecting inconsistent metadata/counter inventories for deterministic follow-up checks;
- proposing which artifact should be evaluated as a candidate fallback when policy permits it.

No inspected source supports granting an AI system independent authority to burn irreversible security eFuses/counters, reduce anti-rollback protection, bypass signature or metadata checks, intentionally authorize an automotive downgrade, confirm an unhealthy firmware image, or declare a multi-ECU vehicle recovered. Those actions require explicit deterministic policy and verified device/vehicle evidence.

## 7. Contradictions and limits preserved

- **Signed/authentic image ≠ acceptable security version.** ESP-IDF explicitly documents rejection of trusted older applications through security-version policy.
- **Functional rollback ≠ security rollback.** MCUboot test-swap recovery and anti-rollback counters solve different problems.
- **Higher ordinary version ≠ higher security level.** MCUboot separates image version and security counter.
- **Anti-rollback ≠ guaranteed recoverability.** Raising a security floor can intentionally make older known-working images unusable.
- **Cloud/fleet abort ≠ device boot fallback.** The fleet controllers documented elsewhere cannot substitute for bootloader evidence.
- **Per-ECU validity ≠ bundle correctness.** Automotive systems must account for partial installation and incompatible multi-ECU combinations.
- **Rollback prevention ≠ supply-chain security.** Uptane explicitly leaves packaged-software/build-system compromise outside its core scope.
- **Boot/self-test success ≠ full business or safety correctness.** Acceptance is only as strong as the checks actually executed.

## 8. Unresolved / open expansion

- additional MCU/SoC implementations with independently documented anti-rollback counters and secure-boot interaction;
- power-loss/fault-injection matrices for counter advancement and candidate confirmation across specific MCUboot ports;
- exact anti-rollback semantics for additional Espressif SoCs rather than extrapolating ESP32 behavior;
- automotive implementations beyond the Uptane standard, including production conformance evidence and hardware-root-of-trust integration;
- quantitative fleet policies for when a security counter may be irreversibly advanced;
- peripheral/co-processor firmware coordination and atomicity;
- AI systems with explicitly documented production authority over irreversible firmware-security state.
