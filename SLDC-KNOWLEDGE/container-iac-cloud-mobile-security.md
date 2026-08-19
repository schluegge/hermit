# Container, IaC, cloud-posture and mobile-security baseline

Verification date: 2026-08-19

This file closes four explicitly tracked expansion gaps with current primary-source-backed representative implementations. These controls are complementary to `application-security-sbom-policy.md` and `supply-chain-security-fuzzing.md`; no single scanner or posture system is treated as a proof of security.

## 1. Container/image and repository scanning — Trivy

### Baseline definition and SDLC role

Container/image scanning evaluates built images and related package metadata for known vulnerabilities and selected configuration/security issues. Repository/filesystem scanning acts earlier in the lifecycle on dependency manifests, IaC, secrets, and licenses. The two scopes are related but not interchangeable: repository scans do not necessarily inspect the final built artifact, while image scans can observe packaged operating-system/application dependencies that source-only inspection may not represent.

### Verified implementation

Current Trivy documentation supports scanning local or remote code repositories for vulnerabilities, misconfigurations, secrets, and licenses, and can generate SBOMs. Filesystem scans support the same major scanner classes. Trivy's current image CLI exposes machine-readable formats including JSON, SARIF, CycloneDX and SPDX and an `--exit-code` option suitable for deterministic CI policy. Misconfiguration scanning covers Docker, Kubernetes, Terraform, CloudFormation and additional IaC types.

A relevant limitation is explicit in Trivy's documentation: misconfiguration scanning is not enabled by default for `image`, `fs`, and `repo`; callers must enable it with `--scanners misconfig` or an equivalent scanner list. Scope/flag configuration therefore belongs in the evidence record for any claimed scan.

### Selection and integration criteria

Select scan targets according to the artifact actually promoted: scan repositories early, then scan the immutable built image/artifact before release. Pin or record scanner version/configuration and vulnerability database freshness where reproducibility matters. Define severity/exception policy explicitly rather than equating any finding with automatic release failure. Preserve target digest/commit and scanner configuration with results.

### Automation possibilities

CI can run repository/filesystem scanning before build, image scanning after build, emit SARIF/SBOM artifacts, and fail on explicitly selected policy thresholds. Kubernetes environments can additionally use Trivy Operator to trigger workload vulnerability/configuration reports when cluster state changes. AI may triage or propose remediations, but scan findings and rebuilt-image re-scans remain the deterministic evidence gate.

### Sources

- Trivy repository scanning: https://trivy.dev/docs/latest/target/repository/
- Trivy filesystem scanning: https://trivy.dev/docs/latest/target/filesystem/
- Trivy misconfiguration scanning: https://trivy.dev/docs/latest/scanner/misconfiguration/
- Trivy image CLI reference: https://trivy.dev/docs/latest/guide/references/configuration/cli/trivy_image/
- Trivy Operator overview: https://aquasecurity.github.io/trivy-operator/latest/

## 2. Infrastructure-as-Code scanning — Checkov plus Trivy configuration scanning

### Baseline definition and SDLC role

IaC scanning evaluates declarative infrastructure configuration before deployment for policy violations and security/reliability misconfigurations. It belongs before provisioning and should also run continuously as policy/check sets evolve. It complements admission policy: IaC scanning evaluates intended configuration in source/build workflows; admission policy evaluates the actual deployment request.

### Verified implementations

Checkov documents policy-as-code scanning across Terraform, Terraform plans, CloudFormation, Kubernetes, Helm, ARM templates, Serverless and AWS CDK. It supports attribute-based and graph-based policies, custom policies, repository/directory/file scans, and CI/CD integrations. Trivy independently documents built-in IaC misconfiguration checks and custom checks, providing a second representative implementation rather than a single-vendor category claim.

### Selection and integration criteria

Choose scanners based on IaC dialect coverage, plan/rendered-output support, graph/cross-resource analysis, custom-policy mechanism, CI integration, and suppression governance. Scan generated/rendered representations when templates can materially differ from source. Treat suppressions as reviewed policy exceptions with rationale rather than invisible permanent exclusions.

### Automation possibilities

Pre-commit and pull-request workflows can scan IaC, annotate findings, run custom policy packs, and block selected severities/check IDs. CI can scan Terraform plans or rendered Kubernetes/Helm output before apply. AI can draft remediation or policy changes, but policy tests plus a fresh deterministic scan should verify them before merge/deploy.

### Sources

- Checkov overview: https://www.checkov.io/
- Checkov feature descriptions / CI integration: https://www.checkov.io/1.Welcome/Feature%20Descriptions.html
- Checkov quick start: https://www.checkov.io/1.Welcome/Quick%20Start.html
- Trivy IaC misconfiguration scanning: https://trivy.dev/docs/latest/scanner/misconfiguration/

## 3. Cloud Security Posture Management — AWS Security Hub CSPM

### Baseline definition and SDLC role

Cloud Security Posture Management continuously evaluates deployed cloud resources/accounts against explicit security controls and standards. It is a runtime/control-plane evidence layer: unlike IaC scanning, it can observe configuration drift and resources created outside the expected code path.

### Verified implementation

AWS Security Hub CSPM documents a consolidated view of security state across AWS accounts, services, and supported third-party products and evaluates environments against supported standards and controls. Current documentation lists AWS Foundational Security Best Practices and external frameworks, and also an AI Security Best Practices standard. Findings can be retrieved through console/API/CLI, aggregated across regions, and routed through automation rules or EventBridge/custom actions.

AWS also documents exposure findings that correlate signals from Security Hub CSPM, Inspector, GuardDuty, Macie and resource relationships to prioritize risk and provide remediation guidance. This is automated correlation/prioritization, not proof that a suggested remediation is correct or safe.

### Selection and integration criteria

Select CSPM according to actual cloud/provider coverage, supported controls/standards, organization/account aggregation, API/export capability, drift visibility, exception/suppression governance, and remediation integration. Preserve control identity, account/region/resource scope and finding timestamps. Evaluate shared-responsibility boundaries explicitly; CSPM does not replace application testing or secure design.

### Automation possibilities

Continuously collect posture findings, normalize/aggregate them, route qualifying findings to tickets/workflows, trigger bounded remediation actions, and verify that the relevant control returns to the intended state. High-impact remediation should retain authorization, rollback and post-change validation.

### Sources

- AWS Security Hub CSPM introduction: https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html
- Security Hub CSPM standards: https://docs.aws.amazon.com/securityhub/latest/userguide/standards-reference.html
- Exposure findings: https://docs.aws.amazon.com/securityhub/latest/userguide/exposure-findings.html
- Finding automation/remediation integration: https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html

## 4. Mobile application security — OWASP MASVS / MASTG

### Baseline definition and SDLC role

Mobile AppSec requires platform-specific controls and test techniques beyond generic web/application scanning because device storage, cryptography, authentication, network usage, platform interaction, resilience and privacy create distinct attack surfaces. A mobile baseline therefore needs explicit mobile requirements plus verifiable test procedures.

### Verified standards and testing guidance

OWASP MASVS is the Mobile Application Security Verification Standard and defines control groups for mobile security verification. OWASP MASTG is the corresponding technical testing and reverse-engineering guide for verifying MASVS controls through documented techniques and tests. OWASP explicitly states that MASVS is a baseline and cannot guarantee absolute security; secure architecture, design and threat modeling remain prerequisites.

### Selection and integration criteria

Map product threat model and assurance requirements to applicable MASVS controls, then select MASTG techniques/tests for Android/iOS and the actual application features. Preserve device/OS/app build, test technique, control identifier and evidence. Separate static package/code inspection, dynamic device/runtime testing, backend/API testing and platform configuration findings.

### Automation possibilities

Automate repeatable static checks, emulator/device setup, selected dynamic instrumentation/test steps, evidence collection, regression tests for known weaknesses and mapping of machine findings to MASVS identifiers where tooling supports it. Device/platform behavior and manual reverse-engineering findings remain necessary for controls that cannot be validated reliably by automation alone.

### Sources

- OWASP Mobile Application Security project: https://mas.owasp.org/
- OWASP MASVS: https://mas.owasp.org/MASVS/
- Using MASVS / limitations: https://mas.owasp.org/MASVS/03-Using_the_MASVS/
- OWASP MASTG: https://mas.owasp.org/MASTG/

## 5. AI-assisted security remediation — bounded representative evidence

### Verified current capabilities

GitHub documents Copilot Autofix for code scanning: LLM-generated targeted code changes are derived from code-scanning alerts and repository context. Agentic autofix (public preview as of verification date) can explore the codebase, generate a fix, validate it for example by re-running CodeQL, iterate, and open a pull request. GitHub explicitly limits the assurance: it is best-effort, custom/security-extended query coverage is not necessarily validated, and third-party finding fix quality is not guaranteed.

GitLab documents Duo Vulnerability Resolution for supported SAST findings. It can generate remediation suggestions in merge requests, while GitLab explicitly requires review because LLM output is not guaranteed correct and the reviewer must verify both preserved functionality and vulnerability resolution.

### Baseline integration rule

AI remediation is a proposal generator, not a security oracle. The defensible loop is:

1. preserve original scanner finding and exact scope;
2. generate/propose a bounded patch;
3. compile/build and run functional/regression tests;
4. re-run the originating deterministic security analyzer/query when supported;
5. run relevant adjacent security controls when the patch changes attack surface;
6. require normal review/authorization before merge;
7. retain before/after finding evidence.

### Sources

- GitHub Copilot Autofix for code scanning: https://docs.github.com/en/code-security/concepts/code-scanning/autofix-for-code-scanning
- GitLab Duo Vulnerability Resolution: https://docs.gitlab.com/user/application_security/remediate/duo/

## Cross-control boundary map

| Evidence plane | Representative implementation | What it can establish | What it does not establish |
|---|---|---|---|
| Repository/filesystem/image | Trivy | Detected known vulnerabilities/config/secrets/licenses in configured target | Absence of unknown vulnerabilities or complete runtime safety |
| IaC source/plan/rendered config | Checkov / Trivy | Violations detected in supported infrastructure definitions | Actual deployed-state compliance or runtime security |
| Cloud deployed state | AWS Security Hub CSPM | Supported control/posture findings for observed AWS resources/accounts | Application correctness or universal multi-cloud security |
| Mobile requirements/testing | OWASP MASVS / MASTG | Structured mobile controls and reproducible test guidance | Absolute mobile security or complete automation |
| AI remediation | GitHub/GitLab AI remediation | Candidate patches/explanations for supported findings | Correctness, completeness, preserved behavior or security without verification |

## Explicit unresolved scope

This remains a representative, non-exhaustive baseline. Still unresolved/open for later evidence passes:

- additional container/image scanners and vulnerability databases, including cross-scanner result differences;
- additional multi-cloud CSPM/CNAPP implementations and cloud-provider-specific posture systems;
- concrete mobile SAST/DAST/runtime tool implementations mapped against MASVS/MASTG;
- additional IaC scanners and policy engines, including cross-tool rule-coverage comparisons;
- autonomous AI security remediation beyond proposal/verified-loop patterns;
- release/deployment systems, rollback verification, progressive delivery and AI-assisted release operations as separate baselines.
