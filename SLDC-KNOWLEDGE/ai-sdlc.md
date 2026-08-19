# AI-assisted software-development lifecycle baseline

Verification date: 2026-08-19

This file separates **verified capability** from **open-ended discovery**. The finite required categories `AI-SDLC`, `Tools that help AI code`, and `AI-driven automation` can have a complete baseline without claiming that every AI product or future automation technique has been enumerated.

## 1. AI-SDLC baseline

### Definition

AI-SDLC is the use of AI assistants or agents in one or more software-development lifecycle phases while retaining explicit scope, provenance, permissions, validation gates, and failure boundaries.

### SDLC role

Verified primary documentation now covers representative AI assistance across planning/requirements, implementation, testing, review/security, CI repair, migration/maintenance, deployment guidance, and operations. This establishes a cross-vendor lifecycle baseline rather than a single-product capability claim.

### Representative verified implementations

#### Planning, requirements, prioritization — GitLab Planner Agent

GitLab documents a Planner Agent that can decompose initiatives into epics/features/user stories, draft requirements and planning artifacts, analyze dependencies, prioritize work, estimate work, manage backlog items, and produce status/risk summaries.

Integration points: GitLab work items, epics, issues, tasks, milestones, labels, dependencies, IDEs, GitLab UI.

Caveats: quality can decrease for large work-item sets; long comment histories may be incomplete; GitLab documents cases where an update can be incorrectly reported as successful.

Source: GitLab Docs, Planner Agent — https://docs.gitlab.com/user/duo_agent_platform/agents/foundational_agents/planner/ (official vendor docs; verified 2026-08-19; GA history documented through GitLab 19.2).

#### Plan → code → iterative changes — GitLab Software Development Flow

GitLab documents a Software Development Flow that gathers project context, creates a plan, works through tasks, stages proposed repository changes, and lets the user accept, modify, reject, pause, or redirect execution. It can use project structure, code, history, issues, merge requests and CI/job APIs.

Integration points: VS Code, Visual Studio, JetBrains, repository files/history, issues, merge requests, CI pipelines/jobs.

Caveats: the flow cannot access the external web; local execution can access sensitive local files; write operations are possible within granted permissions and therefore require permission/sandbox policy.

Source: GitLab Docs, Software Development Flow — https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/software_development/ (official vendor docs; verified 2026-08-19; generally available since GitLab 18.8 per source history).

#### Repository-aware implementation and review — GitHub Copilot agents

GitHub documents its coding agent as accepting work from issues, pull-request comments or chat, creating a branch, generating changes, executing automated tests and linters in an ephemeral environment, and opening a pull request. GitHub documents Copilot code review as reviewing pull requests, identifying issues, suggesting fixes, using broader repository context, agent skills and MCP servers, and handing suggestions to a coding agent.

Integration points: issues, repository, branches, ephemeral execution, tests, linters, pull requests, repository instructions, skills, MCP.

Caveat: GitHub explicitly states AI review can miss problems and must be validated.

Sources:
- GitHub Docs source for responsible use of Copilot agents — https://github.com/github/docs/blob/main/content/copilot/responsible-use/agents.md (primary documentation repository; verified 2026-08-19).
- GitHub Docs, About GitHub Copilot code review — https://docs.github.com/en/copilot/concepts/agents/code-review (official vendor docs; verified 2026-08-19).

#### Multi-step coding with IDE tools and MCP — Google Gemini Code Assist agent mode

Google documents Gemini Code Assist agent mode as supporting multi-step tasks, code generation from design documents/issues/TODO comments, project context, built-in file/symbol/Git tools, MCP servers, and user approval/editing of plans and tool use.

Integration points: VS Code, IntelliJ, repository/VCS, project symbols/files, MCP servers.

Caveat: the referenced agent mode is Preview / Pre-GA and therefore not a stable-GA compatibility guarantee.

Source: Google Cloud Docs, Agent mode overview — https://docs.cloud.google.com/gemini/docs/codeassist/agent-mode (official vendor docs; page last updated 2026-08-05; verified 2026-08-19).

#### Security and dependency/deployment-risk review — Amazon Q Developer

AWS documents Amazon Q Developer code review for SAST findings, secrets, IaC issues, code quality, software composition analysis, and code deployment risks. Reviews can cover recent changes, files, workspaces or projects and may offer remediation.

Integration points: IDE project/workspace, Git diff, source files, IaC, dependency graph/components, security/quality detectors.

Source: AWS Docs, Reviewing code with Amazon Q Developer — https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/code-reviews.html (official vendor docs; verified 2026-08-19).

#### Logic-level security review and SAST remediation — GitLab Duo

GitLab documents Security Review Flow for business-logic vulnerabilities such as access-control, authorization, information-disclosure and race-condition problems, with CWE/severity classifications and optional suggested fixes. GitLab separately documents agentic SAST vulnerability resolution that automatically analyzes SAST findings and can generate merge requests with context-aware fixes.

Integration points: merge-request diffs, GitLab SAST, vulnerability reports, service accounts, merge requests.

Caveats: Security Review Flow is documented as Beta and explicitly advisory; no findings is not proof of security. Agentic SAST resolution output must be reviewed by security professionals.

Sources:
- GitLab Docs, Security Review Flow — https://docs.gitlab.com/user/duo_agent_platform/agents/foundational_agents/security_review_agent/ (official vendor docs; verified 2026-08-19; Beta).
- GitLab Docs, SAST Vulnerability Resolution Flow — https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/agentic_sast_vulnerability_resolution/ (official vendor docs; verified 2026-08-19; GA history documented by source).

#### CI failure diagnosis and repair — GitLab Fix CI/CD Pipeline Flow

GitLab documents an AI flow that examines pipeline logs, failed-job output, merge-request changes, repository contents and script errors, then proposes code suggestions or creates a merge request. It can decline to fix when context is insufficient, security-sensitive or not actionable.

Integration points: CI pipelines/jobs, logs, merge requests, repository files, runners, AGENTS.md.

Caveats: only the last 150 KiB of job logs are processed; repository instructions are not guaranteed to be followed; package installation may not always be verifiable in the sandbox.

Source: GitLab Docs, Fix CI/CD Pipeline Flow — https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/fix_pipeline/ (official vendor docs; verified 2026-08-19; GA history documented through GitLab 19.2).

#### Migration / modernization with iterative verification — Amazon Q Developer

AWS documents automated application transformations, including Java and .NET modernization. The CLI transformation flow creates a branch, generates transformations in steps and repeatedly builds/tests in the local environment to verify changes before continuation. AWS explicitly recommends validating transformed code for functionality and security.

Integration points: source repository, branch, local build environment, tests, build artifacts/logs, transformation plan, diff/review.

Sources:
- AWS Docs, Transforming code on the command line — https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/transform-CLI.html (official vendor docs; verified 2026-08-19).
- AWS Docs, How Amazon Q Developer transforms code for Java language upgrades — https://docs.aws.amazon.com/amazonq/latest/qdeveloper-ug/how-CT-works.html (official vendor docs; verified 2026-08-19).

#### AI DevOps and AI CI/CD

The cross-vendor operational and pipeline baseline is maintained in `ai-ops-memory-context.md`. That file documents representative AWS, Google, GitHub and GitLab implementations, selection criteria, integrations, caveats and automation boundaries.

### AI-SDLC selection criteria

Select an AI-SDLC capability by evidence rather than brand. Evaluate:

1. **Lifecycle phase and task boundary** — exactly what phase/action is delegated.
2. **Execution authority** — read-only, local write, repository write, CI execution, cloud/infrastructure action, production action.
3. **Context sources and freshness** — repository, issues, docs, dependency graph, logs, incidents, MCP/tools; detect stale or truncated context.
4. **Verification surface** — build, tests, lint/static analysis, security scans, runtime inspection, deployment checks, independent review.
5. **Auditability/provenance** — commits, diffs, logs, session/audit events, cited source/context, tool traces.
6. **Isolation and secret handling** — sandbox, ephemeral environment, least privilege, data policy, untrusted-content treatment.
7. **Failure semantics** — ability to stop, decline, roll back, preserve partial evidence and state uncertainty.
8. **Maturity/version** — GA vs beta/preview, supported languages/IDEs/platforms, documented quotas and limits.
9. **Human-control requirement** — approval before irreversible, production, security-sensitive or high-impact actions.
10. **Cost/latency/reproducibility** — operational cost, repeatability, determinism of non-AI gates, and ability to reproduce failures.

### AI-SDLC automation possibilities

Verified representative possibilities include requirements drafting/work breakdown, planning, repository context gathering, code generation/modification, refactoring/migration, branch creation, lint/test/build execution, code/security review, SAST remediation, dependency/SCA review, IaC review, CI failure diagnosis, PR/MR creation, feedback iteration, deployment-risk analysis, operational investigation and context/tool access through protocols. These examples establish lifecycle breadth; they are not a claim that every implementation supports every item.

**Status: complete baseline.** All six completion elements are present: definition, SDLC role, representative cross-vendor implementations, selection criteria, integration points, automation possibilities, with current primary evidence.

## 2. Tools that help AI code

### Definition

Tools that help AI code are developer-facing or agent-facing systems that improve generation, modification, understanding, verification, review or delivery of software by supplying models, context, tools, execution environments, structured workflows or deterministic validation.

### Role in the SDLC

They bridge AI reasoning/generation with concrete software artifacts and deterministic engineering systems. The useful unit is not only the model: it is the combination of context acquisition, repository/tool access, execution, validation and review boundaries.

### Verified tool-class taxonomy

| Tool class | Purpose | Representative primary evidence |
|---|---|---|
| IDE/CLI coding assistants | Explain/generate/edit code interactively | Google Gemini Code Assist; Amazon Q Developer |
| Coding agents | Multi-step repository changes and reviewable branches/PRs | GitHub Copilot coding agent; GitLab Software Development Flow |
| Planning agents | Requirements, decomposition, prioritization, dependency planning | GitLab Planner Agent |
| AI code review | Review diffs/repositories and suggest fixes | GitHub Copilot code review; Amazon Q code review |
| AI security review/remediation | Logic review, SAST remediation, SCA/IaC/security findings | GitLab Security Review/SAST Resolution; Amazon Q review |
| CI diagnosis/remediation | Inspect failed jobs/logs and propose/apply repository fixes | GitLab Fix CI/CD Pipeline Flow |
| Migration/modernization agents | Transform applications with build/test feedback loops | Amazon Q transformations |
| Context/tool protocols | Connect agents to repositories, services, documentation and tools | MCP; see `agent-protocols.md` |
| Agent interoperability | Connect editor/client to coding agent or agent to agent | ACP and A2A; see `agent-protocols.md` |
| Repository instruction/skill files | Supply project-specific commands, policies and conventions | GitHub agent skills/instructions; GitLab AGENTS.md support |
| Deterministic engineering tools used by agents | Build, test, lint, format, static/security analysis, package managers, debuggers | See `core-toolchain.md`; GitHub/AWS/GitLab evidence above shows agents invoking or consuming such gates |
| Memory/context systems | Preserve/retrieve project/session knowledge and control context budgets | See `ai-ops-memory-context.md` |

### Selection criteria

Choose the smallest tool class that satisfies the task. Compare repository/context reach, supported languages/platforms, write authority, sandboxing, deterministic-tool integration, review/approval controls, logs/provenance, extensibility (for example MCP), maturity/preview status, quotas/costs, privacy/data boundaries, and the ability to verify outputs independently.

### Integration points

Common verified integration surfaces include IDEs, CLIs, Git repositories, issues/work items, pull/merge requests, CI runners/jobs/logs, build/test/lint tools, SAST/SCA/IaC scanners, MCP servers, project instruction files, local execution environments and cloud operational systems.

### Automation possibilities

These tools can automate bounded portions of context gathering, planning, code generation/editing, refactoring, migration, build/test/lint execution, review, security remediation, CI repair and change packaging. The automation boundary must be explicit; generated output is not itself proof of correctness.

**Status: complete baseline.** The taxonomy is representative and cross-vendor, not an exhaustive product catalog.

## 3. AI-driven automation

### Definition

AI-driven automation is automation in which an AI system selects, proposes or executes one or more task steps using available context and tools, while deterministic systems and explicit policies define authority and verification boundaries.

### Role in the SDLC

AI-driven automation can connect otherwise separate lifecycle systems: work planning → repository changes → deterministic engineering checks → review/security → CI/CD → operations/maintenance. It is useful where tasks require interpretation or synthesis, but it must defer correctness and safety claims to evidence-producing gates.

### Representative verified classes

- planning/requirements and work-item management;
- repository-aware coding and refactoring;
- code/security review and remediation;
- deterministic build/test/lint execution triggered by agents;
- CI failure diagnosis and proposed repair;
- migration/modernization with iterative build/test verification;
- context/tool retrieval through MCP;
- client/editor-agent interoperability through ACP;
- agent-to-agent communication through A2A;
- AI DevOps operational investigation and AI CI/CD workflows documented in `ai-ops-memory-context.md`.

### Selection criteria

Use the AI-SDLC criteria above plus two automation-specific checks: (1) whether every side effect has an explicit authority/approval model, and (2) whether success can be independently established by deterministic or observable evidence rather than an agent completion message.

### Integration points

Work trackers, repositories, IDE/CLI clients, CI/CD runners, deterministic developer tools, security scanners, deployment/operations systems, observability sources, memory/context stores, MCP servers and agent-interoperability protocols.

### Automation possibilities and open frontier

The verified classes above are sufficient for a baseline. Discovery remains intentionally open-ended for additional capabilities in research, architecture, documentation, dependency management, environment provisioning, fuzzing, profiling, release engineering, deployment, infrastructure operations, observability, incident response, project management, game/content pipelines, embedded/HIL, mobile release and data/ML workflows. New capabilities must be added only from current primary evidence.

**Status: complete baseline, open-ended discovery continues.** `complete` here means the finite six-part category baseline is satisfied; it does **not** mean all AI automation products, domains or future capabilities have been enumerated.

## 4. Correctness and security rule

AI output, an agent's success message, or the absence of an AI finding is not evidence of correctness or security. Establish completion through task-relevant evidence such as builds, tests, lint/static/security analysis, runtime/rendered inspection, CI/release/deployment checks, logs, reproducible behavior or authoritative external evidence.

This rule is directly supported by vendor caveats: GitHub states AI code review can miss problems; GitLab states Security Review findings are advisory and no findings does not prove security; AWS recommends validating generated transformations for functionality and security.
