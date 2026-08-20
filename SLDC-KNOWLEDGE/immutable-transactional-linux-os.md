# Immutable / transactional Linux OS update baseline

Verification date: 2026-08-20

## Scope

This file documents representative Linux operating-system update models where the update unit is larger than an ordinary package transaction and where previous system states are intentionally retained or addressable. It is an evidence-backed expansion of the general SDLC/release baseline; it is not a claim that all immutable, image-based, declarative, or transactional Linux systems are equivalent.

The baseline keeps these evidence planes separate:

1. desired/system definition;
2. update artifact or source identity;
3. pre-activation construction/staging;
4. activation boundary;
5. retained previous system state;
6. rollback/revert mechanism;
7. persistent configuration/data boundary;
8. garbage collection/history retention;
9. trust/integrity policy;
10. post-update functional health.

A successful transactional update proves only that the system reached the updater's accepted state. It does not prove application correctness, data compatibility, external-side-effect reversal, or business-level health.

## 1. rpm-ostree

### Definition and SDLC role

`rpm-ostree` is a hybrid image/package system built around OSTree plus RPM/libdnf integration. The upstream project documents transactional, versioned/checksummed operating-system deployments, package layering and rollback. Development focus has shifted toward bootc/dnf for new bootable-container features, while rpm-ostree remains supported and widely deployed.

### Verified lifecycle

- `rpm-ostree upgrade` prepares a new deployment offline and makes it the default for the next boot.
- By default, ordinary rpm-ostree operations do not mutate the currently booted root; changes become active after reboot.
- `rpm-ostree rollback` swaps the default deployment with the retained previous deployment.
- `rpm-ostree deploy <version>` can select a specific server-side historical version, enabling deterministic pinning/testing workflows where history is available.
- The default deployment model normally retains at most two bootable deployments, although the underlying technology can retain more.
- Package layering and overrides create derived deployments rather than conventional in-place package mutations.

### Persistent-state boundary

The upstream rpm-ostree overview explicitly describes OS rollback as affecting the versioned operating-system content while not generally rolling back user/state locations such as `/var`; `/etc` has separate semantics from immutable `/usr`. Therefore an OS deployment rollback must not be represented as application/database/user-data rollback.

### Selection criteria

Prefer this model when a Fedora-family system already depends on rpm-ostree, when bootable deployment history and package layering are operational requirements, or when offline activation is desirable. Do not choose it solely because a generic workload needs package management; conventional package managers and newer bootc image-mode systems have different operational contracts.

### Integration and automation

Automation can:

- check current/pending deployments with `rpm-ostree status`;
- stage an upgrade;
- pin or deploy a tested historical version where upstream history is available;
- reboot through an external orchestration layer;
- verify booted deployment identity after restart;
- roll back to the retained deployment when deterministic policy requires it.

AI may help interpret status, diagnostics or rollout evidence, but no inspected primary source establishes AI as a trusted authority to select production deployments or declare health. Promotion remains behind deterministic deployment identity and post-boot health checks.

### Caveats

- Rollback requires a usable retained deployment.
- Local/package-layer overrides are part of the deployment model and can affect reproducibility if not captured as intended state.
- `apply-live` and transient `/usr` overlays are exceptional paths and must not be treated as equivalent to the default offline transactional deployment model.
- Upstream states that major new bootable-container functionality is expected to land primarily in bootc/dnf rather than rpm-ostree.

## 2. bootc / bootable container images

### Definition and SDLC role

bootc applies an OCI bootable container image as the operating-system update source. The bootable-container project documents OCI images containing the OS userspace, kernel and system manager; standard container build pipelines can build/test/push these images before hosts consume them.

This makes the image digest/tag and the build pipeline central release artifacts rather than a sequence of independent host package transactions.

### Verified lifecycle

Current bootc documentation separates automatic update activity into independently callable steps:

- `bootc upgrade --check` — discover whether an updated source image is available;
- `bootc upgrade` — fetch/stage the update;
- `bootc upgrade --apply` — apply through the update/reboot path documented by the service workflow.

The upstream `bootc-fetch-apply-updates.service` checks the source registry, downloads a newer image when available and reboots; a companion timer is supplied, while distributions may choose different defaults.

Bootable-container documentation states that the boot loader can return to the previous operating-system image. Per-system state such as `/etc` and `/var` is generally outside the bootable image replacement and persists across image updates.

### Selection criteria

Prefer bootc when the desired OS release artifact is itself an OCI image and the organization already has container image build, registry, signing/promotion and scanning workflows. This can reduce divergence between image construction and deployed OS content.

Do not infer that container-image familiarity alone provides a complete OS trust chain or recovery design.

### Integration and automation

A deterministic pipeline can:

1. build the bootable OCI image from version-controlled inputs;
2. test the image before registry promotion;
3. record an immutable digest rather than rely only on a mutable tag;
4. scan/sign/attest the image using the repository's separate supply-chain controls;
5. publish it to an approved registry/channel;
6. stage/check updates on hosts;
7. reboot in a controlled maintenance/progressive-delivery window;
8. verify booted image identity and service health;
9. invoke previous-image recovery when supported and policy permits.

### Caveats and unresolved trust boundary

The inspected bootable-container project documentation explicitly states that a complete cryptographic trust chain from hardware through application containers has not yet been fully implemented in that project description. Therefore "OCI image" must not be equated with a complete verified-boot or end-to-end supply-chain guarantee.

The documentation also distinguishes conversion/installing a non-bootc system from normal bootc updates: replacing a stock Linux installation with bootc is not documented as reversibly returning to the previous stock-system behavior. That migration boundary is separate from rollback between retained bootc OS images.

## 3. NixOS generations

### Definition and SDLC role

NixOS uses a declarative system configuration and stores built system closures in the Nix store. `nixos-rebuild` creates new system generations instead of overwriting previous system closures in place. Previous generations can remain bootable and selectable until their roots are deleted/garbage-collected.

### Verified lifecycle

Current official NixOS documentation supports these distinct activation modes:

- `nixos-rebuild build` — build without activating;
- `nixos-rebuild test` — activate for the running system without making the generation the persistent boot default;
- `nixos-rebuild boot` — make the generation the next-boot default without switching the running system immediately;
- `nixos-rebuild switch` — activate the new generation now and make it the default;
- `nixos-rebuild switch --rollback` — return to the previous system generation.

Older retained generations are also available from the bootloader, allowing recovery when a newly selected generation does not boot correctly.

### Retention / garbage-collection boundary

NixOS retains old system generations as garbage-collector roots. The official manual states that ordinary garbage collection does not necessarily remove these roots, while destructive generation cleanup such as `nix-collect-garbage -d` removes old generations and therefore removes the ability to roll back to them.

Retention is thus a direct part of rollback availability and must be treated as policy rather than invisible implementation detail.

### Selection criteria

Prefer NixOS generations where declarative whole-system composition, reproducible derivations, explicit build-before-activate workflows and generation-based rollback fit the operating model.

Do not generalize NixOS rollback to mutable application data or arbitrary external services. The generation identifies system configuration/store closures, not the full state of every database, filesystem location, cloud resource or remote dependency.

### Integration and automation

Automation can use a staged sequence such as:

1. evaluate/build the intended configuration;
2. run tests or `build-vm`/other environment-specific validation where appropriate;
3. record the configuration source revision and resulting generation/closure identity;
4. activate with `test`, `boot`, or `switch` according to rollout policy;
5. execute deterministic service/application health checks;
6. roll back to a retained generation when policy criteria fail;
7. garbage-collect old generations only after the required recovery window has expired.

### Caveat: Nix/channel downgrade

The official NixOS manual warns that switching back and forth between channels is generally possible, but a newer Nix version can upgrade Nix's database schema in a way that is not easily undone. Therefore generation rollback must not be advertised as a universal reversal of every underlying state/schema transition.

## Cross-model comparison

| Plane | rpm-ostree | bootc | NixOS |
|---|---|---|---|
| Primary OS update identity | OSTree/rpm-ostree deployment | OCI bootable image | NixOS system generation / closure |
| Default activation pattern | staged offline; reboot | image fetch/stage then reboot/apply | build/test/boot/switch modes |
| Previous-system recovery | retained deployment / `rollback` | previous bootable OS image | retained generation / bootloader / `--rollback` |
| Persistent state outside OS payload | yes; notably mutable state is not equivalent to deployment | `/etc` and `/var` generally persist | mutable application/data state is not represented by system generation alone |
| History retention affects rollback | yes | yes, previous image availability matters | yes; deleting old generations removes rollback capability |
| Package-level mutation model | hybrid layering/overrides | image rebuild is the preferred OS mutation model | declarative package/system composition |
| Complete functional-health proof | no | no | no |

## Baseline selection rules

1. Select the update model based on the authoritative system definition and recovery contract, not the label "immutable".
2. Require immutable or otherwise auditable release identity for production promotion.
3. Separate build success from boot success and boot success from service/application health.
4. Test recovery before depending on it operationally.
5. Define retention policy from the required rollback window; garbage collection/history pruning can destroy recovery capability.
6. Model mutable state separately. OS rollback cannot be assumed to downgrade databases, `/var` data, remote APIs, cloud resources or firmware.
7. Keep supply-chain trust separate from transactional activation. A transaction can apply an untrusted artifact consistently.
8. Keep transactional consistency separate from availability. A valid new generation/image can still fail to boot on specific hardware or fail application-level SLOs.

## AI-driven automation opportunities

Evidence-supported underlying mechanisms allow AI-assisted workflows around:

- summarizing update diffs and release metadata;
- selecting candidate tests based on changed components;
- interpreting deployment/status output;
- correlating boot/service failures with an update;
- proposing a rollback or retained-generation choice;
- generating human-reviewable rollout plans and recovery commands;
- checking whether retention/recovery prerequisites appear present.

The production authority boundary remains deterministic: AI output should not by itself authorize OS promotion, deletion of rollback generations, forced reboot, trust-policy bypass, or recovery completion. Those actions require explicit policy plus inspected deployment identity and health evidence.

## Contradictions intentionally preserved

- rpm-ostree rollback ≠ bootc previous-image rollback ≠ NixOS generation rollback.
- Transactional/atomic activation ≠ application transactionality.
- Previous OS content ≠ previous database/user-data state.
- OCI image ≠ complete cryptographic trust chain.
- Declarative configuration ≠ guaranteed runtime correctness.
- Boot success ≠ service health ≠ SLO satisfaction.
- Retained history ≠ backup.
- Garbage collection is operationally relevant because it can remove rollback material.

## Unresolved / open research

- exact current trust-policy defaults and signed-image enforcement across Fedora/CentOS bootc distributions;
- rpm-ostree/bootc behavior under storage exhaustion, interrupted fetch/finalization, bootloader failure and multi-disk layouts;
- NixOS rollback behavior for stateful service migrations beyond the system generation itself;
- additional transactional/immutable systems such as openSUSE transactional-update/MicroOS, Fedora Atomic variants beyond their shared mechanisms, Ubuntu Core and other image-based OSes;
- independently measured fleet-scale failure/recovery characteristics;
- post-boot health-driven automatic rollback implementations with authoritative current evidence;
- AI systems with explicit, documented authority over production OS update promotion or rollback.

## Sources

All sources verified 2026-08-20.

### rpm-ostree

- rpm-ostree Administrator Handbook — official upstream documentation: https://coreos.github.io/rpm-ostree/administrator-handbook/
- rpm-ostree project overview — official upstream documentation: https://coreos.github.io/rpm-ostree/

### bootc / bootable containers

- bootc automatic update service — official upstream documentation: https://bootc-dev.github.io/bootc/man/bootc-fetch-apply-updates.service.5.html
- Bootable Container Images, how it works — upstream project documentation: https://containers.github.io/bootable/how-does-it-work.html
- Bootable Container Images, known work/trust limitations — upstream project documentation: https://containers.github.io/bootable/what-needs-work.html

### NixOS

- NixOS Manual, stable — official project documentation: https://nixos.org/manual/nixos/stable/
- How Nix Works / rollbacks — official project documentation: https://nixos.org/guides/how-nix-works/
- `nixos-rebuild` — Official NixOS Wiki: https://wiki.nixos.org/wiki/Nixos-rebuild
