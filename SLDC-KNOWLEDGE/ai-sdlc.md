# AI-assisted software-development lifecycle baseline

Verification date: 2026-08-19

This file deliberately separates **verified capability** from **coverage still unresolved**. The universe of AI-driven software-development automation is open-ended and is not claimed exhaustive.

## Verified capabilities

### Repository-aware code review

GitHub documents Copilot code review as reviewing pull requests, identifying issues, and suggesting fixes. It can gather broader repository context, use repository-level agent skills and MCP servers, and can pass suggestions to a cloud coding agent to create a follow-up pull request. GitHub explicitly warns that Copilot code review can miss problems and requires validation.

SDLC stages: review, quality feedback, remediation handoff.

Integration points: pull requests, GitHub Actions runners, repository instructions, agent skills, MCP servers.

Automation possibility: automatic PR review and agent-assisted remediation, with human or independent-tool validation retained as a gate.

Source: GitHub Docs, About GitHub Copilot code review — https://docs.github.com/en/copilot/concepts/agents/code-review (official vendor docs; verified 2026-08-19).

### Agentic coding and pull-request creation

GitHub documents its cloud coding agent as able to accept work from an issue, PR comment, or chat, create a branch, generate code changes, execute automated tests and linters in an ephemeral environment, and open a pull request.

SDLC stages: task intake, coding, branch creation, lint/test execution, pull-request creation, iteration from review feedback.

Integration points: issue tracker, repository, ephemeral execution environment, tests, linters, PR review.

Automation possibility: bounded implementation tasks can be delegated end-to-end up to a reviewable pull request; correctness is not established merely by agent completion.

Source: GitHub Docs source for responsible use of Copilot agents — https://github.com/github/docs/blob/main/content/copilot/responsible-use/agents.md (primary documentation repository; verified 2026-08-19).

### AI context acquisition through MCP

GitHub documents Copilot code review using configured MCP servers to pull context from third-party and internal systems such as issue tracking, documentation, service catalogs, and incident tooling. MCP itself standardizes AI access to tools and context.

SDLC stages: research/context gathering, review, incident-linked development, documentation-aware work.

Integration points: MCP server configuration, repository context, external systems.

Sources:
- GitHub Docs — https://docs.github.com/en/copilot/how-tos/use-copilot-agents/request-a-code-review/use-code-review (official vendor docs; verified 2026-08-19).
- MCP project — https://blog.modelcontextprotocol.io/posts/2026-07-28/ (official protocol project; verified 2026-08-19).

## Required AI categories and current baseline

### AI-SDLC — partial

**Baseline definition.** Application of AI systems/agents to one or more phases of the software-development lifecycle while preserving explicit verification, provenance, permissions, and failure boundaries.

**Verified stages so far.** Repository context gathering, coding, code review, test/lint execution, remediation PR creation.

**Selection criteria.** Task boundedness; available evidence/tests; permissions and side effects; repository context quality; audit logs/provenance; model/tool costs; data policy; reproducibility; ability to independently verify output.

**Unresolved for completion.** Need cross-vendor primary evidence and representative coverage of requirements, planning/architecture, security, release/deployment, operations/observability, incident response, migration, and maintenance.

### Tools that help AI code — partial

Verified classes: coding agents; AI code review; repository instructions; agent skills; MCP-provided context/tools; ephemeral execution with tests/linters.

Unresolved: representative cross-vendor/tool taxonomy and selection matrix.

### AI DevOps — partial

Verified intersection: AI agents can work with issue/repository context and CI execution environments; MCP can expose operational/service/incident systems as context/tools.

Unresolved: independent primary-source baseline for deployment, infrastructure changes, observability triage, incident remediation, rollback and production safety gates.

### AI CI/CD — partial

Verified intersection: GitHub Copilot code review can use GitHub Actions runners for agentic context gathering/tool use and cloud-agent environments can execute tests and linters.

Unresolved: generalized build/package/release/deploy pipeline automation, cross-provider evidence, autonomous gate policy, rollback/canary behavior.

### Memory — partial

**Baseline definition.** Persisted information made available across agent/model interactions beyond the immediate transient request context.

Potential subcategories requiring verification before adoption: working/session memory, episodic history, semantic/knowledge memory, artifact/repository memory, user/project preference memory.

Unresolved: representative implementations, retention/update semantics, conflict resolution, provenance, privacy/security, evaluation methods. No implementation is endorsed in this run.

### Context management — partial

**Baseline definition.** Selection, retrieval, structuring, prioritization, compression, attribution, and delivery of task-relevant information to an AI system within practical context limits.

Verified mechanisms: repository-wide context gathering in GitHub Copilot code review; repository instructions/skills; MCP resources/tools and external context integrations.

Unresolved: general retrieval/reranking/compression strategies, context-budget policy, stale-context detection, provenance/evaluation baseline.

### AI-driven automation — partial and intentionally open-ended

Verified in this run:
- context gathering;
- issue/task intake;
- branch creation;
- code generation/modification;
- lint execution;
- test execution;
- code review;
- suggested-fix generation;
- pull-request creation;
- feedback-driven iteration;
- external context/tool access through MCP;
- editor/agent interoperability through ACP;
- agent/agent task communication through A2A.

Research queue, **not yet claimed verified as a general baseline**: requirements elicitation, literature/repository research, planning, architecture, scaffolding, refactoring, semantic code search, documentation generation/maintenance, dependency updates, environment provisioning, build optimization, static/security analysis, fuzzing, profiling, release engineering, deployment, IaC operations, observability, incident response, migration, maintenance, knowledge management, project management, game/content pipelines, embedded/HIL workflows, mobile release workflows, data/ML lifecycle automation.

## Safety / correctness rule

Agent output is not evidence of correctness. Completion should be established through relevant tests, static analysis, build/release evidence, logs, rendered/runtime inspection, reproducible behavior, or authoritative external evidence depending on the task. GitHub's own documentation explicitly states that its AI code review may miss issues and should be validated.