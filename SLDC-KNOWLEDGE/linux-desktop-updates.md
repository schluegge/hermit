# Linux desktop update channels and self-update boundaries

Verification date: 2026-08-20

Scope: representative Linux desktop application update mechanisms outside distribution-specific DEB/RPM package-manager policy. This file covers Flatpak, Snap, and AppImage/AppImageUpdate as three materially different delivery/update models. It does not claim exhaustive coverage of Linux package managers, distributions, immutable OS update systems, or every desktop updater framework.

## Baseline definition

A Linux desktop update baseline should separate at least:

1. **Distribution authority** — who publishes/authorizes the application revision or update metadata.
2. **Update discovery** — how the installed application/runtime learns about a new revision.
3. **Artifact/repository authenticity** — what trust/signature mechanism protects the delivered content.
4. **Refresh policy** — automatic, user-triggered, scheduled, held, masked, or application-controlled behavior.
5. **Version transition** — whether an older revision can be selected and what exactly is reverted.
6. **Application-data semantics** — whether configuration or user data follows the binary revision transition.
7. **Health/recovery** — whether post-update failure can abort/roll back installation and whether application-level correctness is actually checked.

These are separate evidence planes. A mechanism that can install an older binary revision does not by itself prove application-data compatibility or safe rollback of external side effects.

## Flatpak

Source type: official Flatpak documentation.

Sources:

- https://docs.flatpak.org/en/latest/using-flatpak.html
- https://docs.flatpak.org/en/latest/repositories.html
- https://docs.flatpak.org/en/latest/tips-and-tricks.html
- https://docs.flatpak.org/en/latest/flatpak-devel.html
- https://docs.flatpak.org/en/latest/flatpak-builder.html

Verified scope:

- Flatpak applications and runtimes are installed from configured remotes; `flatpak update` updates installed refs to newer revisions from their remotes.
- Flatpak repositories retain versioned application/runtime objects and use OSTree-style content/version history; repository publication can use static deltas.
- `.flatpakref` and `.flatpakrepo` metadata can carry the repository GPG key; Flatpak documentation recommends signed repository commits and repository verification.
- A specific older commit can be selected with `flatpak update --commit=<COMMIT> <REF>`; for system installations this downgrade is treated as a privileged operation.
- `flatpak mask` can prevent a ref/pattern from being automatically updated or installed.
- `flatpak history` exposes installation/update history, and `flatpak repair` repairs inconsistencies in a local installation.
- Stable and nightly/development variants can be installed in parallel when distinct application IDs are used; the documentation recommends separate IDs (for example a `.Devel` suffix) to avoid configuration and D-Bus conflicts.

Selection criteria:

- Prefer Flatpak when repository-based desktop distribution, sandboxing/runtime integration, per-user or system installation, and commit-addressable application/runtime history fit the product.
- Treat repository signing/trust configuration as part of release policy rather than assuming every configured remote has equivalent trust.
- Decide whether update suppression should use explicit masking and whether downgrade is an operator/user recovery mechanism or a supported application-state transition.

Integration points:

- application manifest/build pipeline (`flatpak-builder`);
- repository publication and GPG signing;
- Flathub or self-hosted Flatpak remotes;
- software-center frontends such as GNOME Software/KDE Discover;
- CI tests for stable/development IDs and runtime compatibility;
- update/downgrade regression fixtures.

Automation possibilities:

- build and test Flatpak manifests in CI;
- sign/export repository commits and generate repository metadata/deltas;
- run non-interactive update/install checks in disposable environments;
- exercise N-1/N-2 commit downgrades and verify launch/data compatibility;
- inspect `flatpak history` and installed commit IDs as release evidence;
- mask a known-bad ref as a containment action where policy allows.

Caveats:

- Flatpak commit rollback/downgrade is not evidence that application-owned data schemas, external services, or side effects are reversible.
- A repository signature authenticates repository content under the configured trust root; it does not prove functional correctness.
- Runtime updates are a different compatibility plane from deliberately switching application branches or IDs.

## Snap / snapd

Source type: current Canonical Snap documentation.

Sources:

- https://snapcraft.io/docs/how-to-guides/manage-snaps/manage-updates/
- https://snapcraft.io/docs/reference/development/supported-snap-hooks/
- https://snapcraft.io/docs/explanation/how-snaps-work/transactional-updates/
- https://snapcraft.io/docs/explanation/security/security-policies/
- https://snapcraft.io/docs/reference/interfaces/snap-refresh-control-interface/

Verified scope:

- Published snaps refresh automatically; current documentation says snapd checks for updates four times per day by default, with configurable scheduling/hold behavior.
- `snap refresh --hold` can postpone automatic refreshes; current docs describe per-snap and system-wide hold semantics and their different effect on manual targeted refreshes.
- `snap revert` can select a previous or specified retained revision. The operation reverts the snap revision and revision-specific configuration/system data handled by snapd, but common user data is not generally reverted.
- `refresh.retain` controls how many revisions snapd retains after refresh, subject to documented bounds/defaults.
- `pre-refresh` and `post-refresh` hooks allow package-defined checks/maintenance around a refresh. Current hook documentation states that failure of `post-refresh` rolls back the refresh and restores the original snap state.
- Snap supports all-snaps transactional install/refresh with `--transaction=all-snaps`: if one snap in the transaction fails, affected snaps return to their pre-transaction state.
- Application-controlled `gate-auto-refresh` / `snap-refresh-control` capabilities exist, but current official documentation still labels the relevant refresh-control feature/interface experimental or under development and super-privileged where applicable.

Selection criteria:

- Prefer Snap when snapd-managed automatic refresh, channel tracking, retained revisions, confinement/interfaces, and Canonical/Snap Store or managed-store workflows fit the target fleet.
- Treat automatic refresh, explicit hold, targeted manual refresh, application refresh awareness, and privileged refresh-control as separate policy mechanisms.
- Do not depend on experimental refresh-control interfaces as a stable production contract without independently validating the deployed snapd version and policy.

Integration points:

- Snap Store/channel promotion;
- snapd refresh scheduler and holds;
- `pre-refresh`/`post-refresh` hooks;
- services managed by snapd/systemd;
- retained revision storage;
- CI/device-fleet update and revert tests.

Automation possibilities:

- promote tested revisions between channels under release policy;
- schedule or hold refreshes for controlled rollout windows;
- implement deterministic pre/post-refresh health checks;
- run transactional multi-snap refreshes when revisions must change together;
- validate installed revision/channel and service health after refresh;
- exercise `snap revert` in staging and verify which configuration/user-data planes actually change.

Caveats:

- Current Canonical documentation explicitly notes that ordinary user data is often stored outside revision-specific directories and is **not** reverted by `snap revert`.
- `post-refresh` rollback proves package/update transaction recovery under snapd semantics, not universal reversal of external database, network, or hardware effects.
- A hold is containment of future refresh activity, not rollback of already updated installations.
- Experimental/super-privileged refresh-control features must not be treated as universally available.

## AppImage and AppImageUpdate

Source type: official AppImage documentation and AppImageCommunity maintainer repository.

Sources:

- https://docs.appimage.org/packaging-guide/optional/updates.html
- https://docs.appimage.org/packaging-guide/optional/signatures.html
- https://docs.appimage.org/packaging-guide/distribution.html
- https://github.com/AppImageCommunity/AppImageUpdate

Verified scope:

- AppImages can be made updateable by embedding update information that tells tooling where/how to find newer content; the documented zsync path enables delta downloads.
- Updating can be performed by external `AppImageUpdate`/`appimageupdatetool`, by bundling updater functionality into the AppImage, or by integrating `libappimageupdate`.
- The model is decentralized: update information travels with the AppImage instead of requiring a system repository definition.
- AppImages can carry an embedded GPG signature. The official documentation distinguishes displaying an embedded signature from actually validating it; validation requires an external validator/tooling path.
- AppImage documentation recommends publishing upstream-produced AppImages directly and documents CI-oriented packaging/update-information generation.
- The current AppImageCommunity/AppImageUpdate repository explicitly describes its implementation as **beta-level code** and says real-world experience is limited.

Selection criteria:

- Prefer AppImage when a portable single-file application and publisher-controlled/decentralized update channel fit the product.
- Require explicit update-information generation and signature-validation policy; do not infer that every AppImage is updateable or signed.
- Treat the beta lifecycle state of AppImageUpdate as a material product-selection caveat for critical unattended production update flows.

Integration points:

- AppImage build tooling (`appimagetool`, linuxdeploy and related tooling);
- publisher web/CDN endpoint supporting the chosen update mechanism;
- embedded update information / `.zsync` metadata;
- GPG signing and independent signature validation;
- application-integrated or external updater UX;
- CI release artifacts and update tests.

Automation possibilities:

- inject update information while packaging and generate `.zsync` metadata;
- sign AppImages and independently validate the resulting signature before publication;
- automate delta-update tests from real previous releases;
- retain the previous AppImage as an explicit operator/user recovery artifact;
- verify resulting executable identity/version and application health after update.

Caveats:

- Updateability is optional; an arbitrary AppImage cannot be assumed to carry usable update information.
- Embedded signature presence is not signature validation.
- AppImageUpdate's maintainer-stated beta status prevents treating it as an evidence-backed universally mature unattended updater.
- The inspected sources do not establish a first-class automatic application-health rollback mechanism comparable to a transactional package manager; that capability remains unresolved.

## Cross-model comparison and selection

The three verified models must not be collapsed into one generic "Linux updater" capability:

| Plane | Flatpak | Snap | AppImage/AppImageUpdate |
|---|---|---|---|
| Distribution model | versioned remote repository | snapd + channels/store/managed store | publisher-controlled portable file/update information |
| Typical refresh trigger | explicit CLI or software-center automation | automatic snapd refresh by default; policy can hold/schedule | external/in-app updater when update information exists |
| Older revision selection | explicit commit downgrade | `snap revert` to retained revision | previous file can be retained manually; no inspected first-class transactional revert contract |
| Data rollback guarantee | not established for application-owned data | revision-specific snap data can revert; common user data may not | not established |
| Update suppression | `flatpak mask` | holds/scheduling; experimental gated controls exist | publisher/user updater behavior; no common system policy established in inspected evidence |
| Post-update automatic rollback | not established by inspected Flatpak sources | `post-refresh` failure can roll refresh back | unresolved in inspected sources |

Selection therefore depends on required authority, update cadence, system integration, trust model, data semantics, unattended operation, and recovery requirements rather than on package format alone.

## Package-manager interaction boundary

This research slice intentionally does **not** generalize from Flatpak/Snap/AppImage to distribution-native package managers such as APT/dpkg, DNF/RPM, Zypper, Pacman, Nix, or transactional/immutable OS update systems. Their repository trust, dependency solving, transaction, rollback, service restart and OS/application ownership semantics differ materially.

A claim such as "Linux desktop updates can always roll back" or "self-update should bypass the system package manager" is therefore unsupported. Distribution-native package-manager and immutable-OS update policy remains a separate unresolved expansion area.

## AI-driven automation boundary

No inspected primary source establishes an AI system as the trusted authority for Linux desktop package signing, repository trust, automatic refresh authorization, application-data rollback, or post-update recovery.

Evidence-backed automation remains deterministic:

- build/package validation;
- artifact/repository signing and signature checks;
- release-channel or remote publication;
- update/refresh scheduling and holds;
- explicit downgrade/revert testing;
- post-update version/launch/service/health verification;
- audit/history capture.

AI may assist with release analysis, failure triage, test generation, or proposed remediation only behind those deterministic gates. AI authority over production Linux desktop update promotion or rollback remains **unresolved**.

## Contradiction and deduplication notes

- This file extends, rather than duplicates, `desktop-update-security.md`: that file provides TUF, Windows MSIX/App Installer and macOS Sparkle evidence; this file adds Linux-specific delivery/update semantics.
- Flatpak downgrade, Snap revert, and retaining an older AppImage are intentionally not treated as equivalent rollback guarantees.
- Snap's `post-refresh` rollback and all-snaps transaction semantics are stronger package-transaction evidence than a simple binary downgrade, but still do not prove reversal of arbitrary external side effects.
- AppImage's decentralized update model is not a repository/package-manager model and must not inherit Flatpak/Snap guarantees by analogy.
- Snap refresh-control capabilities that current docs label experimental/under-development remain so; their existence is not converted into a stable baseline requirement.

## Unresolved frontier

- distribution-native desktop package managers: APT/dpkg, DNF/RPM, Zypper, Pacman and their update/rollback/transaction semantics;
- immutable/transactional Linux OS update systems and application interaction (for example rpm-ostree/bootable-container or Nix-style generations) based on current primary evidence;
- first-class application-health-driven rollback for Flatpak/AppImage and broader Linux desktop channels;
- cross-format application-data migration and downgrade safety;
- independent security/threat-model comparison across Flatpak, Snap and AppImage update paths;
- additional cross-platform desktop updater frameworks;
- AI-specific Linux release/update automation with explicit production authority and deterministic verification boundaries.
