# Ubuntu Core 26 update governance and recovery baseline

Verification date: 2026-08-20

Scope: Ubuntu Core 26 and current Canonical snap/Ubuntu Core documentation available on the verification date. This is a representative immutable/transactional OS implementation, not a universal Linux update model.

## Baseline definition

Ubuntu Core is a minimal immutable operating system whose operating-system and application components are delivered as snaps. Ubuntu Core 26 was released on 2026-05-14 and is the current stable Ubuntu Core release in the verified Canonical release notes.

For SDLC and fleet operations, treat the update path as distinct evidence planes:

1. **Artifact/revision identity** — snap revision, not merely the human-readable version.
2. **Update discovery and refresh policy** — automatic or controlled refresh.
3. **Cross-snap compatibility policy** — validation sets and, where applicable, refresh gating.
4. **Essential-snap staging** — kernel/base/gadget/snapd changes with boot-specific handling.
5. **Boot verification** — proof that the candidate essential system can boot.
6. **Recovery-system verification** — proof that a recovery environment can boot.
7. **Component revert** — reverting an individual snap revision/configuration state.
8. **Recovery/reinstall/factory reset** — device recovery modes with materially different data effects.
9. **Application/service health** — separate post-boot correctness evidence.

These planes must not be collapsed into a single statement such as “Ubuntu Core supports rollback.”

## Role in the SDLC

Ubuntu Core update governance belongs primarily to release, deployment, fleet operations, incident recovery, maintenance and supply-chain policy. It is relevant to embedded/IoT products and other appliance-style systems where base OS, kernel and application components must be updated over a device lifetime.

A safe automation design should distinguish:

`candidate revision -> compatibility policy -> staged refresh/remodel -> boot verification -> recovery-system verification -> service/application verification -> fleet promotion`

Boot success is necessary evidence for essential-snap changes but is not sufficient evidence of functional application correctness.

## Current verified implementation: Ubuntu Core 26

### Release and update model

Canonical's Ubuntu Core release notes identify Ubuntu Core 26 as released on 2026-05-14. Running Ubuntu Core systems automatically refresh snaps. Essential base and kernel snaps can refresh when compatible with the model/build-base constraints, and applying those changes can trigger a reboot.

Decision-relevant consequence: automation should identify deployed software by snap **revision** when assessing whether a specific rebuild/security fix is present. Canonical's CVE-remediation documentation explicitly distinguishes revision from the informational snap version string.

### Refresh control and validation sets

Default snap refresh is automatic. Canonical documents refresh control for deployments that must keep one or more snaps at tested revisions until a new revision is separately validated.

A validation set is a signed assertion defining snaps/components that are required, optional or invalid, and can optionally pin exact revisions. Validation sets can be declared in an Ubuntu Core model and used to keep interdependent snaps at a tested combination.

Important constraints:

- monitoring a validation set does not enforce it;
- enforced validation sets can block store install/refresh/remove operations that would violate the constraints;
- explicit `--ignore-validation` and local installs can bypass enforcement;
- Canonical recommends incrementing a production validation set's **sequence** when changing it because reverting to an older revision of the same sequence is not supported;
- validation-set enforcement is not intended to make hard breaking version dependencies safe during the transient period of a multi-snap update.

Therefore, “validation set present” is not equivalent to “all possible update paths are compatibility-safe.”

### Essential-snap remodel and boot verification

When a model change requires replacement of essential snaps, Ubuntu Core remodeling stages the incoming changes and tests base/kernel changes through reboot. Canonical documents that the new essential snap is only considered verified after successful boot; failed boot verification cancels the remodel and undoes changes made up to that point.

The remodel process also creates and verifies a new recovery system. Failure to verify the recovery system aborts the remodel and undoes the changes.

This is stronger evidence than package-manager transaction success because the candidate is exercised through an actual boot boundary. It still does not prove higher-layer service behavior, external dependencies, application state, device peripherals or business SLOs.

### Component revert semantics

Current Snap documentation supports reverting a snap to a previous or selected retained revision with `snap revert`. The operation reverts the snap revision and configuration/system data associated with the snap, but common user data such as application-generated database contents may not be reverted.

A reverted snap is not automatically re-applied merely because the reverted-from revision is still current; a new different revision can make it eligible for automatic refresh again. An explicit named `snap refresh` can also override that behavior.

Do not treat snap revert as a general application-data rollback.

### Recovery modes are not equivalent

Ubuntu Core exposes run, recover, install and factory-reset modes.

- **recover** boots a recovery environment while leaving running-system data untouched for repair/data retrieval;
- **factory reset** erases system data but preserves the `ubuntu-save` partition;
- **install/reinstall** can erase user and system data, including `ubuntu-save`, returning the device toward manufactured-image state.

The operational runbook must name the intended recovery mode. “Use recovery” is insufficient because the data-destruction semantics differ substantially.

## Representative tool / mechanism classes

| Need | Ubuntu Core mechanism | Evidence produced | Main caveat |
|---|---|---|---|
| Automatic component maintenance | snapd refresh | installed revision/update state | automatic refresh is not application-health proof |
| Controlled compatibility set | validation-set assertion | signed allowed/required revision constraints | bypass paths and transition limits exist |
| Cross-snap release gating | refresh control / gating snap where applicable | held/proceeded refresh state | some lower-level refresh-control interfaces remain under development |
| OS/model evolution | signed model assertion + remodel | authenticated target model and remodel result | remodel cannot downgrade the system base |
| Essential boot validation | staged base/kernel change + reboot | candidate boot succeeds/fails | does not validate full application behavior |
| Recovery-environment validation | remodel-created recovery system + verification reboot | recovery system succeeds/fails | recovery environment is not production-service validation |
| Component rollback | `snap revert` | prior retained snap revision/config active | common application user data may remain unchanged |
| Device recovery | recover/install/factory-reset modes | repair/reinitialization path | destructive semantics vary by mode |

## Selection criteria

Use Ubuntu Core's model when these characteristics are required and verified against the product:

- immutable/appliance-style OS composition is acceptable;
- software can be packaged as snaps or integrated through supported system snaps;
- automatic security refresh is desired, or a justified refresh-control policy is available;
- signed model/assertion governance matches the fleet's trust model;
- reboot boundaries for essential kernel/base changes are acceptable;
- the device has sufficient storage for candidate/recovery states;
- a tested recovery procedure exists for the actual hardware;
- application/state migration behavior is designed separately from snap revision rollback.

Do not select it solely because “automatic rollback” appears in a product summary. The exact mechanism and protected state depend on whether the operation is a snap refresh/revert, essential-snap boot test, remodel, recovery boot, reinstall or factory reset.

## Integration points

Verified integration surfaces include:

- Snap Store / dedicated store distribution;
- snapd automatic/manual refresh;
- validation-set assertions;
- signed model assertions;
- `snap remodel`;
- snapd REST API for remodeling and recovery-system operations;
- recovery modes and recovery-system labels;
- fleet-management layers that schedule or govern refreshes.

Application observability, peripheral tests, data-integrity validation and business SLOs remain separate integration points that should gate fleet promotion when relevant.

## AI-driven automation possibilities

Evidence supports automating the deterministic operations and evidence collection around Ubuntu Core, including:

- inspect installed snap revisions and model state;
- compare candidate revisions against an approved validation set;
- prepare or request controlled refreshes;
- execute signed-model remodel workflows;
- collect boot/remodel/recovery verification results;
- detect a failed verification and stop promotion;
- inventory recovery systems and revision retention;
- correlate device/application telemetry with a staged cohort before wider rollout.

An AI system may assist with research, failure summarization, fleet segmentation, evidence correlation and proposing remediation. It should not be granted production update authority merely because Ubuntu Core itself supplies boot/recovery mechanisms. Promotion authority should remain bounded by deterministic policy, authenticated artifacts/assertions and explicit health gates.

## Contradiction and deduplication rules

- Ubuntu Core snap refresh is not rpm-ostree deployment switching, bootc image switching or NixOS generation activation.
- Snap revision is not the same identifier as the user-facing snap version.
- Validation-set validity is not proof of application compatibility.
- Boot verification is not service/SLO verification.
- `snap revert` is not full user-data rollback.
- Recovery mode is not reinstall; reinstall is not factory reset.
- Remodel boot rollback is not proof that every external side effect was reversed.
- An authenticated model/assertion is authorization/provenance evidence, not functional correctness evidence.

## Unresolved

The following remain unresolved rather than inferred:

- quantitative fleet-wide promotion thresholds for crash, boot-failure, latency or device-health evidence;
- general automatic post-boot service/SLO rollback behavior for arbitrary Ubuntu Core applications;
- exact failure semantics across every supported bootloader, hardware platform and interrupted-power condition;
- fleet-scale guarantees when external peripherals/firmware must change atomically with an Ubuntu Core remodel;
- a general AI system with independently documented authority to approve and execute production Ubuntu Core fleet promotion while preserving deterministic safety gates.

## Sources

All sources are primary Canonical documentation unless stated otherwise. Verified 2026-08-20.

1. Ubuntu Core release notes — current stable release and update mechanism.  
   Source type: official product documentation. Scope: Ubuntu Core 26/current release policy.  
   https://documentation.ubuntu.com/core/reference/release-notes/

2. Ubuntu Core 26 — immutable OS/product scope.  
   Source type: official product documentation. Scope: Ubuntu Core 26.  
   https://documentation.ubuntu.com/core/uc26/

3. Refresh control — automatic refresh and controlled revision rollout.  
   Source type: official product documentation.  
   https://documentation.ubuntu.com/core/explanation/refresh-control/

4. Validation sets — cross-snap constraints and intended update orchestration.  
   Source type: official Snap documentation.  
   https://snapcraft.io/docs/explanation/how-snaps-work/validation-sets/

5. Manage validation sets — enforcement, bypasses, sequence/recovery constraints and transition caveats.  
   Source type: official Snap documentation.  
   https://snapcraft.io/docs/how-to-guides/manage-snaps/manage-validation-sets/

6. Remodel essential snaps — staged essential-snap replacement, boot verification, failure undo and recovery-system verification.  
   Source type: official Ubuntu Core documentation.  
   https://documentation.ubuntu.com/core/explanation/remodel-essential-snaps/

7. Remodeling — model assertions, remodel viability, downgrade restriction and validation-set integration.  
   Source type: official Ubuntu Core documentation.  
   https://documentation.ubuntu.com/core/explanation/remodeling/

8. Manage updates — `snap revert` behavior and data/revision boundaries.  
   Source type: official Snap documentation.  
   https://snapcraft.io/docs/how-to-guides/manage-snaps/manage-updates/

9. Recovery modes — recover/install/factory-reset semantics.  
   Source type: official Ubuntu Core documentation.  
   https://documentation.ubuntu.com/core/explanation/recovery-modes/

10. CVE remediation in Ubuntu Core — revision identity and automatic security refresh model.  
    Source type: official Ubuntu Core documentation.  
    https://documentation.ubuntu.com/core/explanation/cve-remediation/

11. Model assertion reference — validation-set enforcement modes in the device model.  
    Source type: official Ubuntu Core reference.  
    https://documentation.ubuntu.com/core/reference/assertions/model/
