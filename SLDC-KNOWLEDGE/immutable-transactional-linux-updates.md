# Immutable / transactional Linux OS updates

Verification date: 2026-08-20

Status: **verified representative**

## Baseline definition

An immutable/transactional Linux update system treats the operating-system payload as a versioned deployment or generation that can be prepared separately from the currently running system and activated through an explicit switch or boot boundary. The baseline is not defined by a marketing use of the word "immutable"; it requires evidence for how versions are created, activated, retained, inspected, and recovered.

The minimum evidence planes are:

1. **System definition / update source** — what identifies the desired OS state.
2. **Prepared state** — whether the next state is constructed without partially mutating the currently booted OS.
3. **Activation boundary** — reboot, switch, or another explicit transition.
4. **Retained history** — which previous deployments/generations remain selectable.
5. **Rollback / generation switch** — what the recovery operation actually changes.
6. **Persistent-state boundary** — which paths or external state are deliberately outside the OS deployment.
7. **Garbage collection / retention** — when old recoverable states cease to exist.
8. **Verification / health** — what evidence exists that the newly activated system actually works.

A transactional OS update is **not** equivalent to application-data rollback, database rollback, service-health verification, or backup.

## Role in the SDLC

Immutable/transactional OS update systems are relevant to release engineering, fleet maintenance, infrastructure operations, desktop/server lifecycle management, incident recovery, and reproducible environment management. They can reduce partial-update states and can make rollback of the OS payload deterministic, but only inside their documented state boundary.

They integrate naturally with CI-built OS images/configurations, staged rollout systems, provenance/signing controls, post-boot health checks, and automated rollback orchestration. Those integrations must be verified separately; the presence of rollback primitives does not prove that a failed deployment will be detected or rolled back automatically.

---

## Representative implementation 1 — rpm-ostree / OSTree deployments

### Verified scope

The current rpm-ostree administrator handbook documents four primary client operations: `status`, `upgrade`, `rollback`, and `deploy <version>`.

- `rpm-ostree upgrade` prepares a new deployment offline and makes it the default for the next boot.
- `rpm-ostree rollback` swaps the default deployment with the previous deployment.
- `rpm-ostree deploy <version>` can select a version from server-side OSTree history.
- By default, upgrades retain at most two bootable deployments, although the underlying technology can support more.
- Package layering also constructs a new deployment rather than mutating the booted root by default.

The rpm-ostree project describes its update model as transactional and versioned/checksummed, with rollback of the OS while preserving user data outside the OS payload.

### Persistent-state boundary

The administrator handbook states that `/usr` is read-only in the normal model, while `/etc` and `/var` are writable. `/var` is shared across upgrades and is not changed by the base deployment transaction; `/etc` is merged with new defaults during upgrade handling.

This means an rpm-ostree rollback is **not** a rollback of arbitrary state in `/var`, databases, home directories, or external services.

### Important caveat — live apply

The documented `apply-live` path is materially different from the normal offline deployment model. rpm-ostree's own architecture documentation warns that live-applied `/etc` changes are not updated transactionally and configuration can leak from a partially applied live update.

Therefore:

- normal staged/offline deployment semantics and `apply-live` semantics must not be conflated;
- automation that requires transactional guarantees should explicitly record whether live application was used.

### Selection criteria

Prefer this model when:

- the distribution/platform is already OSTree/rpm-ostree based;
- bootable deployment history and OS-payload rollback are required;
- package layering is needed but full in-place package mutation is undesirable;
- `/var` persistence across OS deployments is an intentional design choice.

Do not choose it solely because "rollback" exists if the real requirement is rollback of mutable application/data state.

### Automation possibilities

Verified primitives support automation for:

- checking current and pending deployments with `rpm-ostree status`;
- preparing an update with `rpm-ostree upgrade`;
- pinning a known version with `rpm-ostree deploy <version>`;
- switching back with `rpm-ostree rollback`;
- serializing system mutations through the rpm-ostree daemon/transaction model.

A higher-level controller may combine these with post-boot health checks, but automatic health-triggered rollback is not established by the cited rpm-ostree sources themselves.

### Sources

- Source: rpm-ostree administrator handbook (official project documentation). Verified 2026-08-20. Scope: client administration, deployment/rollback, filesystem state boundaries.  
  https://coreos.github.io/rpm-ostree/administrator-handbook/
- Source: rpm-ostree project overview (official project documentation). Verified 2026-08-20. Scope: transactional image/package model and rollback boundary.  
  https://coreos.github.io/rpm-ostree/
- Source: rpm-ostree apply-live architecture (official project documentation). Verified 2026-08-20. Scope: live-apply caveats, especially `/etc`.  
  https://coreos.github.io/rpm-ostree/apply-live/
- Source: rpm-ostree daemon architecture (official project documentation). Verified 2026-08-20. Scope: mutation serialization and transactions.  
  https://coreos.github.io/rpm-ostree/architecture-daemon/

---

## Representative implementation 2 — bootc / bootable OCI operating-system images

### Verified scope

The bootable-container project defines bootc-style systems around OCI container images that contain the operating-system payload, including the kernel and system manager. The project states that:

- standard OCI/container build and registry workflows can produce the OS image;
- updates are intended to be atomic: the system should use either the old image or the new image, not a mixture;
- updates preserve machine state in writable areas such as `/etc` and `/var`;
- a previous bootable OS image can be selected for rollback;
- update checking, fetching, and application can be separated.

The documented update-service pieces are:

- `bootc upgrade --check`
- `bootc upgrade`
- `bootc upgrade --apply`

The upstream service documentation describes checking the registry, downloading a new image, and rebooting, with a companion systemd timer; distributions may choose different defaults.

### Trust and recovery boundaries

The project's goals describe support for signed images and a future/desired trust chain, but separate project documentation explicitly states that a complete hardware-to-application cryptographic trust chain is not yet fully implemented.

The same documentation also states that converting a non-bootc Linux system with `bootc install` cannot roll back to the previous non-bootc behavior.

Therefore:

- image rollback after the system is operating in the bootc model must not be generalized to migration rollback from an arbitrary pre-bootc installation;
- "OCI image" does not by itself prove end-to-end boot-chain integrity;
- `/etc` and `/var` persistence means image rollback is not arbitrary state rollback.

### Selection criteria

Prefer bootc-style delivery when:

- the OS should be built and promoted using OCI image pipelines and registries;
- fleet nodes should consume a prebuilt OS image rather than resolve fine-grained packages during deployment;
- update/check/fetch/apply phases need to be orchestrated separately;
- retained bootable image rollback matches the desired recovery boundary.

### Automation possibilities

Verified primitives support:

- registry-based update discovery;
- decoupled check/fetch/apply control;
- scheduled unattended update flows through systemd units/timers;
- CI/GitOps production of OS images with normal OCI build/test/sign/push tooling;
- boot selection/rollback to a previous bootable image.

Post-boot application/service health policy remains a separate layer unless an external orchestrator provides it.

### Sources

- Source: Bootable Container Images goals (official project documentation). Verified 2026-08-20. Scope: atomic update, rollback, persistent state, OCI/GitOps model and trust-chain goal.  
  https://containers.github.io/bootable/
- Source: Bootable Container Images architecture/how-it-works (official project documentation). Verified 2026-08-20. Scope: image application, reboot activation, rollback and `/etc`/`/var` persistence.  
  https://containers.github.io/bootable/how-does-it-work.html
- Source: `bootc-fetch-apply-updates.service` manual (official bootc documentation). Verified 2026-08-20. Scope: check/fetch/apply separation and timer-driven updates.  
  https://bootc-dev.github.io/bootc/man/bootc-fetch-apply-updates.service.5.html
- Source: Bootable Container Images "What needs work?" (official project documentation). Verified 2026-08-20. Scope: migration rollback and incomplete end-to-end trust-chain caveats.  
  https://containers.github.io/bootable/what-needs-work.html

---

## Representative implementation 3 — NixOS generations

### Verified scope

The current stable NixOS manual documents generation-based system configuration and several recovery paths:

- `nixos-rebuild switch` creates/activates a new system configuration;
- previous configurations remain selectable from the bootloader while retained;
- `nixos-rebuild switch --rollback` switches to the previous configuration;
- the booted generation can be made the default for subsequent boots;
- `dry-activate` can report activation actions without performing the switch.

The official NixOS Wiki further documents that previous system generations are retained until removed and that garbage collection can delete older generations. Deleting all previous generations removes that rollback path.

### State and rollback boundary

NixOS generations represent versioned system configurations/store closures and activation state. They must not be interpreted as snapshots of all writable data on the machine.

Garbage collection is operationally significant: once an old generation and its reachable store paths are removed, the previously available generation rollback may no longer be possible without rebuilding/refetching the required closure.

### Selection criteria

Prefer NixOS generation-based management when:

- declarative system configuration and reproducible closures are desired;
- operators need multiple retained bootable configurations;
- build, test, boot-only, dry-activation and immediate-switch workflows should be distinct;
- retention/garbage-collection policy can be managed explicitly.

### Automation possibilities

Verified primitives support:

- declarative build and activation via `nixos-rebuild`;
- non-activating builds and `dry-activate` inspection;
- rollback to the previous system generation;
- bootloader recovery into retained generations;
- explicit generation listing/switching and retention through garbage-collection policy.

A successful build or generation switch is not proof that application state, external dependencies, or service-level objectives are healthy.

### Sources

- Source: NixOS stable manual (official NixOS documentation). Verified 2026-08-20. Scope: rollback, bootloader generations, `switch-to-configuration`, dry activation and transactional Nix database note.  
  https://nixos.org/manual/nixos/stable/
- Source: Official NixOS Wiki — NixOS / generations (official project wiki). Verified 2026-08-20. Scope: generation creation, rollback and garbage-collection implications.  
  https://wiki.nixos.org/wiki/NixOS
- Source: Official NixOS Wiki — `nixos-rebuild` (official project wiki). Verified 2026-08-20. Scope: build/switch/test/boot/dry-activate and rollback modes.  
  https://wiki.nixos.org/wiki/Nixos-rebuild

---

## Cross-model comparison

| Evidence plane | rpm-ostree | bootc | NixOS |
|---|---|---|---|
| Desired-state identity | OSTree deployment/version plus optional layered RPM requests | OCI bootable image/reference | Declarative system configuration / Nix store closure / generation |
| Prepare without replacing current booted OS | Yes, normal operations create a pending deployment | Yes, image update is prepared for switch/reboot | Build creates a new generation before/while activation is selected |
| Typical activation boundary | Reboot for normal upgrade | Reboot for image update | `switch`, `boot`, `test`, or bootloader selection depending on action |
| Retained prior state | Bootable deployments; default upgrade policy typically retains at most two | Previous bootable image(s), subject to implementation/retention | Previous generations while not garbage-collected |
| Rollback primitive | `rpm-ostree rollback` | boot previous image / bootc rollback model | `nixos-rebuild switch --rollback` or boot previous generation |
| Mutable state excluded from OS rollback | `/var`; `/etc` has merge semantics | `/etc`, `/var` persist across image updates | General mutable runtime/application data are not made equivalent to system generation |
| Retention hazard | deployment retention/pinning policy | image/deployment retention policy | generation deletion / garbage collection |

The table is a semantic comparison, **not** a claim that the three systems provide equivalent security, trust, storage, package, or recovery guarantees.

## Integration points

A production SDLC may connect these systems to:

- CI that builds and tests OS images/configurations;
- provenance/signing/attestation systems;
- staged fleet rollout controls;
- reboot orchestration;
- health/SLO/crash/telemetry gates;
- incident response and rollback automation;
- retention/garbage-collection policies;
- application/database migration plans.

Each integration requires its own evidence. In particular, OS rollback must be coordinated with any application/database schema change whose backward compatibility is not guaranteed.

## AI-driven automation possibilities

AI can assist this plane by interpreting deployment status, proposing rollout or rollback actions, correlating post-boot incidents with recent OS generations/images, generating configuration changes, and preparing CI changes. The deterministic authority boundary should remain in explicit update/rollback commands, policy gates, health checks, and human/automation approvals.

No source reviewed in this run establishes a general-purpose AI system with autonomous authority to mutate these OS deployments and decide production rollback solely from model judgment. That capability remains **unresolved** and must not be inferred from the existence of command-line update primitives.

## Contradiction / deduplication pass

The following distinctions are intentional and must be preserved:

- rpm-ostree deployment rollback ≠ rollback of `/var` or external data.
- rpm-ostree normal offline deployment ≠ `apply-live`; `/etc` transactional guarantees differ.
- bootc image rollback ≠ rollback from a pre-bootc installation.
- bootc OCI delivery ≠ proof of a complete hardware-to-application trust chain.
- NixOS generation rollback ≠ filesystem/database snapshot rollback.
- retained generation/deployment ≠ backup.
- successful activation ≠ post-boot functional health.
- garbage collection/retention policy can destroy a previously available rollback path.

## Unresolved / open research

- First-class automatic post-boot health rollback in each ecosystem, where supported by separate authoritative components.
- Fleet orchestrators that coordinate these primitives across large node populations.
- Exact signature/provenance enforcement defaults for specific distributions built on rpm-ostree or bootc.
- Comparison with additional transactional/immutable systems such as transactional-update/MicroOS variants, Ubuntu Core, image-based appliance systems, or other declarative OS managers.
- Quantitative disk-space and retention trade-offs for maintaining safe rollback depth.
- Coordination of OS rollback with stateful application/database migrations.
- AI-operated OS maintenance with independently verified authority, policy, and recovery boundaries.
