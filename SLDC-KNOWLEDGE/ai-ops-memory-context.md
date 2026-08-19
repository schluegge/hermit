# AI operations, CI/CD, memory, and context baseline

Verification date: 2026-08-19

This document closes four previously partial required categories with current primary-source evidence while keeping product-specific limitations explicit.

## AI DevOps

### Baseline definition

AI DevOps is the use of AI systems or agents to assist or automate software-delivery and operational work such as repository automation, infrastructure/application troubleshooting, observability analysis, incident investigation, remediation guidance, and operational coordination. AI-generated diagnosis or remediation remains advisory until independently validated or executed through bounded, auditable controls.

### SDLC / operations role

AI DevOps spans post-code lifecycle work: delivery automation, operational monitoring, troubleshooting, root-cause analysis, incident response, remediation planning, and operational communication.

### Representative verified implementations

#### Amazon Q Developer operational investigations

AWS documents operational investigations that analyze logs, metrics, deployments, and configuration changes; identify anomalies and likely root causes; and recommend curated runbooks. Investigations can start from CloudWatch alarms. AWS also documents Teams/Slack integrations and Jira/ServiceNow status updates.

Sources:
- AWS, Amazon Q Developer in chat applications — https://docs.aws.amazon.com/chatbot/ (official documentation; verified 2026-08-19).
- AWS, Monitoring investigations — https://docs.aws.amazon.com/chatbot/latest/adminguide/monitoring-investigations.html (official documentation; verified 2026-08-19).
- AWS, Investigate operational issues in your environment — https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/Investigations-Investigate.html (official documentation; verified 2026-08-19).

#### Gemini Cloud Assist investigations

Google documents Gemini Cloud Assist investigations as a root-cause-analysis tool that reviews logs, configurations, metrics, runbooks, and other signals to produce observations, hypotheses, probable root causes, and recommended fixes or troubleshooting steps. Google explicitly exposes links to source data for fact checking. As of 2026-04-10, creating/running/editing investigations requires Premium Support or requested access and remains a Preview offering. The OAuth token used by investigations is documented as not being used for mutating data.

Source: Google Cloud, Troubleshoot issues with Gemini Cloud Assist investigations — https://docs.cloud.google.com/cloud-assist/investigations (official documentation; verified 2026-08-19; Preview/access caveat applies).

### Selection criteria

- Supported cloud/runtime and resource coverage.
- Read-only versus mutating authority and the exact permission boundary.
- Source-data provenance and ability to inspect evidence behind conclusions.
- Trigger model: manual, alert-driven, chat-driven, or scheduled.
- Remediation model: recommendation only, bounded runbook execution, or direct mutation.
- Auditability, identity, IAM scope, and approval gates.
- Availability/GA status and support-plan requirements.
- Reproducibility and known stochastic behavior.

### Integration points

Observability signals, logs, metrics, alerts, deployment/configuration history, cloud resource inventory, runbooks, chat/incident channels, ticketing systems, and IAM.

### Automation possibilities

Verified: alert-triggered investigation; cross-signal analysis; anomaly/root-cause hypothesis generation; recommended remediation/runbooks; operational chat assistance; incident-status integration. Automated mutation is product- and permission-specific and must not be inferred from analysis capability alone.

## AI CI/CD

### Baseline definition

AI CI/CD applies AI agents or models inside continuous-integration and continuous-delivery workflows to perform contextual repository work, review, generation, triage, reporting, or other bounded pipeline tasks. AI steps supplement rather than replace deterministic build/test/security/release gates unless the release policy explicitly defines otherwise.

### SDLC role

Continuous integration, merge-request/pull-request review, repository maintenance, pipeline-side generation and analysis, and potentially release/deployment assistance where separately evidenced.

### Representative verified implementations

#### GitHub Agentic Workflows

GitHub documents Agentic Workflows as public-preview AI-powered repository automations defined in Markdown and executed by coding agents through GitHub Actions. They compile to hardened `.lock.yml` workflows and carry explicit workflow permissions and allowed write operations. GitHub documents support for multiple AI engines/agents rather than a single-model-only mechanism.

Sources:
- GitHub Docs, About GitHub Agentic Workflows — https://docs.github.com/en/copilot/concepts/agents/about-github-agentic-workflows (official documentation; verified 2026-08-19; public preview).
- GitHub Docs, Creating GitHub Agentic Workflows — https://docs.github.com/en/copilot/how-tos/github-agentic-workflows/creating-github-agentic-workflows (official documentation; verified 2026-08-19; public preview).

GitHub also documents running Copilot CLI inside GitHub Actions to automate AI-powered CI/CD tasks such as repository summaries, reports, or scaffolding.

Source: GitHub Docs, Automating tasks with Copilot CLI and GitHub Actions — https://docs.github.com/en/copilot/how-tos/copilot-cli/automate-copilot-cli/automate-with-actions (official documentation; verified 2026-08-19).

#### GitLab Duo Code Review Flow

GitLab documents Code Review Flow as an agentic review workflow that runs as a CI/CD job and requires a runner. It analyzes changes, repository structure and cross-file dependencies, then emits review feedback. GitLab documents explicit context-size limits and warns that truncated context can cause missed information.

Source: GitLab Docs, Code Review Flow — https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/code_review/ (official documentation; verified 2026-08-19).

### Selection criteria

- Whether the AI step is advisory or has write/deploy authority.
- Workflow permission minimization and secret isolation.
- Deterministic gates retained before merge/release/deploy.
- Runner isolation, network access, and artifact provenance.
- Context-size and truncation behavior.
- Re-run behavior, cost, latency, and stochastic variation.
- Ability to inspect agent logs, diffs, outputs, and resulting commits.
- Preview/beta/GA status.

### Integration points

CI runners, pull/merge requests, repository events, workflow triggers, branch protections, test/lint/security jobs, artifact/report generation, and approval gates.

### Automation possibilities

Verified: natural-language repository automation on CI runners; AI-powered reporting/scaffolding in Actions; agentic code review in CI/CD; automatic review triggers. General autonomous deployment, canary control, rollback, or production mutation are not inferred from these sources and require separate evidence.

## Memory

### Baseline definition

Agent memory is persisted information that can be recalled beyond the immediate model invocation and used to enrich later agent state or model context. Persistence scope and retrieval semantics are implementation choices, not universal protocol properties.

### SDLC role

Memory supports continuity across development sessions, retained project/user facts, prior agent actions, reusable examples/procedures, and durable workflow state.

### Representative verified implementations

#### LangGraph / LangChain

LangGraph documents short-term memory as thread-scoped state persisted through checkpoints and long-term memory as cross-session data stored in custom namespaces. Its conceptual model distinguishes semantic memory (facts), episodic memory (experiences/actions), and procedural memory (rules/instructions), and documents both foreground ('hot path') and background memory writing.

Sources:
- LangChain Docs, Memory overview — https://docs.langchain.com/oss/python/concepts/memory (maintainer documentation; verified 2026-08-19).
- LangChain Docs, Memory — https://docs.langchain.com/oss/python/langgraph/add-memory (maintainer documentation; verified 2026-08-19).

#### Microsoft AutoGen

AutoGen defines a `Memory` protocol with `add`, `query`, `update_context`, `clear`, and `close`; implementations may use different storage and retrieval mechanisms and are responsible for inserting relevant retrieved material into model context.

Source: Microsoft AutoGen, Memory and RAG — https://microsoft.github.io/autogen/stable/user-guide/agentchat-user-guide/memory.html (maintainer documentation; verified 2026-08-19).

### Selection criteria

- Scope: run, thread/session, project, user, organization, or global.
- Storage durability and transactional behavior.
- Retrieval mechanism: exact, indexed, semantic/vector, filtered, hybrid.
- Provenance, timestamps/versioning, and conflict resolution.
- Write policy: explicit, model-decided, deterministic, hot-path, or asynchronous/background.
- Retention/deletion, privacy, access control, and namespace isolation.
- Evaluation for stale, incorrect, duplicated, or poisoned memories.
- Ability to inspect and correct stored state.

### Integration points

Agent state/checkpoints, databases/stores, retrieval systems, project artifacts, model-context assembly, user/project profiles, and workflow history.

### Automation possibilities

Persist/resume agent state; retrieve project facts; preserve successful procedures/examples; record prior actions; automatically form or refresh memory subject to an explicit write policy and validation controls.

## Context management

### Baseline definition

Context management is the controlled selection, retrieval, structuring, prioritization, transformation, attribution, and delivery of task-relevant information to an AI system for a specific invocation or workflow step. Memory can be one source of context but is not identical to context.

### SDLC role

Context management determines what repository files, diffs, instructions, issues, documentation, external tool results, memories, and runtime evidence an AI coding system can use for planning, implementation, review, debugging, or operations.

### Representative verified mechanisms

LangChain documents runtime context categories including invocation-scoped/static context, state, and persistent cross-conversation context. It also documents practical context-pressure controls for long histories such as trimming, deleting, or summarizing messages.

Sources:
- LangChain Docs, Context overview — https://docs.langchain.com/oss/python/concepts/context (maintainer documentation; verified 2026-08-19).
- LangChain Docs, Short-term memory — https://docs.langchain.com/oss/python/langchain/short-term-memory (maintainer documentation; verified 2026-08-19).

GitLab's Code Review Flow provides a concrete coding example: it gathers repository and cross-file context, enforces file/aggregate context limits, truncates when limits are exceeded, and warns that truncated context can cause missed information.

Source: GitLab Docs, Code Review Flow — https://docs.gitlab.com/user/duo_agent_platform/flows/foundational_flows/code_review/ (official documentation; verified 2026-08-19).

MCP is separately documented in `agent-protocols.md` as one standardized mechanism for exposing external resources/tools/context; it is an integration protocol, not a complete context-management strategy.

### Selection criteria

- Relevance and freshness of selected material.
- Provenance and attribution back to source evidence.
- Token/context budget and explicit truncation behavior.
- Retrieval precision/recall and ranking strategy.
- Security boundary and least-privilege context exposure.
- Duplicate/conflicting/stale context handling.
- Compression/summarization fidelity and reversibility to primary evidence.
- Observability: ability to inspect what context the agent actually received.

### Integration points

Repository search/indexes, diffs, instruction files, memory stores, RAG/retrieval layers, MCP/external tools, issue trackers, documentation, observability data, and model invocation middleware.

### Automation possibilities

Automated retrieval/ranking; scoped repository context gathering; context-window trimming/summarization; memory retrieval; external-source acquisition through tool/protocol integrations; stale/duplicate filtering where explicitly implemented.

## Cross-category safety rule

AI-generated hypotheses, reviews, summaries, diagnoses, or remediation proposals are not correctness evidence by themselves. Use deterministic or independently inspectable gates appropriate to the operation: tests, static/security analysis, build artifacts, policy checks, source logs/metrics, deployment health, human approvals, reproducible runtime behavior, or rollback-capable bounded automation.
