# Application security, SBOM, dependency and deployment-policy baseline

Verification date: 2026-08-19

This file adds representative, primary-source-backed implementations for SBOMs, dependency vulnerability policy, secret scanning, SAST, DAST, runtime security, and deployment policy. These controls are complementary. A pass in one control must not be interpreted as proof that software is secure.

## 1. Software Bill of Materials (SBOM) — SPDX 3.0 and CycloneDX 1.7

### Baseline definition and SDLC role

An SBOM is a machine-readable inventory of software components and dependency relationships. It supports supply-chain visibility, vulnerability response, license/compliance analysis, and downstream policy decisions. It describes composition; by itself it does not prove artifact integrity, absence of vulnerabilities, or exploitability.

### Verified standards

SPDX identifies SPDX 3.0 as its current specification and states that SPDX is an international open standard (ISO/IEC 5962:2021).

CycloneDX identifies version 1.7 as current. Its object model can represent components, services, direct/transitive dependency relationships, metadata, and other supply-chain information. CycloneDX documents conventional SBOM JSON/XML filenames and media types.

### Selection and integration criteria

Choose an SBOM format based on ecosystem/tool interoperability, required object model, regulator/customer requirements, and downstream consumers. Preserve exact component versions and dependency relationships where resolvable. Generate SBOMs from the resolved/build-time dependency state when static manifest analysis is insufficient.

Integrate SBOM generation into build/release workflows and attach the resulting document to the immutable artifact/release. Keep SBOM generation distinct from provenance/signing: `supply-chain-security-fuzzing.md` documents SLSA and Sigstore controls.

### Automation possibilities

CI/CD can generate SBOMs, validate their schema, submit dependency snapshots, diff release-to-release component inventories, correlate components with vulnerability intelligence, and gate promotion based on explicit vulnerability/license policy.

### Sources

- SPDX specifications: https://spdx.dev/use/specifications/
- CycloneDX specification overview: https://cyclonedx.org/specification/overview/
- CycloneDX SBOM capability: https://cyclonedx.org/capabilities/sbom/
- GitHub dependency submission API / SBOM snapshots: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/use-dependency-submission-api

## 2. Dependency vulnerability and license policy — GitHub Dependency Review / Dependabot

### Baseline definition and SDLC role

Dependency policy evaluates introduced or existing third-party dependencies against defined security, malware, license, or organizational rules. The strongest integration point for newly introduced risk is before merge; existing/default-branch risk also requires continuous monitoring because new advisories can appear after code has shipped.

### Verified implementation

GitHub Dependency Review can inspect dependency changes in pull requests and its action can enforce workflow failure by vulnerability severity, dependency scope, allowed/denied licenses, and explicitly allowed advisories. GitHub's dependency graph records supported direct/transitive dependency data; dependencies resolved only at build time can require dependency submission.

Dependabot alerts are generated when a vulnerable dependency is detected based on the dependency graph and GitHub Advisory Database, including when new advisories are added after a dependency was already present. Dependabot security updates can raise update pull requests. Malware alerts are a separate capability and currently have ecosystem-specific limitations documented by GitHub.

### Selection and integration criteria

Define policy from project threat model and deployment scope rather than using one universal severity threshold. Evaluate runtime and development dependencies separately when their risk differs. Prefer lock/resolution data and build-time dependency submission for completeness. Record justified exceptions explicitly and time-bound them where policy permits.

### Automation possibilities

Pull-request checks can reject newly introduced dependencies above defined severity or license thresholds. Continuous monitoring can create alerts and remediation pull requests when advisories change. SBOM/dependency snapshots can feed external vulnerability-management systems.

### Sources

- GitHub supply-chain security concepts: https://docs.github.com/en/code-security/concepts/supply-chain-security
- Dependency Review action configuration: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/manage-your-dependency-security/configure-dependency-review-action
- Dependency graph recognition: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependency-graph-data
- Dependabot alerts: https://docs.github.com/en/code-security/concepts/supply-chain-security/dependabot-alerts
- Dependency submission API: https://docs.github.com/en/code-security/how-tos/secure-your-supply-chain/secure-your-dependencies/use-dependency-submission-api

## 3. Secret scanning — GitHub Secret Scanning

### Baseline definition and SDLC role

Secret scanning detects credentials or credential-like material that has entered source-control or collaboration surfaces. Prevention should occur as early as possible, while historical scanning is still required because secrets can already exist in history.

### Verified implementation

GitHub Secret Scanning scans Git history across branches for supported hardcoded credential types and also scans several collaboration surfaces. GitHub documents custom/generic patterns, validity checks, and push protection. When a leaked credential is detected, GitHub's guidance is to rotate/revoke the affected credential; deleting history is not a substitute for revocation.

GitHub also documents AI-detected secrets and AI-assisted custom-pattern generation. These are additional detection mechanisms, not grounds for removing deterministic patterns or remediation verification.

### Selection and integration criteria

Use provider-supported patterns where available, add narrowly tested custom patterns for organization-specific secrets, enable push protection where supported, and define a credential revocation/rotation runbook. Treat pattern matches as findings requiring triage; false positives and unsupported secret forms remain possible.

### Automation possibilities

Automate pre-push/PR blocking, repository-history scans, alert routing, validity checking where safe, and incident workflows that verify revocation/rotation. AI-generated patterns must be reviewed and tested against positive and negative fixtures before enforcement.

### Sources

- GitHub Secret Scanning concepts: https://docs.github.com/en/code-security/concepts/secret-security/secret-scanning
- Secret scanning reference: https://docs.github.com/en/code-security/reference/secret-security

## 4. Static application security testing (SAST) — CodeQL / SARIF

### Baseline definition and SDLC role

SAST analyzes source or an intermediate program representation without exercising a deployed application. It is suited to pre-merge and continuous code analysis for classes of defects expressible by the analyzer's model and queries.

### Verified implementation

GitHub CodeQL builds a language-specific database representation and executes queries to identify vulnerabilities and coding errors. Current documentation covers compiled and interpreted languages, built-in and custom queries, local/CI use through the CodeQL CLI, and SARIF output/upload. GitHub code scanning can also ingest compatible third-party SARIF 2.1.0 results.

### Selection and integration criteria

Select analyzers based on actual language/framework coverage, build-model fidelity, query quality, runtime cost, and CI integration. Verify that the analyzer successfully covered the intended language/build paths; a green job with incomplete extraction is not equivalent to a complete scan.

### Automation possibilities

Run analysis on protected/default branches and pull requests, fail narrowly scoped policy gates on qualifying findings, upload SARIF, and track findings to remediation. AI-assisted/autofix suggestions remain proposed code changes and require normal compilation, test, review, and security verification.

### Sources

- GitHub CodeQL concepts: https://docs.github.com/en/code-security/concepts/code-scanning/codeql
- CodeQL CLI: https://docs.github.com/en/code-security/concepts/code-scanning/codeql/codeql-cli
- Code scanning setup / SARIF integration: https://docs.github.com/en/code-security/concepts/code-scanning/setup-types

## 5. Dynamic application security testing (DAST) — OWASP ZAP

### Baseline definition and SDLC role

DAST exercises a running application over its exposed interfaces. It complements SAST because it observes runtime HTTP/API behavior, authentication, routing, and deployed configuration, but its coverage is constrained by what the scanner can reach and exercise.

### Verified implementation

ZAP's Automation Framework defines applications, authentication, sequential scan jobs, passive/active scans, spiders and job outcome tests in YAML. ZAP supports command-line/daemon/API automation and configurable exit status, making it suitable for CI against authorized test environments.

### Selection and integration criteria

Use an isolated/authorized environment for active scanning unless the selected scan mode is explicitly safe for the target. Configure authentication and application scope, preserve scan plans as code, and distinguish crawl/reachability gaps from clean findings.

### Automation possibilities

CI/CD can deploy an ephemeral environment, seed/authenticate a ZAP plan, spider/import API definitions, run passive/active scans, assert job tests, export findings, and gate on explicit alert policy. A passing scan means no qualifying issue was found in the explored scope; it does not prove absence of vulnerabilities.

### Sources

- ZAP automation overview: https://www.zaproxy.org/docs/automate/
- ZAP Automation Framework: https://www.zaproxy.org/docs/automate/automation-framework/
- ZAP job outcome tests: https://www.zaproxy.org/docs/desktop/addons/automation-framework/tests/

## 6. Runtime security — Falco

### Baseline definition and SDLC role

Runtime security observes behavior after software is running in its deployment environment. It addresses a different evidence plane from build-time SAST/DAST and supply-chain controls: actual host/container/Kubernetes/cloud events and behaviors.

### Verified implementation

Falco is a CNCF graduate runtime-security project. It observes Linux kernel and plugin event sources, enriches events with container/Kubernetes context, evaluates rules, and emits alerts that can be forwarded to downstream systems such as SIEM/data-lake integrations.

### Selection and integration criteria

Select runtime detections based on deployment platform, telemetry availability, threat model, alert volume, and response capability. Tune rules against known-good workload behavior and retain raw/event context needed for incident investigation. Detection without an ownership and response path is incomplete operationally.

### Automation possibilities

Automate rule deployment, alert routing, enrichment/correlation, incident-ticket creation, and bounded response playbooks. Destructive automated remediation should require stronger authorization and validation than read-only alerting.

### Sources

- Falco documentation: https://falco.org/docs/
- Falco getting started/runtime description: https://falco.org/docs/getting-started/

## 7. Deployment policy as code — OPA / Gatekeeper

### Baseline definition and SDLC role

Deployment policy evaluates proposed runtime configuration/artifacts against machine-readable rules before or during admission. It turns selected security, governance, cost, and reliability requirements into deterministic deployment gates.

### Verified implementation

Open Policy Agent can act as a Kubernetes admission controller and return allow/deny decisions for create/update/delete requests. Its official examples include image-registry restrictions and required resource settings. Gatekeeper is a Kubernetes validating/mutating webhook that executes OPA-backed policies and also provides audit functionality for existing resources. Current Gatekeeper documentation also describes integration with Kubernetes Validating Admission Policy.

### Selection and integration criteria

Keep policies small, explainable and testable. Define whether a rule is advisory/audit or blocking, and choose fail-open/fail-closed behavior according to availability and threat model. Pin policy inputs to verifiable artifact identity/provenance where possible instead of mutable tags or names.

### Automation possibilities

CI can test policy bundles against representative fixtures before deployment; cluster admission can reject nonconforming objects; audit can report existing violations. AI may draft policies or remediation suggestions, but enforcement policy requires deterministic tests and human/governance review before activation.

### Sources

- OPA Kubernetes admission control: https://www.openpolicyagent.org/docs/kubernetes
- Gatekeeper introduction/audit: https://open-policy-agent.github.io/gatekeeper/website/docs/
- Gatekeeper Validating Admission Policy integration: https://open-policy-agent.github.io/gatekeeper/website/docs/validating-admission-policy/

## Cross-control baseline

A defensible security pipeline composes controls rather than replacing one with another:

1. resolve dependencies and generate an SBOM;
2. evaluate newly introduced dependency/license risk before merge;
3. prevent/detect leaked secrets;
4. run SAST on source/build representation;
5. build/test/sign/attest immutable artifacts;
6. run DAST against an authorized deployed test surface;
7. enforce deployment policy against the exact artifact/configuration;
8. monitor runtime behavior and feed verified incidents back into tests/rules/policies.

AI can propose changes at every step, including dependency updates, query/rule changes, remediation patches, scan configuration, incident hypotheses and policy drafts. AI output is not itself a gate result. Promotion decisions should rely on deterministic scanner/test/policy outputs, signed provenance/identity where relevant, and explicit human authorization for high-impact exceptions or destructive response.

## Explicit unresolved scope

This representative baseline does not establish exhaustive coverage of:

- every SBOM generator/consumer or vulnerability database;
- every package ecosystem and transitive-resolution edge case;
- every secret type or secret-scanning implementation;
- every SAST/DAST/runtime scanner;
- container/image vulnerability scanners and cloud-security posture systems as separate baselines;
- mobile-specific SAST/DAST/runtime controls;
- infrastructure-as-code scanners beyond the deployment-policy representative implementation;
- AI security agents as autonomous correctness/security authorities.
