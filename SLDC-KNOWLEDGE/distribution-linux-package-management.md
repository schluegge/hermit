# Distribution-native Linux package management

Verification date: 2026-08-20

Status: **verified representative**

## Baseline definition

Distribution-native package management is the repository/transaction layer that discovers, resolves, authenticates, installs, upgrades, removes, and sometimes downgrades operating-system packages and their dependencies. It is distinct from application-specific self-updaters, sandboxed app stores, filesystem snapshot systems, and immutable-image update systems.

This baseline documents representative current implementations for Debian-family APT/dpkg, RPM-family DNF5/RPM, SUSE Zypper with Snapper/transactional-update, and Arch Linux Pacman. It does not claim that their transaction, trust, or rollback semantics are interchangeable.

## SDLC and operations role

Distribution package managers participate in environment provisioning, dependency installation, base-image creation, security patching, CI runner maintenance, development workstation baselines, deployment hosts, and incident/recovery workflows. For automation, the important evidence planes are:

1. repository metadata freshness and trust;
2. dependency resolution and proposed transaction;
3. package/artifact authentication;
4. transaction execution;
5. post-transaction package/file verification;
6. hold/exclusion/pinning policy;
7. downgrade or transaction reversal capability;
8. filesystem/system recovery capability;
9. application/data-state verification after package changes.

A successful package transaction proves only the package-manager transaction outcome within its documented scope. It does not prove that applications start, migrations are reversible, user/application data is compatible, or the host satisfies a higher-level service SLO.

## APT / dpkg family

### Verified implementation and semantics

Current Debian APT documentation describes `apt`/`apt-get` as package-management front ends over configured sources. `apt update` refreshes package metadata; `upgrade` installs available upgrades without removing installed packages, while `full-upgrade` may remove installed packages when necessary to upgrade the system as a whole.

`apt-mark hold` prevents a package from being automatically installed, upgraded, or removed until the hold is cleared. APT also tracks manually versus automatically installed packages, which affects autoremove decisions.

APT's trust model is repository-oriented. `apt-secure` verifies signed Release metadata and chains package checksums through the signed repository metadata. Current APT refuses unsigned repositories by default. The documentation explicitly distinguishes this from per-package signatures: authenticating an archive means trusting the archive maintainer and integrity chain, not proving that package contents are non-malicious.

Current source configuration supports `Signed-By` to scope a repository to selected keyrings/fingerprints. The documented recommended locations are `/usr/share/keyrings` for package-managed keys and `/etc/apt/keyrings` for operator-managed keys.

### Selection/integration criteria

Use APT when the target distribution's supported package ecosystem is Debian/Ubuntu-derived. Automation should record configured sources, refreshed metadata state, held packages, the resolved transaction, exit status, and post-change service/application evidence. Repository-authentication bypasses such as `allow-insecure` or `Trusted=yes` weaken the normal trust model and must not be treated as equivalent to authenticated repositories.

### Recovery boundary

APT can request a specific package version when it remains available, and holds can prevent future automatic changes, but the sources inspected here do **not** establish a universal transaction-history rollback equivalent to a filesystem snapshot rollback. Package downgrade availability depends on repository/package availability and dependency compatibility. Application data rollback remains separate.

## DNF5 / RPM family

### Verified implementation and semantics

Current DNF5 documentation provides package `upgrade`, `downgrade`, transaction `history`, offline transactions, and major-release `system-upgrade`. `dnf5 history undo` reverses one recorded transaction; `history rollback` undoes transactions after a selected transaction. These operations depend on recorded transaction history and on the required package actions remaining possible; options such as `--skip-unavailable`, `--ignore-extras`, and `--ignore-installed` explicitly alter strictness.

DNF5 can stage supported operations with `--offline`; the transaction then runs after reboot in a minimal environment. The official documentation describes this as safer with respect to interference from running processes, not as a guarantee of successful application behavior.

`dnf5 system-upgrade` downloads packages for a new major release and applies them offline. The default behavior can install versions from the new release even when they are lower than installed versions; `--no-downgrade` changes that behavior.

RPM itself can query and verify installed package metadata/files. `rpm --verify` compares recorded metadata such as size, digest, permissions, ownership and other attributes. `rpmkeys --checksig` verifies package digests/signatures against the RPM keyring.

DNF5 separates package, repository-metadata, and local-package signature policy. Current configuration documents `pkg_gpgcheck`, `repo_gpgcheck`, and `localpkg_gpgcheck` independently. Therefore a statement such as "GPG checking is enabled" is insufficient unless the exact configured plane is known.

### Selection/integration criteria

Use DNF5/RPM when that is the supported distribution package stack. For automation, preserve transaction history, repository identity, package/signature settings, proposed removals/downgrades, offline status/logs when used, and post-change host/service evidence.

### Recovery boundary

`dnf5 history undo/rollback` is a package transaction reversal mechanism, not proof of restoring arbitrary filesystem state or application data. Its success also depends on transaction records and package availability. RPM verification detects package-file/metadata differences within its model but does not prove application correctness.

## Zypper + Snapper / transactional-update

### Verified implementation and semantics

SUSE Linux Enterprise Server 15 SP7 documents `zypper` package update/patch/distribution-upgrade workflows together with Snapper and, on transactional systems, `transactional-update`.

On the default supported Btrfs-root setup, Snapper is configured to create pre/post snapshots around Zypper and YaST transactions. SUSE distinguishes two operations:

- **undo**: compare snapshots and restore selected changed files;
- **rollback**: reset the system root to the state captured by a snapshot.

SUSE's system rollback has explicit prerequisites. In SLES 15 SP7, supported bootable rollback requires the documented root filesystem/subvolume configuration; only the root subvolume contents are rolled back, while excluded subvolumes/filesystems are outside that boundary.

`transactional-update` creates a new snapshot, applies Zypper operations to that snapshot, and activates it for the next boot. Its documented `rollback` operation selects a prior/default snapshot according to the system mode. SUSE also warns that after service-pack rollback the repository/registration state must be checked because repository configuration can otherwise mismatch the restored system state.

### Selection/integration criteria

Treat Zypper package transactions, Snapper snapshots, and transactional-update as separate but integrated evidence planes. Before claiming rollback capability, verify the actual filesystem layout, snapshot configuration, bootability, excluded subvolumes, registration/repository state, and the application/data locations that are outside the snapshot.

### Recovery boundary

This is stronger system-state recovery evidence than a package-only downgrade, but it still is not universal machine-state recovery. SUSE explicitly scopes rollback to supported configurations and snapshot contents. External services, databases, remote state, and excluded subvolumes require independent recovery evidence.

## Arch Linux Pacman

### Verified implementation and semantics

The current Arch manual documents Pacman 7.1.0. `pacman -Syu` refreshes package databases and upgrades the installed system; `-U` installs/upgrades a package from a local path or URL. Passing `--sysupgrade` twice enables package downgrades to repository versions that do not match local versions, a behavior useful when switching repository tracks.

Pacman can ignore package or group upgrades (`--ignore`, `IgnorePkg`, `IgnoreGroup`). Its local package cache defaults to `/var/cache/pacman/pkg`, but cache cleaning can remove older package files, so cache presence must be verified before assuming a local downgrade artifact exists.

Pacman has package/file consistency checks: `-Qk` checks owned files are present and `-Qkk` performs deeper checks for packages with mtree metadata. Database checks via `-Dk` validate local database consistency and, when repeated, dependency availability in sync databases.

The current `pacman.conf` manual documents signature policy with `SigLevel`; the built-in default is `Required TrustedOnly`. Repository-specific, local-file, and remote-file signature levels can override policy.

Pacman also has explicit configuration-file merge semantics: when both the locally modified file and incoming package version differ from the original, the new version can be installed as `.pacnew`, requiring operator/user reconciliation.

### Selection/integration criteria

Use Pacman/libalpm on Arch-derived systems where it is the supported package stack. Automated upgrades should inspect repository synchronization, ignored packages/groups, transaction targets, package-signature policy, `.pacnew`/`.pacsave` outcomes where relevant, and application/service health after the package transaction.

### Recovery boundary

Pacman supports installing older package artifacts and repository-driven downgrades under documented conditions, but the inspected official manual does not establish a general transaction-history or filesystem snapshot rollback. Cache cleanup can remove older artifacts. Package downgrade must therefore not be equated with complete system or data rollback.

## Cross-manager comparison rules

Do not normalize unlike semantics:

- APT Release-file authentication is not the same mechanism as RPM per-package signature checks or Pacman `SigLevel`.
- DNF5 `history rollback` is package-transaction reversal; SUSE Snapper rollback is filesystem/root snapshot recovery under explicit prerequisites.
- Pacman `-Suu`/older-package installation is version selection, not state restoration.
- Holds/excludes (`apt-mark hold`, DNF exclusions, Pacman IgnorePkg, etc.) constrain future resolution; they do not revert already-applied changes.
- Package file verification (`rpm --verify`, `pacman -Qkk`) is integrity/state comparison within package metadata, not application semantic validation.

## AI-driven automation possibilities

AI systems may safely assist with package-manager operations when authoritative deterministic tools remain the execution and verification layer. Evidence-backed automation opportunities include:

- explain a proposed dependency transaction or removal set;
- correlate package changes with incidents;
- propose hold/exclusion policies;
- classify security/advisory-driven updates where package-manager metadata supports it;
- summarize offline/system-upgrade logs;
- identify package-file drift from deterministic verification output;
- generate rollback/recovery hypotheses;
- compare repository, package, and service state before/after maintenance.

AI output alone is not sufficient authority to bypass signature policy, force dependency removal, perform a major-release upgrade, delete package caches, or declare recovery successful. Execution should remain gated by package-manager resolution, trust verification, transaction results, and independent post-change service/application checks.

## Unresolved / intentionally not generalized

- Exact safe downgrade coverage for arbitrary APT repositories/package sets is unresolved; availability and dependency solvability are repository-state dependent.
- DNF5 package/repository signature defaults can be changed by distribution configuration; the upstream defaults documented here must not be assumed to equal every Fedora/RHEL-derived installation.
- SUSE snapshot rollback coverage outside the documented supported root/subvolume configurations is not generalized.
- Pacman package-cache retention is administrator/configuration dependent; an older package must not be assumed available.
- Cross-manager "atomic transaction" claims are not made. Their failure, scriptlet, reboot, filesystem, and application-data semantics differ materially.
- No package manager here is treated as an application-health rollback controller without a separately verified health/promotion layer.

## Primary sources

All sources verified 2026-08-20.

### Debian / APT

- Debian manpages, `apt(8)` / APT 3.x testing documentation: https://manpages.debian.org/testing/apt/apt.8.en.html
- Debian manpages, `apt-mark(8)`: https://manpages.debian.org/testing/apt/apt-mark.8.en.html
- Debian manpages, `apt-secure(8)`, source last updated 2026-05-17: https://dyn.manpages.debian.org/testing/apt/apt-secure.8.en.html
- Debian manpages, `sources.list(5)`: https://dyn.manpages.debian.org/unstable/apt/sources.list.5.en.html

### DNF5 / RPM

- DNF5 `upgrade`: https://dnf5.readthedocs.io/en/latest/commands/upgrade.8.html
- DNF5 `downgrade`: https://dnf5.readthedocs.io/en/stable/commands/downgrade.8.html
- DNF5 `history`: https://dnf5.readthedocs.io/en/stable/commands/history.8.html
- DNF5 `offline`: https://dnf5.readthedocs.io/en/stable/commands/offline.8.html
- DNF5 `system-upgrade`: https://dnf5.readthedocs.io/en/latest/commands/system-upgrade.8.html
- DNF5 configuration/signature policy: https://dnf5.readthedocs.io/en/latest/dnf5.conf.5.html
- RPM `rpm(8)`, dated 2026-07-17: https://rpm.org/docs/latest/man/rpm.8
- RPM `rpmkeys(8)`, dated 2026-07-17: https://rpm.org/docs/6.1.x/man/rpmkeys.8

### SUSE

- SLES 15 SP7 Administration Guide, publication date 2026-07-30: https://documentation.suse.com/sles/15-SP7/single-html/SLES-administration/index.html
- SLES 15 SP7 Snapper recovery/rollback: https://documentation.suse.com/en-us/sles/15-SP7/html/SLES-all/cha-snapper.html
- SLES 15 SP7 Upgrade Guide / rollback: https://documentation.suse.com/sles/15-SP7/single-html/SLES-upgrade/

### Arch Linux

- Arch manual, `pacman(8)`, Pacman 7.1.0, dated 2026-05-06: https://man.archlinux.org/man/pacman.8.en
- Arch manual, `pacman.conf(5)`, Pacman 7.1.0: https://man.archlinux.org/man/pacman.conf.5.en
