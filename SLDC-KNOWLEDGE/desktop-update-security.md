# Desktop update security and rollback boundaries

Verification date: 2026-08-20

Scope: representative evidence for desktop software distributed outside app stores. This file covers update trust, update metadata, signing, automated update policy, downgrade/rollback semantics, and deterministic verification boundaries. It does not claim exhaustive coverage of desktop updater frameworks or every installer format.

## Baseline definition

A desktop updater is part of the release/deployment plane. A safe baseline separates at least these concerns:

1. **Update discovery** — how the client learns that an update exists.
2. **Metadata authenticity/freshness** — how the client decides that version and target metadata are trustworthy and current.
3. **Artifact authenticity/integrity** — how downloaded executable content is authenticated and checked for corruption/tampering.
4. **Installation policy** — whether an update is background, prompted, mandatory, or deferred.
5. **Version-transition policy** — whether only upgrades are allowed or explicit downgrade is supported.
6. **Post-update verification/recovery** — whether a failed or unhealthy installation can be detected and whether reverting application binaries/state is actually supported.

These are separate evidence planes. A signed package does not by itself prove freshness, safe installation, application health, data-schema compatibility, or recoverability.

## The Update Framework (TUF): updater trust model

Source type: official project documentation and specification.

Sources:

- https://theupdateframework.io/docs/metadata/
- https://theupdateframework.io/docs/security/
- https://theupdateframework.github.io/specification/v1.0.26/

Verified scope:

- TUF defines four required top-level metadata roles: `root`, `targets`, `snapshot`, and `timestamp`.
- Targets metadata identifies target files and their hashes/sizes; snapshot metadata binds a consistent set of targets metadata; timestamp metadata is short-lived and helps clients detect stale/frozen repository state; root metadata defines trusted keys and signature thresholds.
- The specification includes explicit client checks intended to detect rollback, freeze, mix-and-match, arbitrary-software, and wrong-software attacks.
- Trusted metadata versions are persisted so a client can reject older metadata it has already superseded.

Selection criteria:

- Use a TUF-style design when the updater threat model includes repository/mirror compromise, stale metadata, key compromise boundaries, rollback/freeze attacks, or delegated signing responsibility.
- Separate online timestamp keys from more sensitive signing roles when the implementation follows TUF's role model.
- Treat metadata expiration, version monotonicity, signature threshold, target hash, and target length checks as deterministic gates.

Integration points:

- release artifact publication;
- signing/key-management systems;
- mirrors/CDNs;
- updater clients;
- CI/CD metadata generation and validation;
- incident/key-rotation procedures.

Automation possibilities:

- generate and sign metadata in release pipelines;
- validate role signatures, expiry, monotonic versions, hashes and lengths before publication;
- test clients against stale, rollback and mix-and-match fixtures;
- alert on approaching metadata expiration or failed signature/freshness checks.

Caveat:

TUF secures update metadata and target selection. It is **not** evidence that a newly installed application is healthy, that application data can be downgraded, or that an installed bad release will be automatically reverted.

## Windows outside the Microsoft Store: MSIX + App Installer

Source type: current Microsoft documentation.

Sources:

- https://learn.microsoft.com/en-us/windows/msix/package/signing-package-overview
- https://learn.microsoft.com/en-us/windows/msix/package/sign-msix-package-guide
- https://learn.microsoft.com/en-us/windows/msix/app-installer/auto-update-and-repair--overview
- https://learn.microsoft.com/en-us/windows/msix/app-installer/update-settings
- https://learn.microsoft.com/en-us/windows/apps/package-and-deploy/choose-distribution-path

Verified scope:

- Windows requires deployable MSIX packages to be signed with a valid code-signing certificate, and the signing identity must be trusted on the target device.
- For direct/non-Store MSIX distribution, an `.appinstaller` file can provide an update channel hosted by the publisher.
- App Installer supports update checks on launch and background update checks.
- `ShowPrompt` and `UpdateBlocksActivation` can require a user to take an available update before launching the application.
- `ForceUpdateFromAnyVersion` explicitly allows both moving to a newer version and moving to an older version. Without it, only an upward version transition is allowed.
- Microsoft documents auto-update/repair support for Windows 10 version 2004 (build 19041) and later and Windows 11; individual App Installer settings have older minimum-version requirements documented separately.

Selection criteria:

- Prefer MSIX/App Installer when Windows package identity and OS-managed direct-update behavior fit the application and non-Store distribution is required.
- Production signing must use a trust model appropriate to the distribution population; Microsoft explicitly limits self-signed certificates to development/testing or managed trust scenarios.
- Decide explicitly whether activation may proceed on an old version, whether update prompts are shown, and whether downgrade is permitted.

Integration points:

- package build and signing;
- `.appinstaller` publication endpoint;
- Windows App Installer repository/settings;
- enterprise CSP/management policy;
- CI/CD versioning and package-validation gates.

Automation possibilities:

- sign MSIX artifacts in CI/CD using an approved signing mechanism;
- validate manifest publisher identity and package signatures before publication;
- generate/update `.appinstaller` metadata;
- test mandatory-update and downgrade paths in clean Windows environments;
- verify the installed package version after update.

Caveats:

- `ForceUpdateFromAnyVersion` proves that App Installer can perform a lower-version package transition; it does **not** prove that application data, external services, user configuration, migrations, or side effects are downgrade-safe.
- `UpdateBlocksActivation` is an enforcement control for package currency, not a health check for the new release.
- A trusted signature authenticates the signed publisher/package; it does not prove the package is functionally correct or non-malicious.

## macOS outside the Mac App Store: Sparkle 2

Source type: official Sparkle maintainer documentation.

Sources:

- https://sparkle-project.org/documentation/
- https://sparkle-project.org/documentation/publishing/
- https://sparkle-project.org/documentation/security-and-reliability/
- https://sparkle-project.org/documentation/upgrading/
- https://sparkle-project.org/documentation/delta-updates/

Verified scope:

- Sparkle 2 provides automatic update checking/install flows for macOS applications using an appcast feed.
- Maintainers recommend HTTPS, Apple Developer ID code signing/notarization where applicable, and Sparkle EdDSA (`ed25519`) signatures for published update archives, delta updates and installer packages.
- `generate_appcast` can generate appcast metadata, signatures, and delta-update metadata from release artifacts.
- Sparkle can optionally require signed feeds (`SURequireSignedFeed`), with `SUVerifyUpdateBeforeExtraction` as a prerequisite.
- Sparkle supports binary delta updates and falls back to a full update when a suitable/applicable delta is unavailable.
- Current Sparkle 2 migration documentation states that downgrade support present in Sparkle 1 was removed in Sparkle 2.
- Sparkle's documentation recommends testing updater behavior with genuine old/new application versions; delta-update testing requires matching source versions/checksums.

Selection criteria:

- Use Sparkle when a macOS application is distributed outside the Mac App Store and its trust/update model fits Sparkle's appcast and signing design.
- Protect update-signing private keys separately from public hosting infrastructure.
- Treat key rotation as an explicit lifecycle operation; Sparkle documents constraints for rotating Apple code-signing and EdDSA keys.
- Do not select Sparkle 2 on the assumption that it provides a generic downgrade/rollback mechanism; current documentation says downgrade support was removed.

Integration points:

- Xcode archive/distribution pipeline;
- Developer ID signing/notarization;
- Sparkle EdDSA keys;
- appcast/CDN publication;
- CI-generated signatures/deltas;
- application relaunch/update UX.

Automation possibilities:

- run `generate_appcast` in a controlled release pipeline;
- sign update artifacts and validate signatures before publication;
- generate and test delta updates;
- exercise update-from-N-1/N-2 fixtures and verify relaunch/version state;
- verify signing/notarization and updater logs as release evidence.

Caveats:

- Sparkle's archive/feed verification and code-signing controls are updater trust controls, not proof of application correctness.
- Sparkle 2's documented removal of downgrade support means a generic automatic rollback capability must not be inferred.
- Package updates have additional limitations documented by Sparkle, including authorization requirements and reduced key-rotation/delta tooling compared with regular app-bundle updates.

## Cross-platform baseline selection

Choose/update the mechanism only after answering:

- What is the trusted root of update authority?
- Can a compromised web/CDN origin substitute executable content or stale metadata?
- Are metadata freshness and rollback/freeze attacks in scope?
- Are signing keys online, offline, thresholded, rotated, recoverable, and auditable?
- Is update installation optional, background, forced before launch, or policy-controlled?
- Does the mechanism support downgrade, and is downgrade safe for application state?
- What evidence proves the new application actually launches and meets health criteria?
- What happens if the updater itself becomes unable to verify future updates?
- Can the release channel be paused independently of reversing already installed updates?

## AI-driven automation boundary

No primary source inspected in this slice establishes an AI system as a trusted authority for desktop update signing, freshness validation, downgrade safety, or post-update health.

Evidence-backed deterministic automation remains the baseline:

- cryptographic signing and signature verification;
- metadata freshness/version/hash validation;
- updater integration tests across old/new versions;
- clean-environment installation tests;
- explicit post-update launch/version/health checks;
- controlled key rotation and audit trails.

AI may assist with release analysis, failure triage, documentation, test generation, or change proposals only if its outputs remain behind these deterministic gates. A claim that an AI-specific desktop updater can autonomously authorize or safely roll back production releases remains **unresolved** in this research slice.

## Contradiction and deduplication notes

- This file does not duplicate store rollout semantics from `store-and-fleet-release-safety.md`.
- It does not duplicate general progressive-delivery/Kubernetes rollback controls from `release-deployment-progressive-delivery.md`.
- It complements `supply-chain-security-fuzzing.md`: TUF update metadata/target trust is related to supply-chain integrity but is not identical to SLSA provenance or Sigstore artifact signing.
- Windows App Installer downgrade support and Sparkle 2's removal of downgrade support are intentionally recorded as different implementation semantics rather than normalized into a false cross-platform capability.

## Unresolved frontier

- first-class automatic post-install rollback/health recovery for representative desktop updater systems;
- Windows updater paths for MSI/EXE and additional frameworks beyond MSIX/App Installer;
- additional macOS updater implementations independent of Sparkle;
- Linux desktop/self-update mechanisms and package-manager interactions;
- cross-platform updater frameworks and comparative threat models;
- update-health telemetry that can automatically pause promotion without granting unverified rollback authority;
- AI-specific desktop release/updater automation with documented authority and deterministic verification boundaries.
